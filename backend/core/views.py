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
from datetime import date
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
    TransferirQuartoSerializer,CustomTokenObtainPairSerializer, CriarUtilizadorStaffSerializer,UserListAdminSerializer,UserUpdateAdminSerializer,
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


from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from django.http import HttpResponse
from .utils import gerar_numero_recibo
import io
import pandas as pd
from rest_framework_simplejwt.views import TokenObtainPairView


MESES_PT = {
    1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
    7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez',
}

# ---------------------------------------------------------------------------
# PAGINAÇÃO PADRÃO
# ---------------------------------------------------------------------------

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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
# views.py - RegistoCompletoView

# core/views.py

class RegistoCompletoView(generics.CreateAPIView):
    serializer_class = RegistoCompletoSerializer
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("ERROS:", serializer.errors)  # ← adiciona isto
            return Response(serializer.errors, status=400)

        serializer.is_valid(raise_exception=True)
        dados = serializer.validated_data
        dados_est = dados['estudante']
        dados_enc = dados.get('encarregado')
        criar_usuario = dados.get('criar_usuario_encarregado', False)

        User = get_user_model()
        SENHA_PADRAO = "mudar1234"

        try:
            perfil_est = Perfil.objects.get(nome_perfil='Estudante')
            encarregado_obj = None

            with transaction.atomic():
                quarto = dados_est['quarto']
                if dados_est['genero'] != quarto.genero_permitido:
                    return Response(
                        {"erro": "Género não compatível com o quarto."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if quarto.vagas_disponiveis <= 0:
                    return Response(
                        {"erro": "Quarto sem vagas."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Cria encarregado (sempre)
                encarregado_obj = Encarregado.objects.create(
                    nome_completo=dados_enc.get('nome_completo', ''),
                    telefone_principal=dados_enc.get('telefone_principal', ''),
                    email=dados_enc.get('email', ''),
                    parentesco=dados_enc.get('parentesco', None),
                    telefone_alternativo=dados_enc.get('telefone_alternativo', None),
                    bi=dados_enc.get('bi', None),
                    morada=dados_enc.get('morada', None),
                    profissao=dados_enc.get('profissao', None),  # NOVO
                )

                # Cria utilizador para o encarregado se solicitado e telefone fornecido
                if criar_usuario and dados_enc.get('telefone_principal'):
                    perfil_enc = Perfil.objects.get(nome_perfil='Encarregado')
                    user_enc = User.objects.create_user(
                        email=dados_enc.get('email', ''),
                        password=SENHA_PADRAO,
                        first_name=dados_enc['nome_completo'],
                        telefone=dados_enc['telefone_principal']   # <-- telefone como identificador
                    )
                    user_enc.perfis.set([perfil_enc])
                    encarregado_obj.utilizador = user_enc
                    encarregado_obj.save(update_fields=['utilizador'])

                # Gera email para o estudante se não fornecido (opcional)
                email_estudante = dados_est.get('email', '')

                # Cria o utilizador do estudante (código gerado automaticamente)
                user_est = User.objects.create_user(
                    email=email_estudante,
                    password=SENHA_PADRAO,
                    first_name=dados_est['nome_completo'],
                    # não passamos telefone nem código – o manager gera código
                )
                user_est.perfis.set([perfil_est])

                estudante = Estudante.objects.create(
                    utilizador=user_est,
                    encarregado=encarregado_obj,
                    nome_completo=dados_est['nome_completo'],
                    genero=dados_est['genero'],
                    quarto=quarto,
                    curso=dados_est['curso'],
                    data_nascimento=dados_est.get('data_nascimento', None),
                    bi=dados_est.get('bi', None),
                    telefone_pessoal=dados_est.get('telefone_pessoal', None),
                    email_pessoal=dados_est.get('email_pessoal', None),
                    morada=dados_est.get('morada', None),
                    nome_mae=dados_est.get('nome_mae', None),
                    nome_pai=dados_est.get('nome_pai', None),
                    # NOVOS CAMPOS
                    nuit=dados_est.get('nuit', None),
                    ano_lectivo=dados_est.get('ano_lectivo', '2025/2026'),
                    nacionalidade=dados_est.get('nacionalidade', 'Moçambicana'),
                    condicao_saude=dados_est.get('condicao_saude', None),
                )

            return Response({
                "status": "sucesso",
                "estudante_id": estudante.utilizador_id,
                "codigo_acesso": user_est.codigo_acesso,   # <-- retorna o código gerado
            }, status=status.HTTP_201_CREATED)

        except Perfil.DoesNotExist:
            return Response(
                {"erro": "Perfil 'Estudante' ou 'Encarregado' não encontrado."},
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
            Mensalidade.objects.create(
                estudante=estudante,
                admin_id_registo=request.user,
                mes_referencia=timezone.now().date().replace(day=1),
                valor_pago=2700.00,
                estado='Pendente',
                tipo='Inscrição',
                data_vencimento=None  # será calculada automaticamente no save()
            )
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
    permission_classes = [IsAuthenticated, IsFinanceiroOuSuporte]

    def post(self, request):
        serializer = GerarMensalidadesLoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ano = serializer.validated_data['ano']
        valor = serializer.validated_data.get('valor_padrao', 2500.00)

        estudantes_ativos = Estudante.objects.filter(estado='Activo')
        total_estudantes = estudantes_ativos.count()
        criados = 0
        ignorados = 0

        with transaction.atomic():
            for estudante in estudantes_ativos:
                # Data de entrada do estudante (usando a data de criação do utilizador)
                data_entrada = estudante.utilizador.date_joined.date()
                mes_inicio = data_entrada.month
                ano_inicio = data_entrada.year

                # Ajustar mês inicial conforme o ano alvo
                if ano_inicio < ano:
                    mes_inicio = 1  # entrou antes do ano alvo → começa em Janeiro
                elif ano_inicio == ano:
                    mes_inicio = data_entrada.month  # entrou neste ano → começa no mês de entrada
                else:
                    # Se entrou depois do ano alvo (não deveria acontecer com activos), saltar
                    continue

                # Gerar mensalidades de mes_inicio até Dezembro do ano alvo
                for mes in range(mes_inicio, 13):
                    mes_referencia = date(ano, mes, 1)
                    _, created = Mensalidade.objects.get_or_create(
                        estudante=estudante,
                        mes_referencia=mes_referencia,
                        defaults={
                            'estado': 'Pendente',
                            'valor_pago': valor,
                            'admin_id_registo': request.user,
                            'tipo': 'Mensalidade'
                        }
                    )
                    if created:
                        criados += 1
                    else:
                        ignorados += 1

        return Response({
            "mensagem": f"Processamento anual concluído para {ano}.",
            "total_estudantes": total_estudantes,
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
            ["Bloco:", estudante.quarto.bloco if estudante.quarto else "Não atribuído"],
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
        periodo = data.get('periodo', 'Manhã')      # NOVO
        bloco = data.get('bloco')                   # NOVO
        admin_logado = request.user

        ids_ausentes = set(data.get('ausentes_ids', []))
        ids_justificados = set(data.get('justificados_ids', []))

        # Filtro por bloco (se informado)
        todos_ativos = Estudante.objects.filter(estado='Activo')
        if bloco:
            todos_ativos = todos_ativos.filter(quarto__bloco=bloco)

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
                periodo=periodo,                     # NOVO
            ))

        try:
            with transaction.atomic():
                PresencaEstudo.objects.bulk_create(presencas)
        except Exception as e:
            return Response(
                {"erro": f"Já existem presenças registadas para este dia/período? Detalhe: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"status": f"{len(presencas)} presenças registadas para {data_presenca} ({periodo})."},
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

class PresencaListView(generics.ListAPIView):
    queryset = PresencaEstudo.objects.all()
    serializer_class = PresencaEstudoSerializer
    permission_classes = [IsAuthenticated, IsDisciplinarOuSuporte]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['data_presenca', 'estudante']
# ---------------------------------------------------------------------------
# QUARTOS
# ---------------------------------------------------------------------------

class QuartoListCreateView(generics.ListCreateAPIView):
    """Lista quartos com filtros. POST: cria novo quarto."""
    queryset = Quarto.objects.all().order_by('bloco')
    serializer_class = QuartoSerializer
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genero_permitido', 'estado', 'bloco']
    search_fields = ['bloco']


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
    filterset_fields = ['estado', 'estudante']  # adicionar 'estudante'

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
        perfis_user = set(user.perfis.values_list('nome_perfil', flat=True))

        if not perfis_user & {'Gestor', 'Financeiro', 'Disciplinar', 'Suporte'}:
            return Response({"erro": "Acesso negado."}, status=status.HTTP_403_FORBIDDEN)

        def admin_data():
            total_vagas = Quarto.objects.aggregate(t=Sum('capacidade_maxima'))['t'] or 0
            total_ocupadas = Quarto.objects.aggregate(t=Sum('ocupacao_atual'))['t'] or 0
            total_masculino = Estudante.objects.filter(estado='Activo', genero='M').count()
            total_feminino = Estudante.objects.filter(estado='Activo', genero='F').count()
            return {
                'total_quartos': Quarto.objects.count(),
                'total_vagas': total_vagas,
                'total_ocupadas': total_ocupadas,
                'vagas_disponiveis': total_vagas - total_ocupadas,
                'total_estudantes_ativos': Estudante.objects.filter(estado='Activo').count(),
                'pedidos_saida_pendentes': PedidoSaida.objects.filter(estado='Pendente').count(),
                'total_masculino': total_masculino,
                'total_feminino': total_feminino,
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
            sumario_pedidos = PedidoSaida.objects.aggregate(
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
        if perfis_user & {'Gestor', 'Suporte'}:
            response_data['administrative'] = admin_data()
        if perfis_user & {'Financeiro', 'Suporte'}:
            response_data['finance'] = finance_data()
        if perfis_user & {'Disciplinar', 'Gestor', 'Suporte'}:  # Gestor precisa do sumário de pedidos
            response_data['discipline'] = discipline_data()

        return Response(response_data, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# EXPORTAÇÃO DE RELATÓRIOS
# FIX: permission_classes corrigido — IsAnyAdminUser em vez de 3 permissões em AND
# ---------------------------------------------------------------------------
class ExportarRelatorioView(APIView):
    permission_classes = [IsAuthenticated, IsAnyAdminUser]

    def get(self, request):
        inicio = request.query_params.get('periodo_inicio')
        fim = request.query_params.get('periodo_fim')

        perfis_user = set(request.user.perfis.values_list('nome_perfil', flat=True))

        # DEBUG temporário — remover depois de confirmar
        # return Response({"perfis_detectados": list(perfis_user)})

        perfis_validos = {'Gestor', 'Financeiro', 'Disciplinar', 'Suporte'}
        if not perfis_user & perfis_validos:
            return Response({"erro": "Sem permissão para relatórios."}, status=403)

        dados_completos = self._get_dados_completos(inicio, fim)
        secoes = []

        # Mensalidades — apenas Financeiro ou Suporte
        if perfis_user & {'Financeiro', 'Suporte'}:
            secoes.append(('Mensalidades', 'pivot', dados_completos['financeiro']))

        # Disciplinar — apenas Disciplinar ou Suporte (Gestor NÃO incluído aqui)
        if perfis_user & {'Disciplinar', 'Suporte'}:
            secoes.append(('Sanções', 'generica', dados_completos['disciplinar']['sancoes']))
            secoes.append(('Presenças', 'generica', dados_completos['disciplinar']['presencas']))

        # Pedidos — Gestor ou Suporte
        if perfis_user & {'Gestor', 'Suporte'}:
            secoes.append(('Pedidos de Saída', 'generica', dados_completos['pedidos']))

        if not secoes:
            return Response({"erro": "Nenhuma secção disponível para os seus perfis."}, status=400)

        # ✅ Devolve também os perfis usados para auditoria (opcional)
        # response['X-Perfis-Usados'] = ','.join(perfis_user & perfis_validos)

        return self._gerar_pdf(secoes)
    # ---------------------- Funções de consulta (mantidas) ----------------------
    def _get_dados_financeiros(self, inicio, fim):
        qs = Mensalidade.objects.filter(estudante__estado='Activo')
        if inicio:
            qs = qs.filter(mes_referencia__gte=inicio)
        if fim:
            qs = qs.filter(mes_referencia__lte=fim)
        return pd.DataFrame(list(qs.values(
            'estudante__nome_completo', 'mes_referencia', 'valor_pago', 'estado'
        )))

    def _get_dados_disciplinares(self, inicio, fim):
        sancao_qs = Sancao.objects.all()
        if inicio:
            sancao_qs = sancao_qs.filter(data_ocorrencia__gte=inicio)
        if fim:
            sancao_qs = sancao_qs.filter(data_ocorrencia__lte=fim)
        sancao_df = pd.DataFrame(list(sancao_qs.values(
            'estudante__nome_completo', 'data_ocorrencia', 'tipo_sancao', 'descricao'
        )))
        presenca_qs = PresencaEstudo.objects.all()
        if inicio:
            presenca_qs = presenca_qs.filter(data_presenca__gte=inicio)
        if fim:
            presenca_qs = presenca_qs.filter(data_presenca__lte=fim)
        presenca_df = pd.DataFrame(list(presenca_qs.values(
            'estudante__nome_completo', 'data_presenca', 'estado'
        )))
        return {'sancoes': sancao_df, 'presencas': presenca_df}

    def _get_dados_pedidos(self, inicio, fim):
        qs = PedidoSaida.objects.all()
        if inicio:
            qs = qs.filter(data_submissao__gte=inicio)
        if fim:
            qs = qs.filter(data_submissao__lte=fim)
        return pd.DataFrame(list(qs.values(
            'estudante__nome_completo', 'data_submissao', 'data_saida_pretendida',
            'data_retorno_pretendida', 'estado', 'motivo'
        )))

    def _get_dados_ocupacao(self, inicio, fim):
        # (se quiser incluir ocupação)
        return pd.DataFrame(list(Quarto.objects.all().values(
            'bloco', 'capacidade_maxima', 'ocupacao_atual', 'genero_permitido', 'estado'
        )))

    def _get_dados_completos(self, inicio, fim):
        return {
            'financeiro': self._get_dados_financeiros(inicio, fim),
            'disciplinar': self._get_dados_disciplinares(inicio, fim),
            'pedidos': self._get_dados_pedidos(inicio, fim),
            # 'ocupacao': self._get_dados_ocupacao(inicio, fim),
        }

    # ---------------------- Funções auxiliares do PDF ----------------------
    def _mes_label(self, data):
        return f"{MESES_PT[data.month]}/{data.year % 100:02d}"

    def _pivotar_financeiro(self, df):
        alunos_ativos = list(
            Estudante.objects.filter(estado='Activo')
            .order_by('nome_completo')
            .values_list('nome_completo', flat=True)
        )
        if df is None or df.empty:
            return pd.DataFrame({'Aluno': alunos_ativos})
        df = df.copy()
        df['mes_referencia'] = pd.to_datetime(df['mes_referencia'])
        df['mes_label'] = df['mes_referencia'].apply(self._mes_label)
        df['valor_exibido'] = df.apply(
            lambda r: r['valor_pago'] if r['estado'] == 'Pago' else None, axis=1
        )
        colunas_ordenadas = (
            df[['mes_referencia', 'mes_label']]
            .drop_duplicates()
            .sort_values('mes_referencia')['mes_label']
            .tolist()
        )
        pivot = df.pivot_table(
            index='estudante__nome_completo',
            columns='mes_label',
            values='valor_exibido',
            aggfunc='sum',
        )
        pivot = pivot.reindex(index=alunos_ativos, columns=colunas_ordenadas)
        pivot = pivot.reset_index().rename(columns={'estudante__nome_completo': 'Aluno'})
        return pivot

    def _gerar_pdf(self, secoes):
        """
        Gera o PDF a partir de uma lista de secções.
        Cada secção: (titulo, modo, df)
        """
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            f'attachment; filename="relatorio_{timezone.now().strftime("%Y%m%d_%H%M")}.pdf"'
        )

        doc = SimpleDocTemplate(
            response,
            pagesize=landscape(A4),
            leftMargin=1.2 * cm,
            rightMargin=1.2 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
        )

        styles = getSampleStyleSheet()
        titulo_estilo = ParagraphStyle(
            'TituloRelatorio', parent=styles['Title'], fontSize=16,
            textColor=colors.HexColor('#1a365d'), alignment=1, spaceAfter=8,
        )
        subtitulo_estilo = ParagraphStyle(
            'SubtituloRelatorio', parent=styles['Heading2'], fontSize=13,
            textColor=colors.HexColor('#2d3748'), alignment=1, spaceAfter=4,
        )
        cabecalho_tabela = ParagraphStyle(
            'CabecalhoTabela', parent=styles['Heading4'], fontSize=9,
            textColor=colors.white, alignment=1, fontName='Helvetica-Bold',
        )
        celula_normal = ParagraphStyle('CelulaNormal', parent=styles['Normal'], fontSize=8, alignment=0)
        celula_direita = ParagraphStyle('CelulaDireita', parent=styles['Normal'], fontSize=8, alignment=2)
        celula_centro = ParagraphStyle('CelulaCentro', parent=styles['Normal'], fontSize=8, alignment=1)

        story = []

        def cabecalho_secao(titulo_secao):
            story.append(Paragraph("INSTITUTO INDUSTRIAL E COMERCIAL DA BEIRA", titulo_estilo))
            story.append(Paragraph(f"RELATÓRIO — {titulo_secao.upper()}", subtitulo_estilo))
            story.append(Paragraph(f"Gerado em {timezone.now().strftime('%d/%m/%Y às %H:%M')}", styles['Normal']))
            story.append(Spacer(1, 0.6 * cm))

        def estilo_zebra(base, total_linhas):
            for i in range(1, total_linhas):
                cor = '#edf2f7' if i % 2 == 0 else '#f7fafc'
                base.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor(cor)))
            return base

        def tabela_financeiro_pivot(df_financeiro):
            pivot = self._pivotar_financeiro(df_financeiro)
            if pivot.empty or len(pivot.columns) <= 1:
                story.append(Paragraph("Mensalidades: Sem dados para o período seleccionado.", styles['Normal']))
                return

            colunas = pivot.columns.tolist()
            linhas = [[Paragraph(c, cabecalho_tabela) for c in colunas]]

            for _, row in pivot.iterrows():
                linha = [Paragraph(str(row['Aluno']), celula_normal)]
                for col in colunas[1:]:
                    valor = row[col]
                    if valor is None or pd.isna(valor):
                        linha.append(Paragraph('—', celula_centro))
                    else:
                        texto = f"{valor:,.0f}".replace(',', ' ')
                        linha.append(Paragraph(texto, celula_direita))
                linhas.append(linha)

            largura_aluno = 5 * cm
            largura_mes = (doc.width - largura_aluno) / max(len(colunas) - 1, 1)
            col_widths = [largura_aluno] + [largura_mes] * (len(colunas) - 1)

            t = Table(linhas, colWidths=col_widths, repeatRows=1)
            estilo = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]
            t.setStyle(TableStyle(estilo_zebra(estilo, len(linhas))))
            story.append(t)
            story.append(Spacer(1, 0.4 * cm))
            story.append(Paragraph(
                "<font size=8 color='#718096'>Valores em Meticais (MZN). "
                "Células em branco indicam mês pendente ou em atraso.</font>",
                styles['Normal'],
            ))

        def tabela_generica(titulo, df):
            if df is None or df.empty:
                story.append(Paragraph(f"{titulo}: Sem dados", styles['Normal']))
                return

            cabecalhos = df.columns.tolist()
            linhas = [[Paragraph(col.replace('_', ' ').title(), cabecalho_tabela) for col in cabecalhos]]

            for _, row in df.iterrows():
                linha = []
                for col in cabecalhos:
                    valor = row[col]
                    eh_valor = 'valor' in col.lower() or 'pago' in col.lower()
                    if valor is None or pd.isna(valor):
                        texto = ''
                    elif isinstance(valor, (int, float)):
                        texto = f"{valor:,.2f} MZN".replace(',', ' ') if eh_valor else str(valor)
                    elif isinstance(valor, pd.Timestamp):
                        texto = valor.strftime('%d/%m/%Y')
                    else:
                        texto = str(valor)
                    linha.append(Paragraph(texto, celula_direita if eh_valor else celula_normal))
                linhas.append(linha)

            col_widths = [doc.width / len(cabecalhos)] * len(cabecalhos)
            t = Table(linhas, colWidths=col_widths, repeatRows=1)
            estilo = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]
            t.setStyle(TableStyle(estilo_zebra(estilo, len(linhas))))
            story.append(t)

        # Percorre as secções e gera as respectivas tabelas
        for i, (titulo_secao, modo, df) in enumerate(secoes):
            if i > 0:
                story.append(PageBreak())
            cabecalho_secao(titulo_secao)
            if modo == 'pivot':
                tabela_financeiro_pivot(df)
            else:
                tabela_generica(titulo_secao, df)

        story.append(Spacer(1, 1 * cm))
        story.append(Paragraph(
            "<font size=8 color='#718096'>Documento gerado automaticamente pelo SGI - IICB Beira</font>",
            styles['Normal'],
        ))

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
            encarregado=self.request.user.encarregado_profile, estado='Activo'
        )


class EncarregadoEducandoDetailView(generics.RetrieveAPIView):
    """Encarregado vê os dados de um educando específico seu."""
    serializer_class = EstudanteListSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]

    def get_queryset(self):
        return Estudante.objects.filter(encarregado=self.request.user.encarregado_profile)


class EncarregadoMensalidadeListView(generics.ListAPIView):
    """Encarregado vê o histórico financeiro dos seus educandos."""
    serializer_class = MensalidadeSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estudante', 'estado', 'mes_referencia']

    def get_queryset(self):
        ids = Estudante.objects.filter(
            encarregado=self.request.user.encarregado_profile
        ).values_list('pk', flat=True)
        return Mensalidade.objects.filter(estudante_id__in=ids).order_by('-mes_referencia')


class EncarregadoFinanceiroStatsView(APIView):
    """Resumo financeiro dos educandos do encarregado."""
    permission_classes = [IsAuthenticated, IsEncarregadoUser]

    def get(self, request):
        estudantes = Estudante.objects.filter(encarregado=request.user.encarregado_profile)
        mensalidades = Mensalidade.objects.filter(estudante__in=estudantes)
        hoje = timezone.now().date()

        total_pago = mensalidades.filter(estado='Pago').aggregate(s=Sum('valor_pago'))['s'] or 0

        pendentes = mensalidades.filter(estado='Pendente')
        faturas_pendentes = pendentes.count()
        faturas_atraso = pendentes.filter(data_vencimento__lt=hoje).count()
        faturas_em_dia = faturas_pendentes - faturas_atraso

        return Response({
            "total_pago": total_pago,
            "faturas_pendentes": faturas_pendentes,          # total de pendentes
            "faturas_em_dia": faturas_em_dia,                # pendentes não vencidas
            "faturas_atraso": faturas_atraso,                # pendentes vencidas
            "moeda": "MZN",
        })


class EncarregadoSancaoListView(generics.ListAPIView):
    serializer_class = SancaoSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['estudante', 'tipo_sancao']
    ordering = ['-data_ocorrencia']

    def get_queryset(self):
        ids = Estudante.objects.filter(
            encarregado=self.request.user.encarregado_profile
        ).values_list('pk', flat=True)
        return Sancao.objects.filter(
            estudante_id__in=ids,
            notificado_encarregado=True  # <-- FILTRO
        )

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
            encarregado=self.request.user.encarregado_profile
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
            encarregado=self.request.user.encarregado_profile
        ).values_list('pk', flat=True)
        return PedidoSaida.objects.filter(estudante_id__in=ids)


class EncarregadoPedidoSaidaDetailView(generics.UpdateAPIView):
    """Encarregado aprova ou rejeita um pedido de saída."""
    serializer_class = PedidoSaidaEncarregadoUpdateSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]
 
    def get_queryset(self):
        ids = Estudante.objects.filter(
            encarregado=self.request.user.encarregado_profile
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
        return self.request.user.encarregado_profile


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
            'mensalidade_tipos': fmt(Mensalidade.TIPO_CHOICES),          # NOVO
            'presenca_estados': fmt(PresencaEstudo.ESTADO_CHOICES),
            'presenca_periodos': fmt(PresencaEstudo.PERIODO_CHOICES),    # NOVO
            'sancao_tipos': fmt(Sancao.TIPO_SANCAO_CHOICES),
            'pedido_saida_estados': fmt(PedidoSaida.ESTADO_CHOICES),
            'quarto_estados': fmt(Quarto.ESTADO_CHOICES),
            'generos': fmt(Estudante.GENERO_CHOICES),
        }, status=status.HTTP_200_OK)


class CriarUtilizadorStaffView(generics.CreateAPIView):
    """Cria um novo utilizador interno com um ou vários perfis
    (Gestor, Financeiro, Disciplinar, Suporte — em qualquer combinação)."""
    serializer_class = CriarUtilizadorStaffSerializer
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]  # ver nota abaixo

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dados = serializer.validated_data

        User = get_user_model()
        SENHA_PADRAO = "mudar1234"

        perfis_obj = Perfil.objects.filter(nome_perfil__in=dados['perfis'])
        if perfis_obj.count() != len(dados['perfis']):
            return Response({"erro": "Um ou mais perfis indicados não existem na BD."}, status=400)

        with transaction.atomic():
            nome_partes = dados['nome_completo'].split(' ', 1)
            user = User.objects.create_user(
                email=dados['email'],
                password=SENHA_PADRAO,
                first_name=nome_partes[0],
                last_name=nome_partes[1] if len(nome_partes) > 1 else '',
                is_staff=True,
            )
            user.perfis.set(perfis_obj)

        return Response({
            "status": "sucesso",
            "utilizador_id": user.pk,
            "perfis": dados['perfis'],
            "senha_temporaria": SENHA_PADRAO,
        }, status=status.HTTP_201_CREATED)

# views.py (acrescentar)

class AdminUtilizadorListView(generics.ListAPIView):
    """Lista utilizadores internos (staff) com filtros e pesquisa."""
    serializer_class = UserListAdminSerializer
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['email', 'first_name', 'last_name']
    filterset_fields = ['perfis__nome_perfil', 'is_active']

    def get_queryset(self):
        # Apenas utilizadores que têm pelo menos um perfil interno
        return Utilizador.objects.filter(
            perfis__nome_perfil__in=['Gestor', 'Financeiro', 'Disciplinar', 'Suporte']
        ).distinct().order_by('first_name')


class AdminUtilizadorDetailView(generics.RetrieveUpdateAPIView):
    """GET / PATCH para editar dados e perfis de um utilizador interno."""
    queryset = Utilizador.objects.filter(
        perfis__nome_perfil__in=['Gestor', 'Financeiro', 'Disciplinar', 'Suporte']
    ).distinct()
    serializer_class = UserUpdateAdminSerializer
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]

    def perform_update(self, serializer):
        # Se for desativado, remove permissões de acesso
        user = serializer.save()
        if not user.is_active:
            # opcional: notificar ou logout forçado
            pass


class AdminUtilizadorToggleActiveView(APIView):
    """PATCH: activar/desactivar um utilizador (is_active)."""
    permission_classes = [IsAuthenticated, IsGestorOuSuporte]

    def patch(self, request, pk):
        user = get_object_or_404(Utilizador, pk=pk)
        # Verifica se tem perfil interno
        if not user.perfis.filter(nome_perfil__in=['Gestor','Financeiro','Disciplinar','Suporte']).exists():
            return Response({"erro": "Utilizador não é staff."}, status=400)
        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])
        return Response({"status": "Estado alterado", "is_active": user.is_active})