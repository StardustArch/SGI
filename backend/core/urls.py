# Ficheiro: backend/core/urls.py
#
# Alterações desta versão:
#   - Rotas duplicadas de dashboard individuais removidas (/relatorios/*)
#   - Adicionada rota de transferência de quarto
#   - Rotas reorganizadas por módulo para melhor leitura
#   - Comentários de "ADICIONE ESTA LINHA" limpos

from django.urls import path
from . import views

urlpatterns = [

    # =========================================================================
    # AUTH & UTILIZADOR
    # =========================================================================
    path('users/me/', views.ManageUserView.as_view(), name='manage-user'),
    path('users/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('auth/password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('auth/password-reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    # =========================================================================
    # REGISTO
    # =========================================================================
    path('admin/registar/', views.RegistoCompletoView.as_view(), name='admin-registar'),

    # =========================================================================
    # ESTUDANTES
    # =========================================================================
    path('admin/estudantes/', views.EstudanteListView.as_view(), name='admin-student-list'),
    path('admin/estudantes/<int:pk>/', views.EstudanteDetailView.as_view(), name='admin-student-detail'),
    path('admin/estudantes/<int:pk>/transferir-quarto/', views.TransferirQuartoView.as_view(), name='admin-transferir-quarto'),
    path('admin/estudantes/<int:estudante_pk>/presencas/', views.EstudantePresencaListView.as_view(), name='lista-presencas-estudante'),

    # =========================================================================
    # MENSALIDADES
    # =========================================================================
    path('admin/estudantes/<int:estudante_id>/mensalidades/', views.MensalidadeListCreateView.as_view(), name='lista-mensalidades'),
    path('admin/mensalidades/<int:pk>/', views.MensalidadeDetailView.as_view(), name='detalhe-mensalidade'),
    path('admin/mensalidades/<int:pk>/recibo/', views.GerarReciboView.as_view(), name='gerar-recibo'),
    path('admin/financeiro/mensalidades/', views.AdminMensalidadeListView.as_view(), name='admin-fin-list'),
    path('admin/financeiro/gerar-lote/', views.GerarMensalidadesLoteView.as_view(), name='admin-gerar-mensalidades'),

    # =========================================================================
    # SANÇÕES
    # =========================================================================
    path('admin/estudantes/<int:estudante_id>/sancoes/', views.SancaoListCreateView.as_view(), name='lista-sancoes'),
    path('admin/sancoes/<int:pk>/', views.SancaoDetailView.as_view(), name='detalhe-sancao'),
    path('admin/sancoes/', views.AdminSancaoListCreateView.as_view(), name='admin-sancoes-global'),

    # =========================================================================
    # PRESENÇAS
    # =========================================================================
    path('admin/presencas/batch/', views.PresencaBatchCreateView.as_view(), name='admin-presenca-batch'),
    path('admin/presencas/<int:pk>/', views.PresencaEstudoDetailView.as_view(), name='detalhe-presenca'),
    path('admin/presencas/', views.PresencaListView.as_view(), name='presenca-list'),
    # =========================================================================
    # QUARTOS
    # =========================================================================
    path('admin/quartos/', views.QuartoListCreateView.as_view(), name='admin-quarto-list'),
    path('admin/quartos/<int:pk>/', views.QuartoDetailView.as_view(), name='admin-quarto-detail'),

    # =========================================================================
    # ENCARREGADOS (admin)
    # =========================================================================
    path('admin/encarregados/', views.AdminEncarregadoListView.as_view(), name='admin-encarregado-list'),
    path('admin/encarregados/<int:pk>/', views.AdminEncarregadoDetailView.as_view(), name='admin-encarregado-detail'),

    # =========================================================================
    # PEDIDOS DE SAÍDA (admin)
    # =========================================================================
    path('admin/pedidos-saida/', views.AdminPedidoSaidaListView.as_view(), name='admin-pedidos-list'),
    path('admin/pedidos-saida/<int:pk>/', views.AdminPedidoSaidaDetailView.as_view(), name='admin-pedido-detail'),
    path('admin/portaria/<int:pk>/movimento/', views.PortariaConfirmarMovimentoView.as_view(), name='admin-portaria'),

    # =========================================================================
    # DASHBOARD & RELATÓRIOS
    # dashboard unificado — substituiu as 5 views individuais removidas
    # =========================================================================
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin/relatorios/exportar/', views.ExportarRelatorioView.as_view(), name='exportar-relatorio'),

    # =========================================================================
    # UTILITÁRIOS
    # =========================================================================
    path('opcoes/', views.OpcoesView.as_view(), name='opcoes-dropdown'),

    # =========================================================================
    # PERFIL DO ESTUDANTE
    # =========================================================================
    path('student/me/', views.PerfilEstudanteDetailView.as_view(), name='student-profile'),
    path('student/exits/', views.PedidoSaidaListCreateView.as_view(), name='student-exits'),
    path('student/exits/<int:pk>/', views.PerfilPedidoSaidaDetailView.as_view(), name='student-exit-detail'),
    path('student/financial/', views.PerfilMensalidadeListView.as_view(), name='student-financial'),
    path('student/discipline/', views.PerfilSancaoListView.as_view(), name='student-discipline'),
    path('student/attendance/', views.PerfilPresencaListView.as_view(), name='student-attendance'),

    # =========================================================================
    # PERFIL DO ENCARREGADO
    # =========================================================================
    path('guardian/profile/', views.EncarregadoProfileView.as_view(), name='encarregado-meus-dados'),
    path('guardian/students/', views.EncarregadoEducandosListView.as_view(), name='encarregado-educandos'),
    path('guardian/students/<int:pk>/', views.EncarregadoEducandoDetailView.as_view(), name='encarregado-educando-detalhe'),
    path('guardian/financial/', views.EncarregadoMensalidadeListView.as_view(), name='encarregado-mensalidades'),
    path('guardian/financial/summary/', views.EncarregadoFinanceiroStatsView.as_view(), name='encarregado-financas-stats'),
    path('guardian/discipline/', views.EncarregadoSancaoListView.as_view(), name='encarregado-sancoes'),
    path('guardian/attendance/', views.EncarregadoPresencaListView.as_view(), name='encarregado-presencas'),
    path('guardian/exits/', views.EncarregadoPedidoSaidaListView.as_view(), name='encarregado-pedidos-saida'),
    path('guardian/exits/<int:pk>/', views.EncarregadoPedidoSaidaDetailView.as_view(), name='encarregado-pedido-acao'),
]