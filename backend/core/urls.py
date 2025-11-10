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
]