# Ficheiro: backend/core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Mapeia o URL 'me/' para a nossa ManageUserView
    path('users/me/', views.ManageUserView.as_view(), name='manage-user'),
    # ---- ADICIONE ESTA NOVA ROTA ----
    path('users/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('users/admin/registar/', views.RegistoCompletoView.as_view(), name='admin-registar'),
    path('auth/password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('auth/password-reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    # ---- ADICIONE ESTA NOVA LINHA AQUI ----
    # GET: Lista todos os estudantes (para pesquisa)
    path(
        'estudantes/', 
        views.EstudanteListView.as_view(), 
        name='lista-estudantes'
    ),
    # GET: Lista mensalidades do estudante_id
    # POST: Cria nova mensalidade (ex: Pendente) para o estudante_id
    path(
        'estudantes/<int:estudante_id>/mensalidades/', 
        views.MensalidadeListCreateView.as_view(), 
        name='lista-mensalidades'
    ),

    # GET: Vê uma mensalidade específica
    # PATCH: Atualiza (confirma) uma mensalidade específica
    path(
        'mensalidades/<int:pk>/', 
        views.MensalidadeDetailView.as_view(), 
        name='detalhe-mensalidade'
    ),
    # ---- ADICIONE ESTA NOVA LINHA ----
    
    # UC-Admin-03: Gestão Disciplinar
    
    # GET: Lista sanções do estudante_id
    # POST: Cria nova sanção para o estudante_id
    path(
        'estudantes/<int:estudante_id>/sancoes/', 
        views.SancaoListCreateView.as_view(), 
        name='lista-sancoes'
    ),
    path(
        'presencas/batch/', 
        views.PresencaBatchCreateView.as_view(), 
        name='presenca-batch'
    ),
      # ---- ADICIONE ESTA NOVA ROTA ----
    # GET/PATCH: Detalhes de UM estudante
    path(
        'estudantes/<int:pk>/',
        views.EstudanteDetailView.as_view(),
        name='detalhe-estudante'
    ),

# ---- ADICIONE ESTA NOVA ROTA ----
    # GET: (Estudante) Vê os seus detalhes de perfil
    # GET: Lista as minhas mensalidades
    
    # ---- ADICIONE ESTA NOVA ROTA ----
    # GET/PATCH/DELETE: Detalhes de UMA sanção
    path(
        'sancoes/<int:pk>/',
        views.SancaoDetailView.as_view(),
        name='detalhe-sancao'
    ),
    # GET: Lista as minhas sanções
    
    # GET: Lista as minhas presenças

    # GET/PATCH/DELETE: Detalhes de UM registo de presença
    path(
        'presencas/<int:pk>/',
        views.PresencaEstudoDetailView.as_view(),
        name='detalhe-presenca'
    ),
    # GET: Lista os meus pedidos de saída
    # POST: Cria um novo pedido de saída (UC-04 Parte A)

    # GET: (Admin) Lista todos os pedidos (filtra por ?estado=Pendente)

    # PATCH: (Admin) Aprova/Rejeita um pedido específico

    path('perfil/pedidos-saida/<int:pk>/', views.PerfilPedidoSaidaDetailView.as_view(), name='perfil-detalhe-pedido'),

    path('admin/financeiro/gerar-lote/', views.GerarMensalidadesLoteView.as_view(), name='admin-gerar-mensalidades'),

    path('admin/presencas/batch/', views.PresencaBatchCreateView.as_view(), name='admin-presenca-batch'),
    path('admin/pedidos-saida/', views.AdminPedidoSaidaListView.as_view(), name='admin-pedidos-list'),
    path('admin/pedidos-saida/<int:pk>/', views.AdminPedidoSaidaDetailView.as_view(), name='admin-pedido-detail'),
    # Listagem e Pesquisa
path('admin/estudantes/', views.EstudanteListView.as_view(), name='admin-student-list'),
# Detalhes e Edição
path('admin/estudantes/<int:pk>/', views.EstudanteDetailView.as_view(), name='admin-student-detail'),
# -----------------------------------------------------------------
# --- PERFIL DE ESTUDANTE ---
# -----------------------------------------------------------------

    path('student/me/', views.PerfilEstudanteDetailView.as_view(), name='student-profile'),
    path('student/exits/', views.PedidoSaidaListCreateView.as_view(), name='student-exits'),
    path('student/financial/', views.PerfilMensalidadeListView.as_view(), name='student-financial'),
    path('student/discipline/', views.PerfilSancaoListView.as_view(), name='student-discipline'),
    path('student/attendance/', views.PerfilPresencaListView.as_view(), name='student-attendance'),





# -----------------------------------------------------------------
# --- PERFIL DE ENCARREGADO ---
# -----------------------------------------------------------------

    path('perfil-encarregado/meus-educandos/', views.EncarregadoEducandosListView.as_view(), name='encarregado-educandos'),
    path('perfil-encarregado/meus-educandos/<int:pk>/', views.EncarregadoEducandoDetailView.as_view(), name='encarregado-educando-detalhe'),
    path('perfil-encarregado/mensalidades/', views.EncarregadoMensalidadeListView.as_view(), name='encarregado-mensalidades'),
    path('perfil-encarregado/financas-resumo/', views.EncarregadoFinanceiroStatsView.as_view(), name='encarregado-financas-stats'),
    path('perfil-encarregado/sancoes/', views.EncarregadoSancaoListView.as_view(), name='encarregado-sancoes'),
    path('perfil-encarregado/presencas/', views.EncarregadoPresencaListView.as_view(), name='encarregado-presencas'),
    path('perfil-encarregado/pedidos-saida/<int:pk>/', views.EncarregadoPedidoSaidaDetailView.as_view(), name='encarregado-pedido-acao'),
    path('perfil-encarregado/meus-dados/', views.EncarregadoProfileView.as_view(), name='encarregado-meus-dados'),
    path('perfil-encarregado/pedidos-saida/', views.EncarregadoPedidoSaidaListView.as_view(), name='encarregado-pedidos-saida'),








       # ---- ADICIONE ESTA NOVA ROTA ----
    # GET: Lista histórico de presenças do estudante
    path(
        'estudantes/<int:estudante_pk>/presencas/',
        views.EstudantePresencaListView.as_view(),
        name='lista-presencas-estudante'
    ),

    # GET: Lista os pedidos de saída dos meus educandos
    path('relatorios/financeiro/', views.FinanceiroSummaryView.as_view(), name='relatorio-financeiro'),
    path('relatorios/disciplina/top-10/', views.TopInfratoresView.as_view(), name='relatorio-top-infratores'),
    path('relatorios/assiduidade/top-ausentes/', views.TopAusentesView.as_view(), name='relatorio-top-ausentes'),
    path('relatorios/disciplina/por-tipo/', views.TipoSancaoSummaryView.as_view(), name='relatorio-por-tipo'),
    path('relatorios/pedidos-saida/sumario/', views.PedidoSaidaSummaryView.as_view(), name='relatorio-pedidos-sumario'),
    path('opcoes/', views.OpcoesView.as_view(), name='opcoes-dropdown'),

]