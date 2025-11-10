from django.shortcuts import render
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Utilizador, Perfil, Encarregado, Estudante, Mensalidade, Sancao, PresencaEstudo
from .serializers import UserSerializer, RegistoCompletoSerializer, MensalidadeSerializer, MensalidadeUpdateSerializer, SancaoSerializer, PresencaBatchSerializer, EstudanteListSerializer
from .permissions import IsAdminUser
from django.contrib.auth import get_user_model  # <-- ADICIONE ESTA LINHA
from django.db import transaction  # <-- ADICIONE ESTA LINHA
from django.shortcuts import get_object_or_404 # <-- ADICIONE ESTA
from rest_framework.views import APIView # <-- ADICIONE ESTA

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
        
        # Dados validados
        dados = serializer.validated_data
        dados_encarregado = dados['encarregado']
        dados_estudante = dados['estudante']

        # Obter o Model 'Utilizador'
        User = get_user_model()
        
        # Uma senha padrão (o utilizador deve mudar no primeiro login)
        SENHA_PADRAO = "mudar1234" 

        try:
            # Obter os Perfis que criámos nas migrações
            perfil_encarregado = Perfil.objects.get(nome_perfil='Encarregado')
            perfil_estudante = Perfil.objects.get(nome_perfil='Estudante')

            # --- Iniciar Transação Atómica ---
            # Se algo falhar aqui, tudo é revertido.
            with transaction.atomic():
                
                # 1. Criar Utilizador (Encarregado)
                user_encarregado = User.objects.create_user(
                    email=dados_encarregado['email'],
                    password=SENHA_PADRAO,
                    first_name=dados_encarregado['nome_completo'],
                    perfil=perfil_encarregado
                )

                # 2. Criar Perfil (Encarregado)
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

                # 4. Criar Perfil (Estudante)
                estudante = Estudante.objects.create(
                    utilizador=user_estudante,
                    encarregado=encarregado, # Ligar ao encarregado
                    nome_completo=dados_estudante['nome_completo'],
                    num_estudante=dados_estudante['num_estudante'],
                    quarto=dados_estudante['quarto'],
                    curso=dados_estudante['curso']
                )
            
            # Se tudo correu bem...
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

class MensalidadeDetailView(generics.RetrieveUpdateAPIView):
    """
    Endpoint para:
    GET: Ver uma mensalidade específica.
    PATCH: Atualizar (ex: confirmar) uma mensalidade específica.
    Acesso: Só Admin.
    """
    queryset = Mensalidade.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = MensalidadeUpdateSerializer # Usa o serializer de ATUALIZAÇÃO

    def perform_update(self, serializer):
        """
        Ao actualizar, regista também o admin que fez a alteração.
        """
        serializer.save(admin_id_registo=self.request.user)

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