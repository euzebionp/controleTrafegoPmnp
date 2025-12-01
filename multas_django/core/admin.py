from django.contrib import admin
from .models import Motorista, Veiculo, Viagem, Multa, Manutencao

@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'cnh', 'validade_cnh')
    search_fields = ('nome', 'cpf', 'cnh')

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modelo', 'ano', 'km_atual')
    search_fields = ('placa', 'modelo')

@admin.register(Viagem)
class ViagemAdmin(admin.ModelAdmin):
    list_display = ('data', 'motorista', 'veiculo', 'origem', 'destino', 'distancia')
    list_filter = ('data', 'motorista', 'veiculo')

@admin.register(Multa)
class MultaAdmin(admin.ModelAdmin):
    list_display = ('data', 'tipo_infracao', 'veiculo', 'motorista', 'valor')
    list_filter = ('tipo_infracao', 'veiculo', 'motorista')

@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'tipo_servico', 'veiculo', 'valor')
    list_filter = ('tipo_servico', 'veiculo')
