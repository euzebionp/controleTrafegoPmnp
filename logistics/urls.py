from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # Motoristas
    path('motoristas/', views.motorista_list, name='motorista_list'),
    path('motoristas/novo/', views.motorista_create, name='motorista_create'),
    path('motoristas/<int:pk>/editar/', views.motorista_update, name='motorista_update'),
    path('motoristas/<int:pk>/excluir/', views.motorista_delete, name='motorista_delete'),
    
    # Veiculos
    path('veiculos/', views.veiculo_list, name='veiculo_list'),
    path('veiculos/novo/', views.veiculo_create, name='veiculo_create'),
    path('veiculos/<int:pk>/editar/', views.veiculo_update, name='veiculo_update'),
    path('veiculos/<int:pk>/excluir/', views.veiculo_delete, name='veiculo_delete'),
    
    # Viagens
    path('viagens/', views.viagem_list, name='viagem_list'),
    path('viagens/nova/', views.viagem_create, name='viagem_create'),
    path('viagens/<int:pk>/editar/', views.viagem_update, name='viagem_update'),
    path('viagens/<int:pk>/excluir/', views.viagem_delete, name='viagem_delete'),
    
    # Manutencoes
    path('manutencoes/', views.manutencao_list, name='manutencao_list'),
    path('manutencoes/nova/', views.manutencao_create, name='manutencao_create'),
    path('manutencoes/<int:pk>/editar/', views.manutencao_update, name='manutencao_update'),
    path('manutencoes/<int:pk>/excluir/', views.manutencao_delete, name='manutencao_delete'),
    
    # Multas
    path('multas/', views.multa_list, name='multa_list'),
    path('multas/nova/', views.multa_create, name='multa_create'),
    path('multas/<int:pk>/editar/', views.multa_update, name='multa_update'),
    path('multas/<int:pk>/excluir/', views.multa_delete, name='multa_delete'),
    
    # Reports
    path('relatorios/', views.reports_view, name='reports'),
    
    # PDF Reports
    path('motoristas/pdf/', views.motorista_pdf, name='motorista_pdf'),
    path('veiculos/pdf/', views.veiculo_pdf, name='veiculo_pdf'),
    path('multas/pdf/', views.multa_pdf, name='multa_pdf'),
    path('manutencoes/pdf/', views.manutencao_pdf, name='manutencao_pdf'),
    path('viagens/pdf/', views.viagem_pdf, name='viagem_pdf'),
    
    # Import
    path('viagens/importar/', views.ImportTravelView.as_view(), name='viagem_import'),
    path('viagens/modelo/', views.DownloadTravelTemplateView.as_view(), name='viagem_download_template'),
]

