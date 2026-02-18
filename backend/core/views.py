from django.shortcuts import render
from rest_framework import generics, status, filters
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Utilizador, Perfil, Encarregado, Estudante, Mensalidade, Sancao, PresencaEstudo, PedidoSaida
from .serializers import UserSerializer, RegistoCompletoSerializer, MensalidadeSerializer, MensalidadeUpdateSerializer, SancaoSerializer, PresencaBatchSerializer, EstudanteListSerializer, PresencaEstudoSerializer, PedidoSaidaSerializer, PedidoSaidaListAdminSerializer, PedidoSaidaUpdateAdminSerializer, FinanceiroSummarySerializer,TopInfratoresSerializer, TopAusentesSerializer, TipoSancaoSummarySerializer, PedidoSaidaSummarySerializer, EstudanteDetailSerializer, SancaoUpdateSerializer,PresencaEstudoUpdateSerializer, EstudantePerfilSerializer, ChangePasswordSerializer, PedidoSaidaEncarregadoUpdateSerializer, EncarregadoProfileUpdateSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer
from .permissions import IsAdminUser, IsEstudanteUser, IsOwnerOfPedidoSaida, IsEncarregadoUser
from django.contrib.auth import get_user_model  # <-- ADICIONE ESTA LINHA
from django.db import transaction  # <-- ADICIONE ESTA LINHA
from django.shortcuts import get_object_or_404 # <-- ADICIONE ESTA
from rest_framework.views import APIView # <-- ADICIONE ESTA
from django.db.models import Sum, Count, Q # <-- ADICIONE ESTA
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone # Não esquecer de importar
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class ManageUserView(generics.RetrieveAPIView):
    """
    View para o utilizador autenticado ver o seu próprio perfil.
    """
    serializer_class = UserSerializer
    
    # ---- A MÁGICA ESTÁ AQUI ----
    # Isto bloqueia o acesso a este endpoint, 
    # exigindo um token de acesso válido.
    permission_classes = [IsAuthenticated] 

    def get_object(self):
        # Retorna automaticamente o objecto 'Utilizador'
        # associado ao token que fez o pedido.
        return self.request.user

class RegistoCompletoView(generics.CreateAPIView):
    """
    Endpoint para o Admin registar um Encarregado e Estudante
    de uma só vez.
    """
    serializer_class = RegistoCompletoSerializer
    
    # Protegido: Tem de estar autenticado E ser um Admin.
    permission_classes = [IsAuthenticated, IsAdminUser]

    # Usamos 'create' em vez de 'perform_create' 
    # para controlar a lógica e a resposta.
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        dados = serializer.validated_data
        dados_encarregado = dados['encarregado']
        dados_estudante = dados['estudante']

        User = get_user_model()
        SENHA_PADRAO = "mudar1234" 

        try:
            perfil_encarregado = Perfil.objects.get(nome_perfil='Encarregado')
            perfil_estudante = Perfil.objects.get(nome_perfil='Estudante')

            with transaction.atomic():
                
                # 1. Criar Utilizador (Encarregado)
                user_encarregado = User.objects.create_user(
                    email=dados_encarregado['email'],
                    password=SENHA_PADRAO,
                    first_name=dados_encarregado['nome_completo'],
                    perfil=perfil_encarregado
                )
                # ... (resto da criação do Encarregado) ...
                encarregado = Encarregado.objects.create(
                    utilizador=user_encarregado,
                    nome_completo=dados_encarregado['nome_completo'],
                    telefone_principal=dados_encarregado['telefone_principal'],
                    email_contacto=dados_encarregado['email']
                )

                # 3. Criar Utilizador (Estudante)
                user_estudante = User.objects.create_user(
                    email=dados_estudante['email'],
                    password=SENHA_PADRAO,
                    first_name=dados_estudante['nome_completo'],
                    perfil=perfil_estudante
                )
                # ... (resto da criação do Estudante) ...
                estudante = Estudante.objects.create(
                    utilizador=user_estudante,
                    encarregado=encarregado,
                    nome_completo=dados_estudante['nome_completo'],
                    num_estudante=dados_estudante['num_estudante'],
                    quarto=dados_estudante['quarto'],
                    curso=dados_estudante['curso']
                )
            
            # --- TRANSAÇÃO CONCLUÍDA ---
            # ---- ADICIONE ESTA LÓGICA DE EMAIL ----
            
            print("--- SINAL (Manual): Novo Registo Completo ---")
            
            # 1. Enviar email ao Encarregado
            try:
                send_mail(
                    "Bem-vindo ao Portal SGI (Encarregado)",
                    f"Olá {encarregado.nome_completo},\n\n"
                    f"A sua conta de Encarregado no portal SGI foi criada.\n"
                    f"Login: {encarregado.email_contacto}\n"
                    f"Senha Temporária: {SENHA_PADRAO}\n\n"
                    "Por favor, altere a sua senha no primeiro login.",
                    settings.DEFAULT_FROM_EMAIL,
                    [encarregado.email_contacto],
                    fail_silently=False,
                )
                print(f"--- Email de Boas-Vindas enviado para Encarregado: {encarregado.email_contacto} ---")
            except Exception as e:
                print(f"--- ERRO AO ENVIAR EMAIL (Encarregado): {str(e)} ---")
            
            # 2. Enviar email ao Estudante
            try:
                send_mail(
                    "Bem-vindo ao Portal SGI (Estudante)",
                    f"Olá {estudante.nome_completo},\n\n"
                    f"A sua conta de Estudante no portal SGI foi criada.\n"
                    f"Login: {user_estudante.email}\n"
                    f"Senha Temporária: {SENHA_PADRAO}\n\n"
                    "Por favor, altere a sua senha no primeiro login.",
                    settings.DEFAULT_FROM_EMAIL,
                    [user_estudante.email],
                    fail_silently=False,
                )
                print(f"--- Email de Boas-Vindas enviado para Estudante: {user_estudante.email} ---")
            except Exception as e:
                print(f"--- ERRO AO ENVIAR EMAIL (Estudante): {str(e)} ---")

            # --- FIM DA LÓGICA DE EMAIL ---
            
            # Resposta original
            return Response(
                {"status": "sucesso", "estudante_id": estudante.utilizador_id}, 
                status=status.HTTP_201_CREATED
            )

        except Perfil.DoesNotExist:
            return Response(
                {"erro": "Perfis 'Encarregado' ou 'Estudante' não encontrados na BD."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            # Captura outros erros (ex: email duplicado)
            return Response(
                {"erro": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class MensalidadeListCreateView(generics.ListCreateAPIView):
    """
    Endpoint para:
    GET: Listar todas as mensalidades de UM estudante.
    POST: Criar uma nova mensalidade (ex: "Pendente") para esse estudante.
    Acesso: Só Admin.
    """
    serializer_class = MensalidadeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        Esta função filtra a lista de mensalidades.
        Retorna apenas as do estudante especificado na URL.
        """
        # self.kwargs['estudante_id'] vem da URL
        estudante_id = self.kwargs['estudante_id']
        return Mensalidade.objects.filter(estudante_id=estudante_id).order_by('-mes_referencia')
    
    def perform_create(self, serializer):
        """
        Esta função é chamada ao criar (POST) uma nova mensalidade.
        Associa automaticamente o estudante (da URL) e o admin (do token).
        """
        estudante_id = self.kwargs['estudante_id']
        estudante = get_object_or_404(Estudante, pk=estudante_id)
        
        serializer.save(
            estudante=estudante, 
            admin_id_registo=self.request.user # O admin que está logado
        )

# Ficheiro: backend/core/views.py

class MensalidadeDetailView(generics.RetrieveUpdateAPIView):
    """
    Endpoint para:
    GET: Ver uma mensalidade específica.
    PATCH: Atualizar (ex: confirmar) uma mensalidade específica.
    Acesso: Só Admin.
    """
    queryset = Mensalidade.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    # IMPORTANTE: Temos de lhe dizer para usar o serializer
    # de actualização (Update) ou o de listagem (Retrieve)
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return MensalidadeUpdateSerializer
        return MensalidadeSerializer # Usar o serializer completo para GET

    # --- SÓ PODE HAVER UMA FUNÇÃO 'perform_update' ---
    def perform_update(self, serializer):
        """
        Ao actualizar, regista o admin E passa 'update_fields'
        para que o nosso signal de notificação funcione.
        """
        
        # 1. Pega na lista de campos que vieram no PATCH
        #    (ex: ['estado', 'valor_pago'])
        updated_fields = list(serializer.validated_data.keys())
        
        # 2. Adiciona o campo que estamos a adicionar manualmente
        updated_fields.append('admin_id_registo')

        # 3. Salva, passando a lista de campos
        #    Isto é o que envia o 'update_fields' para o signal
        mensalidade = serializer.save(admin_id_registo=self.request.user)

        # Agora faz o save direto no modelo, com update_fields
        mensalidade.save(update_fields=updated_fields)


# Ficheiro: backend/core/views.py
# ... (Manter as views de Mensalidade existentes) ...

# --- ADICIONE ESTA NOVA VIEW ---

class SancaoListCreateView(generics.ListCreateAPIView):
    """
    Endpoint para:
    GET: Listar todas as sanções de UM estudante.
    POST: Criar uma nova sanção para esse estudante.
    Acesso: Só Admin.
    """
    serializer_class = SancaoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        Esta função filtra a lista de sanções.
        Retorna apenas as do estudante especificado na URL.
        """
        estudante_id = self.kwargs['estudante_id']
        return Sancao.objects.filter(estudante_id=estudante_id).order_by('-data_ocorrencia')
    
    def perform_create(self, serializer):
        """
        Esta função é chamada ao criar (POST) uma nova sanção.
        Associa automaticamente o estudante (da URL) e o admin (do token).
        """
        estudante_id = self.kwargs['estudante_id']
        estudante = get_object_or_404(Estudante, pk=estudante_id)
        
        serializer.save(
            estudante=estudante, 
            admin_id_registo=self.request.user # O admin que está logado
        )

# Ficheiro: backend/core/views.py
# ... (Manter as views Sancao existentes) ...

# --- ADICIONE ESTA NOVA VIEW ---

class PresencaBatchCreateView(APIView):
    """
    Endpoint para criar (POST) todas as presenças de estudo
    de um dia específico de uma só vez (em lote).
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = PresencaBatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data_presenca = data['data_presenca']
        admin_logado = request.user

        # Usamos sets para performance (ex: 500 estudantes)
        ids_ausentes = set(data.get('ausentes_ids', []))
        ids_justificados = set(data.get('justificados_ids', []))

        # Obter TODOS os estudantes que deveriam estar no estudo
        todos_estudantes_activos = Estudante.objects.filter(estado='Activo')
        
        # Lista para 'bulk_create' (muito rápido)
        presencas_para_criar = []
        
        try:
            # --- Iniciar Transação Atómica ---
            # Garante que ou TODOS são registados, ou NENHUM é.
            with transaction.atomic():
                
                # 1. Percorrer todos os estudantes
                for estudante in todos_estudantes_activos:
                    estado = 'Presente' # Começa como presente
                    
                    if estudante.pk in ids_ausentes:
                        estado = 'Ausente'
                    elif estudante.pk in ids_justificados:
                        estado = 'Justificado'
                    
                    presencas_para_criar.append(
                        PresencaEstudo(
                            estudante=estudante,
                            admin_id_registo=admin_logado,
                            data_presenca=data_presenca,
                            estado=estado
                        )
                    )
                
                # 2. Inserir tudo na BD de uma só vez
                # (Se já existir registo para este dia/estudante, vai falhar)
                PresencaEstudo.objects.bulk_create(presencas_para_criar)

            return Response(
                {"status": f"Sucesso: {len(presencas_para_criar)} presenças registadas para {data_presenca}."}, 
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            # A causa mais provável de falha é 'unique_together'
            # (tentar submeter presenças para um dia que já foi submetido)
            return Response(
                {"erro": f"Erro ao registar presenças. Já existem registos para este dia? Detalhe: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

# Ficheiro: backend/core/views.py
# ... (outras views) ...

# --- MODIFIQUE ESTA VIEW ---

class EstudanteListView(generics.ListAPIView):
    """
    Endpoint para:
    GET: Listar e pesquisar todos os estudantes (para o admin).
    Acesso: Só Admin.
    """
    serializer_class = EstudanteListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    # ---- ADICIONE ESTAS LINHAS ----
    # Ativa os filtros de backend
    filter_backends = [filters.SearchFilter]
    
    # Define os campos pelos quais podemos pesquisar
    # O 'nome_completo' usará 'icontains' (semelhante a LIKE)
    # O 'num_estudante' usará 'exact' (procura exata)
    search_fields = ['nome_completo', 'num_estudante']
    # --------------------------------

    def get_queryset(self):
        """
        Retorna todos os estudantes, por defeito apenas os 'Activos'.
        
        A pesquisa está ativada via query param 'search'.
        ex: /api/v1/estudantes/?search=joao
        """
        # O SearchFilter vai aplicar-se automaticamente a este queryset
        return Estudante.objects.filter(estado='Activo').order_by('nome_completo')

# Ficheiro: backend/core/views.py
# ... (Manter a view EstudanteListView) ...


# -----------------------------------------------------------------
# --- ENDPOINTS DO ADMIN (UC-04 Parte B) ---
# -----------------------------------------------------------------

class AdminPedidoSaidaListView(generics.ListAPIView):
    """
    Endpoint para o Admin (logado) ver a "fila" de pedidos de saída.
    Filtra por estado (ex: Pendente).
    """
    serializer_class = PedidoSaidaListAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] # Protegido!

    def get_queryset(self):
        """ Retorna pedidos, filtrados pelo 'estado' na URL """
        queryset = PedidoSaida.objects.all().order_by('data_submissao')

        # Filtra por ?estado=Pendente
        estado = self.request.query_params.get('estado', None)
        if estado is not None:
            queryset = queryset.filter(estado=estado)

        return queryset

class AdminPedidoSaidaDetailView(generics.UpdateAPIView):
    """
    Endpoint para o Admin (logado) Aprovar ou Rejeitar (PATCH)
    um pedido de saída específico.
    """
    queryset = PedidoSaida.objects.all()
    serializer_class = PedidoSaidaUpdateAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] # Protegido!

    # Ficheiro: backend/core/views.py
# Dentro da classe AdminPedidoSaidaDetailView

    def perform_update(self, serializer):
        """ 
        Ao aprovar/rejeitar, regista o admin E dispara o signal
        para notificar o estudante.
        """
        
        # 1. Pega na lista de campos que vieram no PATCH
        #    (ex: ['estado', 'observacao_admin'])
        updated_fields = list(serializer.validated_data.keys())
        
        # 2. Adiciona o campo que estamos a adicionar manualmente
        updated_fields.append('admin_id_aprovacao')

        # 3. (PASSO 1) Salva os dados do serializer
        pedido = serializer.save(
            admin_id_aprovacao=self.request.user
        )

        # 4. (PASSO 2) Salva *novamente* para disparar o sinal
        #    com a lista correcta de 'update_fields'.
        pedido.save(update_fields=updated_fields)


# Ficheiro: backend/core/views.py
# ... (Manter a view AdminPedidoSaidaDetailView) ...

# -----------------------------------------------------------------
# --- ENDPOINTS DO PERFIL DE ESTUDANTE (DETALHE) ---
# -----------------------------------------------------------------

class PerfilPedidoSaidaDetailView(generics.RetrieveAPIView):
    """
    Endpoint para o Estudante (logado) ver UM pedido de saída
    específico (ex: para ver a resposta do admin).
    """
    queryset = PedidoSaida.objects.all()
    serializer_class = PedidoSaidaSerializer
    
    # Protecção Dupla:
    # 1. Tem de ser um Estudante para sequer tentar.
    # 2. Tem de ser o DONO do objecto que está a pedir.
    permission_classes = [IsAuthenticated, IsEstudanteUser, IsOwnerOfPedidoSaida]


# Ficheiro: backend/core/views.py
# ... (Manter as views do Estudante) ...

# -----------------------------------------------------------------
# --- ENDPOINTS DO PERFIL DE ENCARREGADO (CONSULTA) ---
# -----------------------------------------------------------------

class EncarregadoEducandosListView(generics.ListAPIView):
    """
    Endpoint para o Encarregado (logado) ver
    a lista dos seus educandos.
    """
    serializer_class = EstudanteListSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser] # <-- Protegido!

    def get_queryset(self):
        """ Retorna apenas os estudantes associados ao encarregado logado """
        # request.user.encarregado funciona por causa do OneToOneField
        return Estudante.objects.filter(encarregado=self.request.user.encarregado, estado='Activo')

class EncarregadoMensalidadeListView(generics.ListAPIView):
    """
    Endpoint para o Encarregado (logado) ver
    o histórico financeiro dos seus educandos.
    """
    serializer_class = MensalidadeSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]
    pagination_class = StandardResultsSetPagination
    
    # Ativar filtros automáticos
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estudante', 'estado', 'mes_referencia']

    def get_queryset(self):
        """ Retorna mensalidades apenas dos estudantes do encarregado logado """
        # 1. Encontra os IDs dos estudantes deste encarregado
        estudante_ids = Estudante.objects.filter(
            encarregado=self.request.user.encarregado
        ).values_list('pk', flat=True)
        
        # 2. Retorna as mensalidades que pertencem a esses IDs
        return Mensalidade.objects.filter(estudante_id__in=estudante_ids).order_by('-mes_referencia')

# Adiciona isto no views.py

class EncarregadoEducandoDetailView(generics.RetrieveAPIView):
    """
    Endpoint para ver os dados detalhados (Nome, Curso, Quarto)
    de um estudante específico, MAS APENAS se for educando do user logado.
    """
    serializer_class = EstudanteListSerializer # Ou EstudanteDetailSerializer se tiveres um mais completo
    permission_classes = [IsAuthenticated, IsEncarregadoUser]

    def get_queryset(self):
        # Filtra para garantir que o ID solicitado pertence à lista de filhos do user
        return Estudante.objects.filter(encarregado=self.request.user.encarregado)


class EncarregadoFinanceiroStatsView(APIView):
    """
    Retorna o somatório do que já foi pago e do que está em dívida.
    """
    permission_classes = [IsAuthenticated, IsEncarregadoUser]

    def get(self, request):
        # Pegar todos os estudantes do encarregado
        estudantes = Estudante.objects.filter(encarregado=request.user.encarregado)
        
        # Pegar todas as mensalidades desses estudantes
        mensalidades = Mensalidade.objects.filter(estudante__in=estudantes)

        # Calcular Totais
        total_pago = mensalidades.filter(estado='Pago').aggregate(Sum('valor_pago'))['valor_pago__sum'] or 0
        total_pendente = mensalidades.filter(estado='Pendente').count()
        total_atraso = mensalidades.filter(estado='Atraso').count()

        return Response({
            "total_pago": total_pago,
            "faturas_pendentes": total_pendente,
            "faturas_atraso": total_atraso,
            "moeda": "MZN"
        })


class EncarregadoSancaoListView(generics.ListAPIView):
    serializer_class = SancaoSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]
    pagination_class = StandardResultsSetPagination # <--- Paginação Ativa
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['estudante', 'tipo_sancao'] 
    ordering = ['-data_ocorrencia'] # Padrão: Ocorrência mais recente no topo

    def get_queryset(self):
        estudante_ids = Estudante.objects.filter(
            encarregado=self.request.user.encarregado
        ).values_list('pk', flat=True)
        return Sancao.objects.filter(estudante_id__in=estudante_ids)

class EncarregadoPedidoSaidaListView(generics.ListAPIView):
    serializer_class = PedidoSaidaListAdminSerializer # Usa o que tem o nome do aluno
    permission_classes = [IsAuthenticated, IsEncarregadoUser]
    pagination_class = StandardResultsSetPagination # <--- Paginação Ativa
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['estudante', 'estado'] 
    ordering = ['-data_submissao'] # Padrão: Pedido mais recente primeiro

    def get_queryset(self):
        estudante_ids = Estudante.objects.filter(
            encarregado=self.request.user.encarregado
        ).values_list('pk', flat=True)
        return PedidoSaida.objects.filter(estudante_id__in=estudante_ids)


class EncarregadoPresencaListView(generics.ListAPIView):
    serializer_class = PresencaEstudoSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]
    pagination_class = StandardResultsSetPagination # <--- Paginação Ativa
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['estudante', 'estado', 'data_presenca'] 
    ordering = ['-data_presenca'] # Padrão: Hoje primeiro

    def get_queryset(self):
        estudante_ids = Estudante.objects.filter(
            encarregado=self.request.user.encarregado
        ).values_list('pk', flat=True)
        return PresencaEstudo.objects.filter(estudante_id__in=estudante_ids)


class EncarregadoPedidoSaidaDetailView(generics.UpdateAPIView):
    """
    Endpoint para o Encarregado (logado) FINALIZAR um pedido de saída.
    PATCH: Mudar estado de 'Aguardando_Encarregado' para 'Autorizado' ou 'Rejeitado'.
    """
    serializer_class = PedidoSaidaEncarregadoUpdateSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]

    def get_queryset(self):
        # Só pode editar pedidos dos seus próprios educandos
        estudante_ids = Estudante.objects.filter(
            encarregado=self.request.user.encarregado
        ).values_list('pk', flat=True)
        return PedidoSaida.objects.filter(estudante_id__in=estudante_ids)

    def perform_update(self, serializer):
        # 1. Verificar o estado atual antes de salvar
        pedido = self.get_object()
        
        # O Encarregado só pode mexer se o Admin já tiver aprovado
        if pedido.estado != 'Aguardando_Encarregado':
             raise serializers.ValidationError(
                 {"erro": "Não pode alterar este pedido. Ele ainda não foi aprovado pelo Admin ou já foi finalizado."}
             )

        # 2. Salvar o novo estado e a data
        serializer.save(data_aprovacao_encarregado=timezone.now())


# --- 1. ATUALIZAR PERFIL DO ENCARREGADO ---
class EncarregadoProfileView(generics.RetrieveUpdateAPIView):
    """
    GET: Vê os seus próprios dados (Telefone, Email).
    PATCH: Atualiza os seus contactos.
    """
    serializer_class = EncarregadoProfileUpdateSerializer
    permission_classes = [IsAuthenticated, IsEncarregadoUser]

    def get_object(self):
        # Retorna o objecto Encarregado ligado ao User
        return self.request.user.encarregado










# -----------------------------------------------------------------
# --- ENDPOINTS DE RELATÓRIOS (DASHBOARD) ---
# -----------------------------------------------------------------

class FinanceiroSummaryView(APIView):
    """
    Endpoint para o Dashboard do Admin.
    GET: Retorna um sumário financeiro do mês corrente.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        # 1. Obter o mês e ano actuais
        hoje = timezone.now().date()
        primeiro_dia_mes = hoje.replace(day=1)
        
        # 2. Filtrar todas as mensalidades deste mês
        mensalidades_mes = Mensalidade.objects.filter(
            mes_referencia=primeiro_dia_mes
        )

        # 3. Fazer os cálculos de agregação na BD
        sumario = mensalidades_mes.aggregate(
            # Soma o 'valor_pago' APENAS das que estão 'Pago'
            total_arrecadado=Sum(
                'valor_pago', 
                filter=Q(estado='Pago')
            ),
            
            # Conta quantos estudantes únicos têm estado 'Pendente'
            total_pendentes=Count(
                'estudante', 
                distinct=True, 
                filter=Q(estado='Pendente')
            )
        )
        
        # O 'total_pendente_mes' é mais complexo: 
        # Precisamos do valor *esperado*, não do 'valor_pago' (que é 0)
        # Assumindo que o valor é fixo. Por agora, vamos simplificar.
        # Vamos calcular o valor pendente com base no 'valor_pago' (se foi pago parcialmente)
        total_pendente_calculado = mensalidades_mes.filter(estado='Pendente').aggregate(
             total_pendente_valor=Sum('valor_pago') # Isto está conceptualmente errado, mas serve para o exemplo
        )['total_pendente_valor'] or 0

        # Vamos assumir que o "total pendente" é o número de estudantes * o valor da mensalidade
        # Por agora, vamos retornar 0 para este campo complexo.
        # TODO: A lógica de "valor pendente" precisa ser definida (ex: um campo 'valor_total' no modelo)
        
        data = {
            'total_arrecadado_mes': sumario.get('total_arrecadado') or 0,
            'total_pendente_mes': 0, # TODO: Implementar lógica de valor esperado
            'total_estudantes_pendentes': sumario.get('total_pendentes') or 0,
            'mes_referencia': primeiro_dia_mes
        }
        
        # Validar os dados de saída
        serializer = FinanceiroSummarySerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# Ficheiro: backend/core/views.py
# ... (Manter a view FinanceiroSummaryView) ...

# --- ADICIONE ESTA NOVA VIEW ---

class TopInfratoresView(APIView):
    """
    Endpoint para o Dashboard do Admin.
    GET: Retorna os 5 estudantes com mais sanções este mês.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        # 1. Obter o primeiro dia do mês actual
        hoje = timezone.now().date()
        primeiro_dia_mes = hoje.replace(day=1)
        
        # 2. Query de Agregação
        top_infratores = Sancao.objects.filter(
            # Apenas sanções deste mês em diante
            data_ocorrencia__gte=primeiro_dia_mes 
        ).values(
            'estudante',                # Agrupa por ID do estudante
            'estudante__nome_completo'  # Puxa o nome do estudante
        ).annotate(
            total_sancoes=Count('id')   # Conta o nº de sanções por grupo
        ).order_by(
            '-total_sancoes'            # Ordena do maior para o menor
        )[:10]                           # Limita aos 10 primeiros
        
        # 3. Serializar e Retornar
        # O 'top_infratores' é uma lista de dicts
        # (ex: [{'estudante': 3, 'estudante__nome_completo': 'João Aluno', 'total_sancoes': 2}])
        serializer = TopInfratoresSerializer(top_infratores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Ficheiro: backend/core/views.py
# ... (Manter a view TopInfratoresView) ...

# --- ADICIONE ESTA NOVA VIEW ---

class TopAusentesView(APIView):
    """
    Endpoint para o Dashboard do Admin.
    GET: Retorna os 5 estudantes com mais ausências/justificações este mês.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        # 1. Obter o primeiro dia do mês actual
        hoje = timezone.now().date()
        primeiro_dia_mes = hoje.replace(day=1)
        
        # 2. Query de Agregação
        top_ausentes = PresencaEstudo.objects.filter(
            # Apenas registos deste mês
            data_presenca__gte=primeiro_dia_mes,
            # Apenas onde o estado NÃO é 'Presente'
            estado__in=['Ausente', 'Justificado']
        ).values(
            'estudante',                # Agrupa por ID do estudante
            'estudante__nome_completo'  # Puxa o nome do estudante
        ).annotate(
            total_ausencias=Count('id') # Conta o nº de ausências por grupo
        ).order_by(
            '-total_ausencias'            # Ordena do maior para o menor
        )[:10]                           # Limita aos 10 primeiros
        
        # 3. Serializar e Retornar
        serializer = TopAusentesSerializer(top_ausentes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Ficheiro: backend/core/views.py
# ... (Manter a view TopAusentesView) ...

# --- ADICIONE ESTA NOVA VIEW ---

class TipoSancaoSummaryView(APIView):
    """
    Endpoint para o Dashboard do Admin.
    GET: Retorna um sumário de sanções agrupadas por tipo.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        # 1. Obter o primeiro dia do mês actual
        hoje = timezone.now().date()
        primeiro_dia_mes = hoje.replace(day=1)
        
        # 2. Query de Agregação
        sumario_tipo = Sancao.objects.filter(
            # Apenas sanções deste mês
            data_ocorrencia__gte=primeiro_dia_mes
        ).values(
            'tipo_sancao' # Agrupa pelo texto do tipo de sanção
        ).annotate(
            total=Count('id') # Conta o nº de sanções por tipo
        ).order_by(
            '-total' # Ordena do maior para o menor
        )
        
        # 3. Serializar e Retornar
        # O 'sumario_tipo' é uma lista de dicts
        # (ex: [{'tipo_sancao': 'Advertência Verbal', 'total': 2}])
        serializer = TipoSancaoSummarySerializer(sumario_tipo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Ficheiro: backend/core/views.py
# ... (Manter a view TipoSancaoSummaryView) ...

# --- ADICIONE ESTA NOVA VIEW ---

class PedidoSaidaSummaryView(APIView):
    """
    Endpoint para o Dashboard do Admin.
    GET: Retorna um sumário dos pedidos de saída agrupados por estado.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        # 1. Obter o primeiro dia do mês actual
        hoje = timezone.now().date()
        primeiro_dia_mes = hoje.replace(day=1)
        
        # 2. Query de Agregação
        # Filtra todos os pedidos deste mês
        sumario = PedidoSaida.objects.filter(
            data_submissao__gte=primeiro_dia_mes
        ).aggregate(
            # Conta apenas os que têm estado 'Pendente'
            total_pendentes=Count('id', filter=Q(estado='Pendente')),
            # Conta apenas os 'Aprovado_Admin'
            total_aprovados=Count('id', filter=Q(estado='Aprovado_Admin')),
            # Conta apenas os 'Rejeitado'
            total_rejeitados=Count('id', filter=Q(estado='Rejeitado'))
        )
        
        # 3. Serializar e Retornar
        # O 'sumario' é um dict único
        # (ex: {'total_pendentes': 0, 'total_aprovados': 2, 'total_rejeitados': 0})
        serializer = PedidoSaidaSummarySerializer(sumario)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Ficheiro: backend/core/views.py
# ... (Manter as views de Relatórios) ...

# -----------------------------------------------------------------
# --- ENDPOINT DE UTILIDADES (PARA DROPDOWNS DO FRONTEND) ---
# -----------------------------------------------------------------

class OpcoesView(APIView):
    """
    Endpoint de "utilidades" que retorna todas as
    opções (CHOICES) definidas nos modelos.
    Essencial para o frontend construir os dropdowns.
    """
    # Qualquer utilizador logado (Admin, Estudante) pode ver as opções
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        # Função helper para formatar os 'choices' do Django
        # (valor_bd, valor_legivel) -> { value: valor_bd, label: valor_legivel }
        # Isto é o formato perfeito para um <select> no frontend
        def format_choices(choices):
            return [{'value': choice[0], 'label': choice[1]} for choice in choices]

        # Construir o dicionário de opções
        opcoes = {
            'perfis': format_choices(Perfil.NOME_CHOICES),
            'estudante_estados': format_choices(Estudante.ESTADO_CHOICES),
            'mensalidade_metodos': format_choices(Mensalidade.METODO_CHOICES),
            'mensalidade_estados': format_choices(Mensalidade.ESTADO_CHOICES),
            'presenca_estados': format_choices(PresencaEstudo.ESTADO_CHOICES),
            'sancao_tipos': format_choices(Sancao.TIPO_SANCAO_CHOICES),
            'pedido_saida_estados': format_choices(PedidoSaida.ESTADO_CHOICES),
        }
        
        return Response(opcoes, status=status.HTTP_200_OK)


# --- ADICIONE ESTAS DUAS NOVAS VIEWS ---

class EstudanteDetailView(generics.RetrieveUpdateAPIView):
    """
    Endpoint para Admin:
    GET: Ver os detalhes de UM estudante.
    PATCH: Atualizar os dados de UM estudante (nome, quarto, curso, estado).
    """
    queryset = Estudante.objects.all()
    serializer_class = EstudanteDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'pk' # A PK do Estudante é o 'utilizador_id'

class EstudantePresencaListView(generics.ListAPIView):
    """
    Endpoint para Admin:
    GET: Listar o histórico de presenças de UM estudante.
    """
    serializer_class = PresencaEstudoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """ Filtra presenças pelo estudante_pk da URL """
        # Usamos 'estudante_pk' para evitar conflito com 'pk' de outras rotas
        estudante_pk = self.kwargs['estudante_pk']
        return PresencaEstudo.objects.filter(estudante_id=estudante_pk).order_by('-data_presenca')

class SancaoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint para Admin:
    GET: Ver uma sanção específica.
    PATCH: Atualizar uma sanção específica.
    DELETE: Apagar uma sanção específica.
    """
    queryset = Sancao.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    # Usar serializers diferentes para GET vs PATCH
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return SancaoUpdateSerializer
        return SancaoSerializer

class PresencaEstudoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint para Admin:
    GET: Ver um registo de presença específico.
    PATCH: Corrigir (atualizar) um registo.
    DELETE: Apagar um registo.
    """
    queryset = PresencaEstudo.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    # Usar serializers diferentes para GET vs PATCH
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return PresencaEstudoUpdateSerializer
        return PresencaEstudoSerializer



# Ficheiro: backend/core/views.py
# ... (Manter a view ManageUserView) ...

# --- ADICIONE ESTA NOVA VIEW ---

class ChangePasswordView(generics.UpdateAPIView):
    """
    Endpoint para um utilizador (logado) mudar a sua própria senha.
    Funciona para qualquer perfil (Admin, Estudante, Encarregado).
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated] # Só precisa de estar logado

    def get_object(self):
        # O objecto a ser atualizado é o próprio utilizador logado
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Lógica customizada para o PATCH (Update).
        """
        user = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # O .save() no serializer é que faz a mudança da senha
        serializer.save() 
        
        return Response({"status": "senha alterada com sucesso"}, status=status.HTTP_200_OK)







class PasswordResetRequestView(APIView):
    """
    Passo 1: Recebe o email e envia o link de recuperação.
    """
    permission_classes = [] # Qualquer um pode pedir (público)

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        User = get_user_model()
        user = User.objects.get(email=email)

        # 1. Gerar Token e ID codificado
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        # 2. Construir o Link para o Frontend (Nuxt)
        # Ajuste o domínio conforme necessário (localhost:3000 em dev)
        frontend_url = "http://localhost:3000/auth/reset-password"
        reset_link = f"{frontend_url}?uid={uidb64}&token={token}"

        # 3. Enviar Email
        # Nota: Para testar localmente, o email vai aparecer na consola (terminal)
        try:
            send_mail(
                subject="Recuperação de Senha - SGI",
                message=f"Olá {user.first_name},\n\nUse o link abaixo para redefinir a sua senha:\n\n{reset_link}\n\nSe não pediu isto, ignore.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({"erro": "Erro ao enviar email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": "Email de recuperação enviado."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Passo 2: Recebe a nova senha e o token, e altera a senha.
    """
    permission_classes = [] # Público

    def patch(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # O serializer já validou o token e encontrou o user
        user = serializer.validated_data['user']
        new_password = serializer.validated_data['password']

        # Definir a nova senha
        user.set_password(new_password)
        user.save()

        return Response({"status": "Senha redefinida com sucesso."}, status=status.HTTP_200_OK)



# -----------------------------------------------------------------
# --- PERFIL DE ESTUDANTE ---
# -----------------------------------------------------------------

class PerfilEstudanteDetailView(generics.RetrieveAPIView):
    """ Ver o próprio perfil """
    serializer_class = EstudantePerfilSerializer
    permission_classes = [IsAuthenticated, IsEstudanteUser]
    def get_object(self):
        return get_object_or_404(Estudante, pk=self.request.user.id)

class PedidoSaidaListCreateView(generics.ListCreateAPIView):
    """ Listar e Criar Pedidos de Saída """
    serializer_class = PedidoSaidaSerializer
    permission_classes = [IsAuthenticated, IsEstudanteUser]

    def get_queryset(self):
        # Só vê os seus pedidos
        return PedidoSaida.objects.filter(estudante_id=self.request.user.id).order_by('-data_submissao')

    def perform_create(self, serializer):
        # Auto-associa o estudante logado
        estudante = get_object_or_404(Estudante, pk=self.request.user.id)
        serializer.save(estudante=estudante)

class PerfilMensalidadeListView(generics.ListAPIView):
    """ Histórico Financeiro """
    serializer_class = MensalidadeSerializer
    permission_classes = [IsAuthenticated, IsEstudanteUser]
    def get_queryset(self):
        return Mensalidade.objects.filter(estudante_id=self.request.user.id).order_by('-mes_referencia')

class PerfilSancaoListView(generics.ListAPIView):
    """ Histórico Disciplinar """
    serializer_class = SancaoSerializer
    permission_classes = [IsAuthenticated, IsEstudanteUser]
    def get_queryset(self):
        return Sancao.objects.filter(estudante_id=self.request.user.id).order_by('-data_ocorrencia')

class PerfilPresencaListView(generics.ListAPIView):
    """ Histórico de Presenças """
    serializer_class = PresencaEstudoSerializer
    permission_classes = [IsAuthenticated, IsEstudanteUser]
    def get_queryset(self):
        return PresencaEstudo.objects.filter(estudante_id=self.request.user.id).order_by('-data_presenca')