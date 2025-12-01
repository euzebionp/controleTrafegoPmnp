from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Motorista, Veiculo, Viagem, Multa, Manutencao

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_motoristas'] = Motorista.objects.count()
        context['total_veiculos'] = Veiculo.objects.count()
        context['total_viagens'] = Viagem.objects.count()
        context['total_multas'] = Multa.objects.count()
        context['total_manutencoes'] = Manutencao.objects.count()
        return context

# Motorista Views
class MotoristaListView(ListView):
    model = Motorista
    template_name = 'drivers/driver_list.html'
    context_object_name = 'motoristas'

class MotoristaCreateView(CreateView):
    model = Motorista
    template_name = 'drivers/driver_form.html'
    fields = ['nome', 'cpf', 'cnh', 'validade_cnh']
    success_url = reverse_lazy('motorista_list')

class MotoristaUpdateView(UpdateView):
    model = Motorista
    template_name = 'drivers/driver_form.html'
    fields = ['nome', 'cpf', 'cnh', 'validade_cnh']
    success_url = reverse_lazy('motorista_list')

class MotoristaDeleteView(DeleteView):
    model = Motorista
    template_name = 'drivers/driver_confirm_delete.html'
    success_url = reverse_lazy('motorista_list')

# Veiculo Views
class VeiculoListView(ListView):
    model = Veiculo
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'veiculos'

class VeiculoCreateView(CreateView):
    model = Veiculo
    template_name = 'vehicles/vehicle_form.html'
    fields = ['placa', 'modelo', 'ano', 'renavam', 'km_atual']
    success_url = reverse_lazy('veiculo_list')

class VeiculoUpdateView(UpdateView):
    model = Veiculo
    template_name = 'vehicles/vehicle_form.html'
    fields = ['placa', 'modelo', 'ano', 'renavam', 'km_atual']
    success_url = reverse_lazy('veiculo_list')

class VeiculoDeleteView(DeleteView):
    model = Veiculo
    template_name = 'vehicles/vehicle_confirm_delete.html'
    success_url = reverse_lazy('veiculo_list')

# Viagem Views
class ViagemListView(ListView):
    model = Viagem
    template_name = 'travels/travel_list.html'
    context_object_name = 'viagens'

class ViagemCreateView(CreateView):
    model = Viagem
    template_name = 'travels/travel_form.html'
    fields = ['data', 'hora_saida', 'motorista', 'veiculo', 'origem', 'destino', 'distancia']
    success_url = reverse_lazy('viagem_list')

class ViagemUpdateView(UpdateView):
    model = Viagem
    template_name = 'travels/travel_form.html'
    fields = ['data', 'hora_saida', 'motorista', 'veiculo', 'origem', 'destino', 'distancia']
    success_url = reverse_lazy('viagem_list')

class ViagemDeleteView(DeleteView):
    model = Viagem
    template_name = 'travels/travel_confirm_delete.html'
    success_url = reverse_lazy('viagem_list')

# Multa Views
class MultaListView(ListView):
    model = Multa
    template_name = 'fines/fine_list.html'
    context_object_name = 'multas'

class MultaCreateView(CreateView):
    model = Multa
    template_name = 'fines/fine_form.html'
    fields = ['data', 'hora_infracao', 'local', 'tipo_infracao', 'descricao', 'motorista', 'veiculo', 'viagem', 'valor']
    success_url = reverse_lazy('multa_list')

class MultaUpdateView(UpdateView):
    model = Multa
    template_name = 'fines/fine_form.html'
    fields = ['data', 'hora_infracao', 'local', 'tipo_infracao', 'descricao', 'motorista', 'veiculo', 'viagem', 'valor']
    success_url = reverse_lazy('multa_list')

class MultaDeleteView(DeleteView):
    model = Multa
    template_name = 'fines/fine_confirm_delete.html'
    success_url = reverse_lazy('multa_list')

# Manutencao Views
class ManutencaoListView(ListView):
    model = Manutencao
    template_name = 'maintenance/maintenance_list.html'
    context_object_name = 'manutencoes'

class ManutencaoCreateView(CreateView):
    model = Manutencao
    template_name = 'maintenance/maintenance_form.html'
    fields = ['veiculo', 'data', 'tipo_servico', 'descricao', 'km_realizado', 'proximo_servico_km', 'proximo_servico_data', 'valor']
    success_url = reverse_lazy('manutencao_list')

class ManutencaoUpdateView(UpdateView):
    model = Manutencao
    template_name = 'maintenance/maintenance_form.html'
    fields = ['veiculo', 'data', 'tipo_servico', 'descricao', 'km_realizado', 'proximo_servico_km', 'proximo_servico_data', 'valor']
    success_url = reverse_lazy('manutencao_list')

class ManutencaoDeleteView(DeleteView):
    model = Manutencao
    template_name = 'maintenance/maintenance_confirm_delete.html'
    success_url = reverse_lazy('manutencao_list')
