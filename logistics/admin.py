from django.contrib import admin
from .models import Motorista, Veiculo, Viagem, Manutencao, Multa


@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'cnh', 'validade_cnh']
    search_fields = ['nome', 'cpf', 'cnh']
    list_filter = ['validade_cnh']


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ['placa', 'modelo', 'ano', 'renavam', 'km_atual']
    search_fields = ['placa', 'modelo', 'renavam']
    list_filter = ['ano']


@admin.register(Viagem)
class ViagemAdmin(admin.ModelAdmin):
    list_display = ['data', 'motorista', 'veiculo', 'origem', 'destino', 'distancia']
    search_fields = ['origem', 'destino', 'motorista__nome', 'veiculo__placa']
    list_filter = ['data', 'motorista', 'veiculo']
    date_hierarchy = 'data'


@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'data', 'tipo_servico', 'km_realizado', 'proximo_servico_km', 'valor']
    search_fields = ['veiculo__placa', 'tipo_servico', 'descricao']
    list_filter = ['data', 'tipo_servico', 'veiculo']
    date_hierarchy = 'data'


@admin.register(Multa)
class MultaAdmin(admin.ModelAdmin):
    list_display = ['data', 'motorista', 'veiculo', 'tipo_infracao', 'local', 'valor']
    search_fields = ['motorista__nome', 'veiculo__placa', 'local', 'tipo_infracao']
    list_filter = ['data', 'tipo_infracao', 'motorista', 'veiculo']
    date_hierarchy = 'data'
