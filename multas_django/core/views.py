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
from .reports import generate_pdf_report
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
# Report Export Views
def relatorio_motoristas_pdf(request):
    """Exporta relatório de motoristas em PDF"""
    motoristas = Motorista.objects.all().order_by('nome')
    headers = ['Nome', 'CPF', 'CNH', 'Validade CNH']
    data = []
    for m in motoristas:
        data.append([
            m.nome,
            m.cpf,
            m.cnh,
            m.validade_cnh.strftime('%d/%m/%Y') if m.validade_cnh else '-'
        ])
    
    return generate_pdf_report("Relatório de Motoristas", data, headers, "relatorio_motoristas.pdf")

def relatorio_veiculos_pdf(request):
    """Exporta relatório de veículos em PDF"""
    veiculos = Veiculo.objects.all().order_by('placa')
    headers = ['Placa', 'Modelo', 'Ano', 'Renavam', 'KM Atual']
    data = []
    for v in veiculos:
        data.append([
            v.placa,
            v.modelo,
            str(v.ano),
            v.renavam,
            str(v.km_atual)
        ])
    
    return generate_pdf_report("Relatório de Veículos", data, headers, "relatorio_veiculos.pdf")

def relatorio_multas_pdf(request):
    """Exporta relatório de multas em PDF"""
    multas = Multa.objects.select_related('motorista', 'veiculo').order_by('-data')
    headers = ['Data', 'Hora', 'Local', 'Motorista', 'Veículo', 'Valor']
    data = []
    for m in multas:
        data.append([
            m.data.strftime('%d/%m/%Y'),
            m.hora_infracao.strftime('%H:%M') if m.hora_infracao else '-',
            m.local,
            m.motorista.nome if m.motorista else '-',
            m.veiculo.placa if m.veiculo else '-',
            f"R$ {m.valor:.2f}"
        ])
    
    return generate_pdf_report("Relatório de Multas", data, headers, "relatorio_multas.pdf")

def relatorio_manutencoes_pdf(request):
    """Exporta relatório de manutenções em PDF"""
    manutencoes = Manutencao.objects.select_related('veiculo').order_by('-data')
    headers = ['Veículo', 'Data', 'Tipo', 'Descrição', 'Valor']
    data = []
    for m in manutencoes:
        data.append([
            m.veiculo.placa if m.veiculo else '-',
            m.data.strftime('%d/%m/%Y'),
            m.tipo_servico,
            m.descricao,
            f"R$ {m.valor:.2f}"
        ])
    
    return generate_pdf_report("Relatório de Manutenções", data, headers, "relatorio_manutencoes.pdf")

def relatorio_viagens_pdf(request):
    """Exporta relatório de viagens em PDF"""
    viagens = Viagem.objects.select_related('motorista', 'veiculo').order_by('-data')
    headers = ['Data', 'Saída', 'Chegada', 'Motorista', 'Veículo', 'Destino']
    data = []
    for v in viagens:
        data.append([
            v.data.strftime('%d/%m/%Y'),
            v.hora_saida.strftime('%H:%M') if v.hora_saida else '-',
            v.hora_chegada.strftime('%H:%M') if v.hora_chegada else '-',
            v.motorista.nome if v.motorista else '-',
            v.veiculo.placa if v.veiculo else '-',
            v.destino
        ])
    return generate_pdf_report("Relatório de Viagens", data, headers, "relatorio_viagens.pdf")

