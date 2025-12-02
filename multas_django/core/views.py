from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import F
from .models import Motorista, Veiculo, Viagem, Multa, Manutencao
from .forms import ViagemForm

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_motoristas'] = Motorista.objects.count()
        context['total_veiculos'] = Veiculo.objects.count()
        context['total_viagens'] = Viagem.objects.count()
        context['total_multas'] = Multa.objects.count()
        context['total_manutencoes'] = Manutencao.objects.count()

        # Maintenance Alerts
        alerts = []
        # Check for vehicles with maintenance due by KM
        # We need to find the last maintenance for each vehicle to know the next service km
        # For simplicity, we can query vehicles and their maintenances. 
        # A more optimized way would be to have 'proximo_servico_km' on the Vehicle model or a separate status table.
        # Here we will iterate over vehicles for the migration scope.
        veiculos = Veiculo.objects.all()
        for veiculo in veiculos:
            last_maintenance = Manutencao.objects.filter(veiculo=veiculo).order_by('-data').first()
            if last_maintenance and last_maintenance.proximo_servico_km:
                if veiculo.km_atual >= last_maintenance.proximo_servico_km:
                    alerts.append({
                        'type': 'danger',
                        'message': f"MANUTENÇÃO VENCIDA! {veiculo} atingiu {veiculo.km_atual} km. Revisão era aos {last_maintenance.proximo_servico_km} km."
                    })
                elif (last_maintenance.proximo_servico_km - veiculo.km_atual) <= 1000:
                    remaining = last_maintenance.proximo_servico_km - veiculo.km_atual
                    alerts.append({
                        'type': 'warning',
                        'message': f"Manutenção Próxima! {veiculo} - Faltam {remaining:.0f} km."
                    })
        
        context['alerts'] = alerts
        return context

# Motorista Views
class MotoristaListView(LoginRequiredMixin, ListView):
    model = Motorista
    template_name = 'drivers/driver_list.html'
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
