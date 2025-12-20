from django import forms
from .models import Motorista, Veiculo, Viagem, Manutencao, Multa


class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista
        fields = ['nome', 'cpf', 'cnh', 'validade_cnh']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'cnh': forms.TextInput(attrs={'class': 'form-control'}),
            'validade_cnh': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo', 'ano', 'renavam', 'km_atual']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ABC-1234'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'renavam': forms.TextInput(attrs={'class': 'form-control'}),
            'km_atual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = ['data', 'motorista', 'veiculo', 'origem', 'destino', 'hora_saida', 'distancia', 'km_atual']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'motorista': forms.Select(attrs={'class': 'form-control'}),
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'origem': forms.TextInput(attrs={'class': 'form-control'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_saida': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'distancia': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'km_atual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['veiculo', 'data', 'tipo_servico', 'descricao', 'km_realizado', 'proximo_servico_km', 'proximo_servico_data', 'valor']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo_servico': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'km_realizado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'proximo_servico_km': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'proximo_servico_data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class MultaForm(forms.ModelForm):
    class Meta:
        model = Multa
        fields = ['data', 'hora_infracao', 'local', 'tipo_infracao', 'descricao', 'motorista', 'veiculo', 'valor', 'viagem']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_infracao': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_infracao': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'motorista': forms.Select(attrs={'class': 'form-control'}),
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'viagem': forms.Select(attrs={'class': 'form-control'}),
        }


class ViagemImportForm(forms.Form):
    arquivo_excel = forms.FileField(
        label='Arquivo Excel',
        help_text='Selecione o arquivo .xlsx com os dados das viagens',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
