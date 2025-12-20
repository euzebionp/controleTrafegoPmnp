from django import forms
from django.contrib import messages
from .models import Viagem, Veiculo, Manutencao

class ViagemImportForm(forms.Form):
    arquivo_excel = forms.FileField(
        label='Arquivo Excel',
        help_text='Selecione o arquivo .xlsx com os dados das viagens'
    )

class ViagemForm(forms.ModelForm):
    km_atual = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label='KM Atual do Veículo',
        help_text='Informe a quilometragem atual do veículo após a viagem'
    )
    
    class Meta:
        model = Viagem
        fields = ['data', 'hora_saida', 'motorista', 'veiculo', 'origem', 'destino', 'distancia', 'km_atual']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_saida': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing, populate km_atual with current vehicle km
        if self.instance.pk and self.instance.veiculo:
            self.fields['km_atual'].initial = self.instance.veiculo.km_atual
        
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            if field_name not in ['data', 'hora_saida']:
                field.widget.attrs['class'] = 'form-control'
        
        # Add Bootstrap class for FileInput if present (though ViagemForm doesn't use it, ViagemImportForm does)
        # But this is ViagemForm __init__. Checking ViagemImportForm is separate.

    def clean(self):
        cleaned_data = super().clean()
        veiculo = cleaned_data.get('veiculo')
        km_atual = cleaned_data.get('km_atual')
        distancia = cleaned_data.get('distancia')
        
        if veiculo and km_atual:
            # Validate that km_atual is not less than current vehicle km
            if km_atual < veiculo.km_atual:
                raise forms.ValidationError(
                    f'KM atual ({km_atual}) não pode ser menor que o KM atual do veículo ({veiculo.km_atual})'
                )
        
        return cleaned_data
    
    def save(self, commit=True, request=None):
        instance = super().save(commit=False)
        km_atual = self.cleaned_data.get('km_atual')
        
        if commit:
            instance.save()
            
            # Update vehicle km if km_atual is provided
            if km_atual and km_atual > 0:
                veiculo = instance.veiculo
                veiculo.km_atual = km_atual
                veiculo.save()
                
                # Check for maintenance alerts
                if request:
                    self.check_maintenance_alerts(veiculo, km_atual, request)
        
        return instance
    
    def check_maintenance_alerts(self, veiculo, km_atual, request):
        """Check if vehicle needs maintenance and add messages"""
        # Get the last maintenance for this vehicle
        last_maintenance = Manutencao.objects.filter(
            veiculo=veiculo
        ).order_by('-data').first()
        
        if last_maintenance and last_maintenance.proximo_servico_km:
            km_restante = last_maintenance.proximo_servico_km - km_atual
            
            if km_restante <= 0:
                messages.error(
                    request,
                    f'⚠️ MANUTENÇÃO VENCIDA! O veículo {veiculo} atingiu {km_atual} km. '
                    f'A revisão deveria ter sido feita aos {last_maintenance.proximo_servico_km} km. '
                    f'Agende a manutenção imediatamente!'
                )
            elif km_restante <= 1000:
                messages.warning(
                    request,
                    f'⚠️ MANUTENÇÃO PRÓXIMA! O veículo {veiculo} está com {km_atual} km. '
                    f'Faltam apenas {km_restante:.0f} km para a próxima revisão '
                    f'(prevista para {last_maintenance.proximo_servico_km} km). '
                    f'Agende a manutenção em breve!'
                )
            elif km_restante <= 2000:
                messages.info(
                    request,
                    f'ℹ️ Lembrete: O veículo {veiculo} está com {km_atual} km. '
                    f'Próxima manutenção em {km_restante:.0f} km '
                    f'({last_maintenance.proximo_servico_km} km total).'
                )
