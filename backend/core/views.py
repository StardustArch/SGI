"""
views.py — SGI Internato IICB

Alterações desta versão:
  - BUG FIX: TopInfratoresView duplicada removida (mantida só a do dashboard)
  - BUG FIX: perform_update do MensalidadeDetailView corrigido (double save removido)
  - BUG FIX: PasswordResetRequestView protegida contra User.DoesNotExist
  - BUG FIX: ExportarRelatorioView usa IsAnyAdminUser em vez de 3 permissões em AND
  - BUG FIX: EncarregadoFinanceiroStatsView — 'Atraso' calculado correctamente
  - BUG FIX: PedidoSaidaSummaryView — estado 'Aprovado_Admin' corrigido
  - REMOVIDO: FinanceiroSummaryView, TopInfratoresView, TopAusentesView,
              TipoSancaoSummaryView, PedidoSaidaSummaryView (redundantes com AdminDashboardView)
  - REMOVIDO: GerarReciboView simplificada — modelo Recibo eliminado, campos em Mensalidade
  - MANTIDO: AdminDashboardView como endpoint único de dashboard
"""

from django.shortcuts import render
from rest_framework import generics, status, filters
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    Utilizador, Perfil, Encarregado, Estudante,
    Mensalidade, Sancao, PresencaEstudo, PedidoSaida, Quarto,
)
from .serializers import (
    UserSerializer, RegistoCompletoSerializer,
    MensalidadeSerializer, MensalidadeUpdateSerializer,
    SancaoSerializer, SancaoUpdateSerializer,
    PresencaBatchSerializer, PresencaEstudoSerializer, PresencaEstudoUpdateSerializer,
    EstudanteListSerializer, EstudanteDetailSerializer, EstudantePerfilSerializer,
    PedidoSaidaSerializer, PedidoSaidaListAdminSerializer, PedidoSaidaUpdateAdminSerializer,
    PedidoSaidaEncarregadoUpdateSerializer,
    EncarregadoAdminSerializer, EncarregadoProfileUpdateSerializer,
    MensalidadeAdminListSerializer,
    QuartoSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer, SetNewPasswordSerializer,
    GerarMensalidadesLoteSerializer,
    TransferirQuartoSerializer,
)
from .permissions import (
    IsAdminUser, IsAnyAdminUser,
    IsGestorOuSuporte, IsFinanceiroOuSuporte,
    IsDisciplinarOuSuporte, IsEstudanteUser,
    IsEncarregadoUser, IsOwnerOfPedidoSaida,
)
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.db.models import Sum, Count, Q
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from django.http import HttpResponse
from .utils import gerar_numero_recibo
import io
import pandas as pd
from io import BytesIO


# ---------------------------------------------------------------------------
# PAGINAÇÃO PADRÃO
# ---------------------------------------------------------------------------

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ---------------------------------------------------------------------------
# UTILIZADOR / AUTH
# ---------------------------------------------------------------------------

class ManageUserView(generics.RetrieveAPIView):
    """Retorna os dados do utilizador autenticado (token)."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """Permite ao utilizador autenticado mudar a sua própria senha."""
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "Senha alterada com sucesso."}, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    """Passo 1 do reset de senha: envia link por email."""
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        User = get_user_model()

        # FIX: protegido contra DoesNotExist (race condition possível)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Por segurança não revelamos se o email existe ou não
            return Response({"status": "Se o email existir, receberá o link."}, status=status.HTTP_200_OK)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        reset_link = f"{frontend_url}/auth/reset-password?uid={uidb64}&token={token}"

        try:
            send_mail(
                subject="Recuperação de Senha — SGI IICB",
                message=(
                    f"Olá {user.first_name},\n\n"
                    f"Use o link abaixo para redefinir a sua senha:\n\n{reset_link}\n\n"
                    f"Se não pediu isto, ignore este email."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception:
            return Response(
                {"erro": "Erro ao enviar email. Contacte o administrador."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"status": "Se o email existir, receberá o link."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """Passo 2 do reset: valida token e define nova senha."""
    permission_classes = []

    def patch(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response({"status": "Senha redefinida com sucesso."}, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# REGISTO COMPLETO (Admin cria Encarregado + Estudante de uma vez)
# ---------------------------------------------------------------------------

class RegistoCompletoView(generics.CreateAPIView):
    """
    Endpoint para o Admin registar um Encarregado e Estudante
    numa transacção atómica com alocação de quarto.
    """
    serializer_class = RegistoCompletoSerializer
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dados = serializer.validated_data
        dados_enc = dados['encarregado']
        dados_est = dados['estudante']

        User = get_user_model()
        SENHA_PADRAO = "mudar1234"

        try:
            perfil_enc = Perfil.objects.get(nome_perfil='Encarregado')
            perfil_est = Perfil.objects.get(nome_perfil='Estudante')

            with transaction.atomic():
                quarto = dados_est['quarto']

                if dados_est['genero'] != quarto.genero_permitido:
                    return Response(
                        {"erro": "O género do estudante não é compatível com o quarto seleccionado."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if quarto.vagas_disponiveis <= 0:
                    return Response(
                        {"erro": "Este quarto já atingiu a capacidade máxima."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                user_enc = User.objects.create_user(
                    email=dados_enc['email'],
                    password=SENHA_PADRAO,
                    first_name=dados_enc['nome_completo'],
                    perfil=perfil_enc,
                )
                encarregado = Encarregado.objects.create(
                    utilizador=user_enc,
                    nome_completo=dados_enc['nome_completo'],
                    telefone_principal=dados_enc['telefone_principal'],
                    email_contacto=dados_enc['email'],
                )

                user_est = User.objects.create_user(
                    email=dados_est['email'],
                    password=SENHA_PADRAO,
                    first_name=dados_est['nome_completo'],
                    perfil=perfil_est,
                )
                estudante = Estudante.objects.create(
                    utilizador=user_est,
                    encarregado=encarregado,
                    nome_completo=dados_est['nome_completo'],
                    genero=dados_est['genero'],
                    quarto=quarto,
                    curso=dados_est['curso'],
                )
                # A ocupação do quarto é actualizada pelo Signal post_save do Estudante

            return Response(
                {"status": "sucesso", "estudante_id": estudante.utilizador_id},
                status=status.HTTP_201_CREATED
            )

        except Perfil.DoesNotExist:
            return Response(
                {"erro": "Perfis 'Encarregado' ou 'Estudante' não encontrados na base de dados."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------
# ESTUDANTES
# ---------------------------------------------------------------------------

class EstudanteListView(generics.ListAPIView):
    """Lista e pesquisa estudantes. Por defeito só activos; ?estado=Inactivo para histórico."""
    serializer_class = EstudanteListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nome_completo']
    filterset_fields = ['estado', 'genero', 'quarto']

    def get_queryset(self):
        # FIX: aceita ?estado=Inactivo para o admin ver o histórico completo
        estado = self.request.query_params.get('estado', 'Activo')
        return Estudante.objects.filter(estado=estado).order_by('nome_completo')


class EstudanteDetailView(generics.RetrieveUpdateAPIView):
    """GET: Detalhes de um estudante. PATCH: Actualizar dados."""
    queryset = Estudante.objects.all()
    serializer_class = EstudanteDetailSerializer
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]


class TransferirQuartoView(APIView):
    """
    PATCH: Transfere um estudante de quarto de forma atómica.
    Valida género e vagas. A ocupação de ambos os quartos é
    recalculada automaticamente pelo Signal.
    """
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]

    def patch(self, request, pk):
        estudante = get_object_or_404(Estudante, pk=pk)
        serializer = TransferirQuartoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quarto_destino = serializer.validated_data['quarto_destino']

        if estudante.genero != quarto_destino.genero_permitido:
            return Response(
                {"erro": "O género do estudante não é compatível com o quarto de destino."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quarto_destino.vagas_disponiveis <= 0:
            return Response(
                {"erro": "O quarto de destino não tem vagas disponíveis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Guardar referência ao quarto anterior para o Signal recalcular
            estudante._quarto_anterior_id = estudante.quarto_id
            estudante.quarto = quarto_destino
            estudante.save()
            # Signal post_save recalcula ocupação de ambos os quartos

        return Response(
            {"status": f"Estudante transferido para o Quarto {quarto_destino.numero} com sucesso."},
            status=status.HTTP_200_OK
        )


# ---------------------------------------------------------------------------
# MENSALIDADES
# ---------------------------------------------------------------------------

class MensalidadeListCreateView(generics.ListCreateAPIView):
    """GET: Lista mensalidades de um estudante. POST: Cria mensalidade."""
    serializer_class = MensalidadeSerializer
    permission_classes = [IsAuthenticated, IsFinanceiroOuSuporte]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        estudante_id = self.kwargs['estudante_id']
        return Mensalidade.objects.filter(estudante_id=estudante_id).order_by('-mes_referencia')

    def perform_create(self, serializer):
        estudante_id = self.kwargs['estudante_id']
        estudante = get_object_or_404(Estudante, pk=estudante_id)
        serializer.save(estudante=estudante, admin_id_registo=self.request.user)


class MensalidadeDetailView(generics.RetrieveUpdateAPIView):
    queryset = Mensalidade.objects.all()
    permission_classes = [IsAuthenticated, IsFinanceiroOuSuporte]
 
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return MensalidadeUpdateSerializer
        return MensalidadeSerializer
 
    def perform_update(self, serializer):
        # FIX: update_fields não funciona como kwarg no serializer.save() do DRF.
        # A solução correcta é:
        #   1. Guardar via serializer (sem update_fields) para validar e persistir
        #   2. Se o estado mudou para 'Pago', fazer um save() explícito com update_fields
        #      para que o signal confirmar_pagamento consiga detectar a mudança.
        instance = serializer.save(admin_id_registo=self.request.user)
 
        if 'estado' in serializer.validated_data and instance.estado == 'Pago':
            instance.save(update_fields=['estado'])

class AdminMensalidadeListView(generics.ListAPIView):
    """Lista global de mensalidades com filtro por estado e pesquisa."""
    queryset = Mensalidade.objects.all().order_by('-mes_referencia')
    serializer_class = MensalidadeAdminListSerializer
    permission_classes = [IsAuthenticated, IsFinanceiroOuSuporte]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['estudante__nome_completo']

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get('estado', None)
        if estado == 'Atraso':
            # FIX: 'Atraso' não é estado persistido — calculado correctamente
            hoje = timezone.now().date()
            queryset = queryset.filter(estado='Pendente', data_vencimento__lt=hoje)
        elif estado:
            queryset = queryset.filter(estado=estado)
        return queryset


class GerarMensalidadesLoteView(APIView):
    """
    POST: Cria mensalidades 'Pendente' para TODOS os estudantes activos
    de uma vez. Ignora quem já tem mensalidade para o mês. 
    Poupa ~200 cliques/mês ao admin.
    """
    permission_classes = [IsAuthenticated, IsFinanceiroOuSuporte]

    def post(self, request):
        serializer = GerarMensalidadesLoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data_ref = serializer.validated_data['mes_referencia'].replace(day=1)
        valor = serializer.validated_data.get('valor_padrao', 0.0)

        estudantes_ativos = Estudante.objects.filter(estado='Activo')
        total = estudantes_ativos.count()
        criados = 0
        ignorados = 0

        with transaction.atomic():
            for estudante in estudantes_ativos:
                _, created = Mensalidade.objects.get_or_create(
                    estudante=estudante,
                    mes_referencia=data_ref,
                    defaults={
                        'estado': 'Pendente',
                        'valor_pago': valor,
                        'admin_id_registo': request.user,
                    }
                )
                if created:
                    criados += 1
                else:
                    ignorados += 1

        return Response({
            "mensagem": f"Processamento concluído para {data_ref.strftime('%B de %Y')}.",
            "total_estudantes": total,
            "mensalidades_criadas": criados,
            "ja_existiam": ignorados,
        }, status=status.HTTP_201_CREATED)


# ---------------------------------------------------------------------------
# RECIBO PDF
# FIX: modelo Recibo eliminado — campos numero_recibo e arquivo_pdf em Mensalidade
# ---------------------------------------------------------------------------

class GerarReciboView(APIView):
    """Gera e devolve o PDF do recibo de uma mensalidade paga."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        mensalidade = get_object_or_404(Mensalidade, pk=pk)

        if mensalidade.estado != 'Pago':
            return Response(
                {"erro": "Só é possível gerar recibo para mensalidades pagas."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # FIX: sem modelo Recibo separado — número gerado e guardado directamente
        if not mensalidade.numero_recibo:
            mensalidade.numero_recibo = gerar_numero_recibo()
            mensalidade.save(update_fields=['numero_recibo'])

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            f'attachment; filename="recibo_{mensalidade.numero_recibo}.pdf"'
        )

        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle(
            'Titulo', parent=styles['Heading1'], alignment=1, fontSize=16
        )

        estudante = mensalidade.estudante
        encarregado = estudante.encarregado

        conteudo = [
            Paragraph("INSTITUTO INDUSTRIAL E COMERCIAL DA BEIRA", estilo_titulo),
            Paragraph("Internato — Recibo de Pagamento", estilo_titulo),
            Spacer(1, 0.5 * cm),
        ]

        dados_recibo = [
            ["Número do Recibo:", mensalidade.numero_recibo],
            ["Mês de Referência:", mensalidade.mes_referencia.strftime("%B/%Y")],
            ["Valor Pago:", f"{mensalidade.valor_pago:.2f} MZN"],
            ["Método:", mensalidade.get_metodo_pagamento_display() or "—"],
            ["Referência/Comprovativo:", mensalidade.referencia_comprovativo or "—"],
            ["Data de Confirmação:", str(mensalidade.data_pagamento_confirmado or "—")],
        ]
        dados_estudante = [
            ["Nome:", estudante.nome_completo],
            ["Curso:", estudante.curso],
            ["Quarto:", estudante.quarto.numero if estudante.quarto else "Não atribuído"],
            ["Encarregado:", encarregado.nome_completo],
        ]

        estilo_tabela = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ])

        for titulo, dados in [("Dados do Pagamento", dados_recibo), ("Dados do Estudante", dados_estudante)]:
            conteudo.append(Paragraph(titulo, styles['Heading2']))
            t = Table(dados, colWidths=[5 * cm, 8 * cm])
            t.setStyle(estilo_tabela)
            conteudo.append(t)
            conteudo.append(Spacer(1, 0.5 * cm))

        conteudo.append(Spacer(1, 1 * cm))
        conteudo.append(Paragraph("___________________________________", styles['Normal']))
        conteudo.append(Paragraph("Assinatura do Responsável Financeiro", styles['Normal']))

        doc.build(conteudo)
        return response


# ---------------------------------------------------------------------------
# SANÇÕES
# ---------------------------------------------------------------------------

class SancaoListCreateView(generics.ListCreateAPIView):
    """Lista e cria sanções de um estudante específico."""
    serializer_class = SancaoSerializer
    permission_classes = [IsAuthenticated, IsDisciplinarOuSuporte]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Sancao.objects.filter(
            estudante_id=self.kwargs['estudante_id']
        ).order_by('-data_ocorrencia')

    def perform_create(self, serializer):
        estudante = get_object_or_404(Estudante, pk=self.kwargs['estudante_id'])
        serializer.save(estudante=estudante, admin_id_registo=self.request.user)


class SancaoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET / PATCH / DELETE de uma sanção."""
    queryset = Sancao.objects.all()
    permission_classes = [IsAuthenticated, IsDisciplinarOuSuporte]

    def get_serializer_class(self):
        return SancaoUpdateSerializer if self.request.method == 'PATCH' else SancaoSerializer


class AdminSancaoListCreateView(generics.ListCreateAPIView):
    """Lista global de sanções com pesquisa."""
    queryset = Sancao.objects.all().order_by('-data_ocorrencia')
    serializer_class = SancaoSerializer
    permission_classes = [IsAuthenticated, IsDisciplinarOuSuporte]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(admin_id_registo=self.request.user)


# ---------------------------------------------------------------------------
# PRESENÇAS
# ---------------------------------------------------------------------------

class PresencaBatchCreateView(APIView):
    """POST: Regista presenças de todos os alunos de um dia em lote."""
    permission_classes = [IsAuthenticated, IsDisciplinarOuSuporte]

    def post(self, request, *args, **kwargs):
        serializer = PresencaBatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data_presenca = data['data_presenca']
        admin_logado = request.user

        ids_ausentes = set(data.get('ausentes_ids', []))
        ids_justificados = set(data.get('justificados_ids', []))

        todos_ativos = Estudante.objects.filter(estado='Activo')
        presencas = []

        for estudante in todos_ativos:
            if estudante.pk in ids_ausentes:
                estado = 'Ausente'
            elif estudante.pk in ids_justificados:
                estado = 'Justificado'
            else:
                estado = 'Presente'

            presencas.append(PresencaEstudo(
                estudante=estudante,
                admin_id_registo=admin_logado,
                data_presenca=data_presenca,
                estado=estado,
            ))

        try:
            with transaction.atomic():
                PresencaEstudo.objects.bulk_create(presencas)
        except Exception as e:
            return Response(
                {"erro": f"Já existem presenças registadas para este dia? Detalhe: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"status": f"{len(presencas)} presenças registadas para {data_presenca}."},
            status=status.HTTP_201_CREATED
        )


class EstudantePresencaListView(generics.ListAPIView):
    """Lista o histórico de presenças de um estudante."""
    serializer_class = PresencaEstudoSerializer
    permission_classes = [IsAuthenticated, IsDisciplinarOuSuporte]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return PresencaEstudo.objects.filter(
            estudante_id=self.kwargs['estudante_pk']
        ).order_by('-data_presenca')


class PresencaEstudoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET / PATCH / DELETE de um registo de presença."""
    queryset = PresencaEstudo.objects.all()
    permission_classes = [IsAuthenticated, IsDisciplinarOuSuporte]

    def get_serializer_class(self):
        return PresencaEstudoUpdateSerializer if self.request.method == 'PATCH' else PresencaEstudoSerializer


# ---------------------------------------------------------------------------
# QUARTOS
# ---------------------------------------------------------------------------

class QuartoListCreateView(generics.ListCreateAPIView):
    """Lista quartos com filtros. POST: cria novo quarto."""
    queryset = Quarto.objects.all().order_by('bloco', 'numero')
    serializer_class = QuartoSerializer
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genero_permitido', 'estado', 'bloco']
    search_fields = ['numero', 'bloco']


class QuartoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET / PATCH / DELETE de um quarto."""
    queryset = Quarto.objects.all()
    serializer_class = QuartoSerializer
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.estudantes.filter(estado='Activo').exists():
            return Response(
                {"erro": "Não é possível apagar um quarto com estudantes activos alocados."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


# ---------------------------------------------------------------------------
# PEDIDOS DE SAÍDA
# ---------------------------------------------------------------------------

class AdminPedidoSaidaListView(generics.ListAPIView):
    """Lista pedidos de saída para o admin, filtráveis por estado."""
    serializer_class = PedidoSaidaListAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = PedidoSaida.objects.all().order_by('data_submissao')
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset


class AdminPedidoSaidaDetailView(generics.UpdateAPIView):
    """PATCH: Admin aprova ou rejeita um pedido de saída."""
    queryset = PedidoSaida.objects.all()
    serializer_class = PedidoSaidaUpdateAdminSerializer
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]
 
    def perform_update(self, serializer):
        instance = serializer.save(admin_id_aprovacao=self.request.user)
 
        # Disparar o signal de notificação ao estudante com update_fields correcto
        if 'estado' in serializer.validated_data:
            instance.save(update_fields=['estado'])

class PortariaConfirmarMovimentoView(APIView):
    """PATCH: Regista hora real de saída ou regresso do estudante."""
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]

    def patch(self, request, pk):
        pedido = get_object_or_404(PedidoSaida, pk=pk)
        acao = request.data.get('acao')

        if acao == 'saida':
            if pedido.estado != 'Autorizado':
                return Response(
                    {"erro": "Saída não autorizada. O pedido ainda não foi aprovado por todos."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            pedido.data_saida_real = timezone.now()

        elif acao == 'regresso':
            pedido.data_regresso_real = timezone.now()

        else:
            return Response(
                {"erro": "Acção inválida. Use 'saida' ou 'regresso'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        pedido.save()
        return Response({"status": "Movimento registado com sucesso."})


# ---------------------------------------------------------------------------
# ENCARREGADOS (Admin)
# ---------------------------------------------------------------------------

class AdminEncarregadoListView(generics.ListAPIView):
    """Lista encarregados com pesquisa."""
    queryset = Encarregado.objects.all().order_by('nome_completo')
    serializer_class = EncarregadoAdminSerializer
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome_completo', 'telefone_principal', 'email_contacto']


class AdminEncarregadoDetailView(generics.RetrieveUpdateAPIView):
    """GET / PATCH de um encarregado."""
    queryset = Encarregado.objects.all()
    serializer_class = EncarregadoAdminSerializer
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]


# ---------------------------------------------------------------------------
# DASHBOARD UNIFICADO
# FIX: as 5 views individuais de dashboard foram removidas — este endpoint
# cobre tudo e devolve só os dados relevantes para cada perfil.
# ---------------------------------------------------------------------------

class AdminDashboardView(APIView):
    """
    Dashboard unificado — devolve dados conforme o perfil do utilizador.
    Gestor: dados administrativos.
    Financeiro: dados financeiros.
    Disciplinar: dados disciplinares.
    Suporte: tudo.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        perfil = user.perfil.nome_perfil if user.perfil else None

        if perfil not in ['Gestor', 'Financeiro', 'Disciplinar', 'Suporte']:
            return Response({"erro": "Acesso negado."}, status=status.HTTP_403_FORBIDDEN)

        def admin_data():
            total_vagas = Quarto.objects.aggregate(t=Sum('capacidade_maxima'))['t'] or 0
            total_ocupadas = Quarto.objects.aggregate(t=Sum('ocupacao_atual'))['t'] or 0
            return {
                'total_quartos': Quarto.objects.count(),
                'total_vagas': total_vagas,
                'total_ocupadas': total_ocupadas,
                'vagas_disponiveis': total_vagas - total_ocupadas,
                'total_estudantes_ativos': Estudante.objects.filter(estado='Activo').count(),
                'pedidos_saida_pendentes': PedidoSaida.objects.filter(estado='Pendente').count(),
            }

        def finance_data():
            hoje = timezone.now().date()
            primeiro_dia = hoje.replace(day=1)
            mensalidades_mes = Mensalidade.objects.filter(mes_referencia=primeiro_dia)
            total_arrecadado = mensalidades_mes.filter(estado='Pago').aggregate(
                t=Sum('valor_pago'))['t'] or 0
            pendentes = mensalidades_mes.filter(estado='Pendente')
            # FIX: 'Atraso' calculado correctamente
            atrasados = pendentes.filter(data_vencimento__lt=hoje)
            return {
                'total_arrecadado_mes': total_arrecadado,
                'total_estudantes_pendentes': pendentes.count(),
                'total_estudantes_atraso': atrasados.count(),
                'mes_referencia': primeiro_dia.isoformat(),
            }

        def discipline_data():
            hoje = timezone.now().date()
            primeiro_dia = hoje.replace(day=1)
            top_infratores = list(
                Sancao.objects.filter(data_ocorrencia__gte=primeiro_dia)
                .values('estudante_id', 'estudante__nome_completo')
                .annotate(total=Count('id'))
                .order_by('-total')[:10]
            )
            top_ausentes = list(
                PresencaEstudo.objects.filter(
                    data_presenca__gte=primeiro_dia,
                    estado__in=['Ausente', 'Justificado']
                ).values('estudante_id', 'estudante__nome_completo')
                .annotate(total=Count('id'))
                .order_by('-total')[:10]
            )
            sancao_por_tipo = list(
                Sancao.objects.filter(data_ocorrencia__gte=primeiro_dia)
                .values('tipo_sancao')
                .annotate(total=Count('id'))
                .order_by('-total')
            )
            # FIX: usa estados reais do modelo
            sumario_pedidos = PedidoSaida.objects.filter(
                data_submissao__date__gte=primeiro_dia
            ).aggregate(
                total_pendentes=Count('id', filter=Q(estado='Pendente')),
                total_aguardando=Count('id', filter=Q(estado='Aguardando_Encarregado')),
                total_rejeitados=Count('id', filter=Q(estado='Rejeitado')),
                total_autorizados=Count('id', filter=Q(estado='Autorizado')),
            )
            return {
                'top_infratores': top_infratores,
                'top_ausentes': top_ausentes,
                'sancao_por_tipo': sancao_por_tipo,
                'sumario_pedidos': sumario_pedidos,
            }

        response_data = {}
        if perfil == 'Gestor':
            response_data['administrative'] = admin_data()
        elif perfil == 'Financeiro':
            response_data['finance'] = finance_data()
        elif perfil == 'Disciplinar':
            response_data['discipline'] = discipline_data()
        elif perfil == 'Suporte':
            response_data['administrative'] = admin_data()
            response_data['finance'] = finance_data()
            response_data['discipline'] = discipline_data()

        return Response(response_data, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# EXPORTAÇÃO DE RELATÓRIOS
# FIX: permission_classes corrigido — IsAnyAdminUser em vez de 3 permissões em AND
# ---------------------------------------------------------------------------

class ExportarRelatorioView(APIView):
    # FIX: antes tinha [IsGestorOuSuporte, IsFinanceiroOuSuporte, IsDisciplinarOuSuporte]
    # que em DRF é AND — impossível satisfazer. Agora usa IsAnyAdminUser (OR).
    permission_classes = [IsAuthenticated, IsAnyAdminUser]

    def get(self, request):
        tipo = request.query_params.get('tipo')
        formato = request.query_params.get('formato', 'xlsx')
        inicio = request.query_params.get('periodo_inicio')
        fim = request.query_params.get('periodo_fim')

        if not tipo:
            return Response({"erro": "Parâmetro 'tipo' é obrigatório."}, status=400)

        handlers = {
            'financeiro': self._get_dados_financeiros,
            'disciplinar': self._get_dados_disciplinares,
            'ocupacao': self._get_dados_ocupacao,
            'pedidos': self._get_dados_pedidos,
            'completo': self._get_dados_completos,
        }

        if tipo not in handlers:
            return Response({"erro": f"Tipo inválido. Opções: {', '.join(handlers.keys())}"}, status=400)

        dados = handlers[tipo](inicio, fim)

        if formato == 'xlsx':
            return self._gerar_excel(dados, tipo)
        elif formato == 'pdf':
            return self._gerar_pdf(dados, tipo)
        else:
            return Response({"erro": "Formato inválido. Use 'xlsx' ou 'pdf'."}, status=400)

    def _get_dados_financeiros(self, inicio, fim):
        qs = Mensalidade.objects.all()
        if inicio:
            qs = qs.filter(mes_referencia__gte=inicio)
        if fim:
            qs = qs.filter(mes_referencia__lte=fim)
        return pd.DataFrame(list(qs.values(
            'estudante__nome_completo',
            'mes_referencia', 'valor_pago', 'estado', 'metodo_pagamento'
        )))

    def _get_dados_disciplinares(self, inicio, fim):
        sancao_qs = Sancao.objects.all()
        if inicio:
            sancao_qs = sancao_qs.filter(data_ocorrencia__gte=inicio)
        if fim:
            sancao_qs = sancao_qs.filter(data_ocorrencia__lte=fim)
        sancao_df = pd.DataFrame(list(sancao_qs.values(
            'estudante__nome_completo',
            'data_ocorrencia', 'tipo_sancao', 'descricao'
        )))
        presenca_qs = PresencaEstudo.objects.all()
        if inicio:
            presenca_qs = presenca_qs.filter(data_presenca__gte=inicio)
        if fim:
            presenca_qs = presenca_qs.filter(data_presenca__lte=fim)
        presenca_df = pd.DataFrame(list(presenca_qs.values(
            'estudante__nome_completo',
            'data_presenca', 'estado'
        )))
        return {'sancoes': sancao_df, 'presencas': presenca_df}

    def _get_dados_ocupacao(self, inicio, fim):
        return pd.DataFrame(list(Quarto.objects.all().values(
            'numero', 'bloco', 'capacidade_maxima', 'ocupacao_atual',
            'genero_permitido', 'estado'
        )))

    def _get_dados_pedidos(self, inicio, fim):
        qs = PedidoSaida.objects.all()
        if inicio:
            qs = qs.filter(data_submissao__gte=inicio)
        if fim:
            qs = qs.filter(data_submissao__lte=fim)
        return pd.DataFrame(list(qs.values(
            'estudante__nome_completo',
            'data_submissao', 'data_saida_pretendida', 'data_retorno_pretendida',
            'estado', 'motivo'
        )))

    def _get_dados_completos(self, inicio, fim):
        return {
            'financeiro': self._get_dados_financeiros(inicio, fim),
            'disciplinar': self._get_dados_disciplinares(inicio, fim),
            'pedidos': self._get_dados_pedidos(inicio, fim),
        }

    def _gerar_excel(self, dados, tipo):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            if tipo == 'completo':
                dados['financeiro'].to_excel(writer, sheet_name='Mensalidades', index=False)
                dados['disciplinar']['sancoes'].to_excel(writer, sheet_name='Sanções', index=False)
                dados['disciplinar']['presencas'].to_excel(writer, sheet_name='Presenças', index=False)
                dados['pedidos'].to_excel(writer, sheet_name='Pedidos de Saída', index=False)
            elif tipo == 'disciplinar':
                dados['sancoes'].to_excel(writer, sheet_name='Sanções', index=False)
                dados['presencas'].to_excel(writer, sheet_name='Presenças', index=False)
            else:
                dados.to_excel(writer, sheet_name=tipo.capitalize(), index=False)
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = (
            f'attachment; filename="relatorio_{tipo}_{timezone.now().strftime("%Y%m%d")}.xlsx"'
        )
        return response

    def _gerar_pdf(self, dados, tipo):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            f'attachment; filename="relatorio_{tipo}_{timezone.now().strftime("%Y%m%d")}.pdf"'
        )
        doc = SimpleDocTemplate(response, pagesize=A4)
        styles = getSampleStyleSheet()
        story = [
            Paragraph(f"Relatório — {tipo.capitalize()}", styles['Title']),
            Spacer(1, 0.5 * cm),
            Paragraph(f"Gerado em {timezone.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']),
            Spacer(1, 1 * cm),
        ]

        def adicionar_tabela(titulo, df):
            if df is None or df.empty:
                story.append(Paragraph(f"{titulo}: Sem dados", styles['Normal']))
            else:
                story.append(Paragraph(titulo, styles['Heading2']))
                data = [df.columns.tolist()] + df.fillna('').values.tolist()
                t = Table(data)
                t.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                ]))
                story.append(t)
            story.append(Spacer(1, 0.5 * cm))

        if tipo == 'completo':
            adicionar_tabela("Mensalidades", dados['financeiro'])
            adicionar_tabela("Sanções", dados['disciplinar']['sancoes'])
            adicionar_tabela("Presenças", dados['disciplinar']['presencas'])
            adicionar_tabela("Pedidos de Saída", dados['pedidos'])
        elif tipo == 'disciplinar':
            adicionar_tabela("Sanções", dados['sancoes'])
            adicionar_tabela("Presenças", dados['presencas'])
        else:
            adicionar_tabela(tipo.capitalize(), dados)

        doc.build(story)
        return response


# ---------------------------------------------------------------------------
# PERFIL DO ESTUDANTE (endpoints do próprio estudante autenticado)
# ---------------------------------------------------------------------------

class PerfilEstudanteDetailView(generics.RetrieveAPIView):
    """Estudante vê o seu próprio perfil."""
    serializer_class = EstudantePerfilSerializer
    permission_classes = [IsAuthenticated, IsEstudanteUser]

    def get_object(self):
        return get_object_or_404(Estudante, pk=self.request.user.id)


class PedidoSaidaListCreateView(generics.ListCreateAPIView):
    """Estudante lista e cria os seus pedidos de saída."""
    serializer_class = PedidoSaidaSerializer
    permission_classes = [IsAuthenticated, IsEstudanteUser]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return PedidoSaida.objects.filter(
            estudante_id=self.request.user.id
        ).order_by('-data_submissao')

    def perform_create(self, serializer):
        estudante = get_object_or_404(Estudante, pk=self.request.user.id)
        serializer.save(estudante=estudante)


class PerfilPedidoSaidaDetailView(generics.RetrieveAPIView):
    """Estudante vê um pedido de saída específico seu."""
    queryset = PedidoSaida.objects.all()
    serializer_class = PedidoSaidaSerializer
    permission_classes = [IsAuthenticated, IsEstudanteUser, IsOwnerOfPedidoSaida]


class PerfilMensalidadeListView(generics.ListAPIView):
    """Estudante vê o seu histórico financeiro."""
    serializer_class = MensalidadeSerializer
    permission_classes = [IsAuthenticated, IsEstudanteUser]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Mensalidade.objects.filter(
            estudante_id=self.request.user.id
        ).order_by('-mes_referencia')


class PerfilSancaoListView(generics.ListAPIView):
    """Estudante vê o seu histórico disciplinar."""
    serializer_class = SancaoSerializer
    permission_classes = [IsAuthenticated, IsEstudanteUser]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Sancao.objects.filter(
            estudante_id=self.request.user.id
        ).order_by('-data_ocorrencia')


class PerfilPresencaListView(generics.ListAPIView):
    """Estudante vê o seu histórico de presenças."""
    serializer_class = PresencaEstudoSerializer
    permission_classes = [IsAuthenticated, IsEstudanteUser]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return PresencaEstudo.objects.filter(
            estudante_id=self.request.user.id
        ).order_by('-data_presenca')


# ---------------------------------------------------------------------------
# PERFIL DO ENCARREGADO (endpoints do próprio encarregado autenticado)
# ---------------------------------------------------------------------------

class EncarregadoEducandosListView(generics.ListAPIView):
    """Encarregado lista os seus educandos."""
    serializer_class = EstudanteListSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]

    def get_queryset(self):
        return Estudante.objects.filter(
            encarregado=self.request.user.encarregado, estado='Activo'
        )


class EncarregadoEducandoDetailView(generics.RetrieveAPIView):
    """Encarregado vê os dados de um educando específico seu."""
    serializer_class = EstudanteListSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]

    def get_queryset(self):
        return Estudante.objects.filter(encarregado=self.request.user.encarregado)


class EncarregadoMensalidadeListView(generics.ListAPIView):
    """Encarregado vê o histórico financeiro dos seus educandos."""
    serializer_class = MensalidadeSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estudante', 'estado', 'mes_referencia']

    def get_queryset(self):
        ids = Estudante.objects.filter(
            encarregado=self.request.user.encarregado
        ).values_list('pk', flat=True)
        return Mensalidade.objects.filter(estudante_id__in=ids).order_by('-mes_referencia')


class EncarregadoFinanceiroStatsView(APIView):
    """Resumo financeiro dos educandos do encarregado."""
    permission_classes = [IsAuthenticated, IsEncarregadoUser]

    def get(self, request):
        estudantes = Estudante.objects.filter(encarregado=request.user.encarregado)
        mensalidades = Mensalidade.objects.filter(estudante__in=estudantes)
        hoje = timezone.now().date()

        total_pago = mensalidades.filter(estado='Pago').aggregate(
            s=Sum('valor_pago'))['s'] or 0
        faturas_pendentes = mensalidades.filter(estado='Pendente').count()
        # FIX: 'Atraso' calculado correctamente — não é estado persistido
        faturas_atraso = mensalidades.filter(
            estado='Pendente', data_vencimento__lt=hoje
        ).count()

        return Response({
            "total_pago": total_pago,
            "faturas_pendentes": faturas_pendentes,
            "faturas_atraso": faturas_atraso,
            "moeda": "MZN",
        })


class EncarregadoSancaoListView(generics.ListAPIView):
    """Encarregado vê as sanções dos seus educandos."""
    serializer_class = SancaoSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['estudante', 'tipo_sancao']
    ordering = ['-data_ocorrencia']

    def get_queryset(self):
        ids = Estudante.objects.filter(
            encarregado=self.request.user.encarregado
        ).values_list('pk', flat=True)
        return Sancao.objects.filter(estudante_id__in=ids)


class EncarregadoPresencaListView(generics.ListAPIView):
    """Encarregado vê o histórico de presenças dos seus educandos."""
    serializer_class = PresencaEstudoSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['estudante', 'estado', 'data_presenca']
    ordering = ['-data_presenca']

    def get_queryset(self):
        ids = Estudante.objects.filter(
            encarregado=self.request.user.encarregado
        ).values_list('pk', flat=True)
        return PresencaEstudo.objects.filter(estudante_id__in=ids)


class EncarregadoPedidoSaidaListView(generics.ListAPIView):
    """Encarregado vê os pedidos de saída dos seus educandos."""
    serializer_class = PedidoSaidaListAdminSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['estudante', 'estado']
    ordering = ['-data_submissao']

    def get_queryset(self):
        ids = Estudante.objects.filter(
            encarregado=self.request.user.encarregado
        ).values_list('pk', flat=True)
        return PedidoSaida.objects.filter(estudante_id__in=ids)


class EncarregadoPedidoSaidaDetailView(generics.UpdateAPIView):
    """Encarregado aprova ou rejeita um pedido de saída."""
    serializer_class = PedidoSaidaEncarregadoUpdateSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]
 
    def get_queryset(self):
        ids = Estudante.objects.filter(
            encarregado=self.request.user.encarregado
        ).values_list('pk', flat=True)
        return PedidoSaida.objects.filter(estudante_id__in=ids)
 
    def perform_update(self, serializer):
        from rest_framework import serializers as drf_serializers
        pedido = self.get_object()
        if pedido.estado != 'Aguardando_Encarregado':
            raise drf_serializers.ValidationError(
                {"erro": "Só pode agir sobre pedidos que aguardam a sua aprovação."}
            )
        instance = serializer.save(data_aprovacao_encarregado=timezone.now())
 
        # Disparar signal com update_fields para notificar o estudante
        if 'estado' in serializer.validated_data:
            instance.save(update_fields=['estado', 'data_aprovacao_encarregado'])
 

class EncarregadoProfileView(generics.RetrieveUpdateAPIView):
    """Encarregado vê e actualiza os seus contactos."""
    serializer_class = EncarregadoProfileUpdateSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]

    def get_object(self):
        return self.request.user.encarregado


# ---------------------------------------------------------------------------
# UTILITÁRIOS
# ---------------------------------------------------------------------------

class OpcoesView(APIView):
    """Devolve todos os CHOICES dos modelos para o frontend construir dropdowns."""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        def fmt(choices):
            return [{'value': c[0], 'label': c[1]} for c in choices]

        return Response({
            'perfis': fmt(Perfil.NOME_CHOICES),
            'estudante_estados': fmt(Estudante.ESTADO_CHOICES),
            'mensalidade_metodos': fmt(Mensalidade.METODO_CHOICES),
            'mensalidade_estados': fmt(Mensalidade.ESTADO_CHOICES),
            'presenca_estados': fmt(PresencaEstudo.ESTADO_CHOICES),
            'sancao_tipos': fmt(Sancao.TIPO_SANCAO_CHOICES),
            'pedido_saida_estados': fmt(PedidoSaida.ESTADO_CHOICES),
            'quarto_estados': fmt(Quarto.ESTADO_CHOICES),
            'generos': fmt(Estudante.GENERO_CHOICES),
        }, status=status.HTTP_200_OK)