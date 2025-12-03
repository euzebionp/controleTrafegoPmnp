from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import F, Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from .models import Motorista, Veiculo, Viagem, Multa, Manutencao
from .forms import ViagemForm
from .reports import (gerar_relatorio_viagens_pdf, gerar_relatorio_multas_pdf,
                      gerar_relatorio_viagens_excel, gerar_relatorio_multas_excel)
    context_object_name = 'motoristas'

class MotoristaCreateView(LoginRequiredMixin, CreateView):
    model = Motorista
    template_name = 'drivers/driver_form.html'
    fields = ['nome', 'cpf', 'cnh', 'validade_cnh']
    success_url = reverse_lazy('motorista_list')

class MotoristaUpdateView(LoginRequiredMixin, UpdateView):
    model = Motorista
    template_name = 'drivers/driver_form.html'
    fields = ['nome', 'cpf', 'cnh', 'validade_cnh']
    success_url = reverse_lazy('motorista_list')

class MotoristaDeleteView(LoginRequiredMixin, DeleteView):
    model = Motorista
    template_name = 'drivers/driver_confirm_delete.html'
    success_url = reverse_lazy('motorista_list')

# Veiculo Views
class VeiculoListView(LoginRequiredMixin, ListView):
    model = Veiculo
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'veiculos'

class VeiculoCreateView(LoginRequiredMixin, CreateView):
    model = Veiculo
    template_name = 'vehicles/vehicle_form.html'
    fields = ['placa', 'modelo', 'ano', 'renavam', 'km_atual']
    success_url = reverse_lazy('veiculo_list')

class VeiculoUpdateView(LoginRequiredMixin, UpdateView):
    model = Veiculo
    template_name = 'vehicles/vehicle_form.html'
    fields = ['placa', 'modelo', 'ano', 'renavam', 'km_atual']
    success_url = reverse_lazy('veiculo_list')

class VeiculoDeleteView(LoginRequiredMixin, DeleteView):
    model = Veiculo
    template_name = 'vehicles/vehicle_confirm_delete.html'
    success_url = reverse_lazy('veiculo_list')

# Viagem Views
class ViagemListView(LoginRequiredMixin, ListView):
    model = Viagem
    template_name = 'travels/travel_list.html'
    context_object_name = 'viagens'
    paginate_by = 50
    
    def get_queryset(self):
        return Viagem.objects.select_related(
            'motorista', 'veiculo'
        ).order_by('-data', '-hora_saida')

class ViagemCreateView(LoginRequiredMixin, CreateView):
    model = Viagem
    form_class = ViagemForm
    template_name = 'travels/travel_form.html'
    success_url = reverse_lazy('viagem_list')
    
    def form_valid(self, form):
        form.save(commit=True, request=self.request)
        return super().form_valid(form)

class ViagemUpdateView(LoginRequiredMixin, UpdateView):
    model = Viagem
    form_class = ViagemForm
    template_name = 'travels/travel_form.html'
    success_url = reverse_lazy('viagem_list')
    
    def form_valid(self, form):
        form.save(commit=True, request=self.request)
        return super().form_valid(form)

class ViagemDeleteView(LoginRequiredMixin, DeleteView):
    model = Viagem
    template_name = 'travels/travel_confirm_delete.html'
    success_url = reverse_lazy('viagem_list')

# Multa Views
class MultaListView(LoginRequiredMixin, ListView):
    model = Multa
    template_name = 'fines/fine_list.html'
    context_object_name = 'multas'
    paginate_by = 50
    
    def get_queryset(self):
        return Multa.objects.select_related(
            'motorista', 'veiculo', 'viagem'
        ).order_by('-data')

class MultaCreateView(LoginRequiredMixin, CreateView):
    model = Multa
    template_name = 'fines/fine_form.html'
    fields = ['data', 'hora_infracao', 'local', 'tipo_infracao', 'descricao', 'motorista', 'veiculo', 'viagem', 'valor']
    success_url = reverse_lazy('multa_list')

class MultaUpdateView(LoginRequiredMixin, UpdateView):
    model = Multa
    template_name = 'fines/fine_form.html'
    fields = ['data', 'hora_infracao', 'local', 'tipo_infracao', 'descricao', 'motorista', 'veiculo', 'viagem', 'valor']
    success_url = reverse_lazy('multa_list')

class MultaDeleteView(LoginRequiredMixin, DeleteView):
    model = Multa
    template_name = 'fines/fine_confirm_delete.html'
    success_url = reverse_lazy('multa_list')

# Manutencao Views
class ManutencaoListView(LoginRequiredMixin, ListView):
    model = Manutencao
    template_name = 'maintenance/maintenance_list.html'
    context_object_name = 'manutencoes'
    paginate_by = 50
    
    def get_queryset(self):
        return Manutencao.objects.select_related(
            'veiculo'
        ).order_by('-data')

class ManutencaoCreateView(LoginRequiredMixin, CreateView):
    model = Manutencao
    template_name = 'maintenance/maintenance_form.html'
    fields = ['veiculo', 'data', 'tipo_servico', 'descricao', 'km_realizado', 'proximo_servico_km', 'proximo_servico_data', 'valor']
    success_url = reverse_lazy('manutencao_list')

class ManutencaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Manutencao
    template_name = 'maintenance/maintenance_form.html'
    fields = ['veiculo', 'data', 'tipo_servico', 'descricao', 'km_realizado', 'proximo_servico_km', 'proximo_servico_data', 'valor']
    success_url = reverse_lazy('manutencao_list')

class ManutencaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Manutencao
    template_name = 'maintenance/maintenance_confirm_delete.html'
    success_url = reverse_lazy('manutencao_list')

# Report Export Views
def relatorio_viagens_pdf(request):
    """Exporta relatório de viagens em PDF"""
    viagens = Viagem.objects.select_related('motorista', 'veiculo').order_by('-data')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_viagens.pdf"'
    return gerar_relatorio_viagens_pdf(viagens, response)

def relatorio_viagens_excel(request):
    """Exporta relatório de viagens em Excel"""
    viagens = Viagem.objects.select_related('motorista', 'veiculo').order_by('-data')
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="relatorio_viagens.xlsx"'
    return gerar_relatorio_viagens_excel(viagens, response)

def relatorio_multas_pdf(request):
    """Exporta relatório de multas em PDF"""
    multas = Multa.objects.select_related('motorista', 'veiculo').order_by('-data')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_multas.pdf"'
    return gerar_relatorio_multas_pdf(multas, response)

def relatorio_multas_excel(request):
    """Exporta relatório de multas em Excel"""
    multas = Multa.objects.select_related('motorista', 'veiculo').order_by('-data')
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="relatorio_multas.xlsx"'
    return gerar_relatorio_multas_excel(multas, response)
