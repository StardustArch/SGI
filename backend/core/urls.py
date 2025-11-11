# Ficheiro: backend/core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Mapeia o URL 'me/' para a nossa ManageUserView
    path('users/me/', views.ManageUserView.as_view(), name='manage-user'),
    path('users/admin/registar/', views.RegistoCompletoView.as_view(), name='admin-registar'),
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
    # GET: Lista as minhas mensalidades
    path('perfil/mensalidades/', views.PerfilMensalidadeListView.as_view(), name='perfil-mensalidades'),
    
    # GET: Lista as minhas sanções
    path('perfil/sancoes/', views.PerfilSancaoListView.as_view(), name='perfil-sancoes'),
    
    # GET: Lista as minhas presenças
    path('perfil/presencas/', views.PerfilPresencaListView.as_view(), name='perfil-presencas'),

    # GET: Lista os meus pedidos de saída
    # POST: Cria um novo pedido de saída (UC-04 Parte A)
    path('perfil/pedidos-saida/', views.PedidoSaidaListCreateView.as_view(), name='perfil-pedidos-saida'),

    # GET: (Admin) Lista todos os pedidos (filtra por ?estado=Pendente)
    path('admin/pedidos-saida/', views.AdminPedidoSaidaListView.as_view(), name='admin-lista-pedidos'),

    # PATCH: (Admin) Aprova/Rejeita um pedido específico
    path('admin/pedidos-saida/<int:pk>/', views.AdminPedidoSaidaDetailView.as_view(), name='admin-detalhe-pedido'),

    path('perfil/pedidos-saida/<int:pk>/', views.PerfilPedidoSaidaDetailView.as_view(), name='perfil-detalhe-pedido'),
    # GET: Lista os meus educandos
    path('perfil-encarregado/meus-educandos/', views.EncarregadoEducandosListView.as_view(), name='encarregado-educandos'),
    
    # GET: Lista o histórico financeiro dos meus educandos
    path('perfil-encarregado/mensalidades/', views.EncarregadoMensalidadeListView.as_view(), name='encarregado-mensalidades'),
    
    # GET: Lista o histórico disciplinar dos meus educandos
    path('perfil-encarregado/sancoes/', views.EncarregadoSancaoListView.as_view(), name='encarregado-sancoes'),
    
    # GET: Lista os pedidos de saída dos meus educandos
    path('perfil-encarregado/pedidos-saida/', views.EncarregadoPedidoSaidaListView.as_view(), name='encarregado-pedidos-saida'),
    path('relatorios/financeiro/', views.FinanceiroSummaryView.as_view(), name='relatorio-financeiro'),
    path('relatorios/disciplina/top-10/', views.TopInfratoresView.as_view(), name='relatorio-top-infratores'),
    path('relatorios/assiduidade/top-ausentes/', views.TopAusentesView.as_view(), name='relatorio-top-ausentes'),
    path('relatorios/disciplina/por-tipo/', views.TipoSancaoSummaryView.as_view(), name='relatorio-por-tipo'),
    path('relatorios/pedidos-saida/sumario/', views.PedidoSaidaSummaryView.as_view(), name='relatorio-pedidos-sumario'),
    path('opcoes/', views.OpcoesView.as_view(), name='opcoes-dropdown'),

]