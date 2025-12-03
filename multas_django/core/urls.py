from django.urls import path
from .views import (
    DashboardView,
    MotoristaListView, MotoristaCreateView, MotoristaUpdateView, MotoristaDeleteView,
    VeiculoListView, VeiculoCreateView, VeiculoUpdateView, VeiculoDeleteView,
    ViagemListView, ViagemCreateView, ViagemUpdateView, ViagemDeleteView,
    MultaListView, MultaCreateView, MultaUpdateView, MultaDeleteView,
    ManutencaoListView, ManutencaoCreateView, ManutencaoUpdateView, ManutencaoDeleteView,
    relatorio_viagens_pdf, relatorio_viagens_excel,
    relatorio_multas_pdf, relatorio_multas_excel
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Motorista URLs
    path('motoristas/', MotoristaListView.as_view(), name='motorista_list'),
    path('motoristas/novo/', MotoristaCreateView.as_view(), name='motorista_create'),
    path('motoristas/<int:pk>/editar/', MotoristaUpdateView.as_view(), name='motorista_update'),
    path('motoristas/<int:pk>/excluir/', MotoristaDeleteView.as_view(), name='motorista_delete'),

    # Veiculo URLs
    path('veiculos/', VeiculoListView.as_view(), name='veiculo_list'),
    path('veiculos/novo/', VeiculoCreateView.as_view(), name='veiculo_create'),
    path('veiculos/<int:pk>/editar/', VeiculoUpdateView.as_view(), name='veiculo_update'),
    path('veiculos/<int:pk>/excluir/', VeiculoDeleteView.as_view(), name='veiculo_delete'),

    # Viagem URLs
    path('viagens/', ViagemListView.as_view(), name='viagem_list'),
    path('viagens/novo/', ViagemCreateView.as_view(), name='viagem_create'),
    path('viagens/<int:pk>/editar/', ViagemUpdateView.as_view(), name='viagem_update'),
    path('viagens/<int:pk>/excluir/', ViagemDeleteView.as_view(), name='viagem_delete'),

    # Multa URLs
    path('multas/', MultaListView.as_view(), name='multa_list'),
    path('multas/novo/', MultaCreateView.as_view(), name='multa_create'),
    path('multas/<int:pk>/editar/', MultaUpdateView.as_view(), name='multa_update'),
    path('multas/<int:pk>/excluir/', MultaDeleteView.as_view(), name='multa_delete'),

    # Manutencao URLs
    path('manutencoes/', ManutencaoListView.as_view(), name='manutencao_list'),
    path('manutencoes/novo/', ManutencaoCreateView.as_view(), name='manutencao_create'),
    path('manutencoes/<int:pk>/editar/', ManutencaoUpdateView.as_view(), name='manutencao_update'),
    path('manutencoes/<int:pk>/excluir/', ManutencaoDeleteView.as_view(), name='manutencao_delete'),
    
    # Report URLs
    path('relatorios/viagens/pdf/', relatorio_viagens_pdf, name='relatorio_viagens_pdf'),
    path('relatorios/viagens/excel/', relatorio_viagens_excel, name='relatorio_viagens_excel'),
    path('relatorios/multas/pdf/', relatorio_multas_pdf, name='relatorio_multas_pdf'),
    path('relatorios/multas/excel/', relatorio_multas_excel, name='relatorio_multas_excel'),
]
