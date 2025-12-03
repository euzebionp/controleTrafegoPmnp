import django_filters
from django import forms
from .models import Viagem, Multa, Manutencao, Motorista, Veiculo

class ViagemFilter(django_filters.FilterSet):
    data_inicio = django_filters.DateFilter(
        field_name='data', 
        lookup_expr='gte',
        label='Data Início',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    data_fim = django_filters.DateFilter(
        field_name='data', 
        lookup_expr='lte',
        label='Data Fim',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    distancia_min = django_filters.NumberFilter(
        field_name='distancia', 
        lookup_expr='gte',
        label='Distância Mínima (km)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    distancia_max = django_filters.NumberFilter(
        field_name='distancia', 
        lookup_expr='lte',
        label='Distância Máxima (km)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    motorista = django_filters.ModelChoiceFilter(
        queryset=Motorista.objects.all(),
        label='Motorista',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    veiculo = django_filters.ModelChoiceFilter(
        queryset=Veiculo.objects.all(),
        label='Veículo',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    origem = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Origem',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a origem'})
    )
    destino = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Destino',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o destino'})
    )
    
    class Meta:
        model = Viagem
        fields = []

class MultaFilter(django_filters.FilterSet):
    data_inicio = django_filters.DateFilter(
        field_name='data', 
        lookup_expr='gte',
        label='Data Início',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    data_fim = django_filters.DateFilter(
        field_name='data', 
        lookup_expr='lte',
        label='Data Fim',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    valor_min = django_filters.NumberFilter(
        field_name='valor', 
        lookup_expr='gte',
        label='Valor Mínimo (R$)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    valor_max = django_filters.NumberFilter(
        field_name='valor', 
        lookup_expr='lte',
        label='Valor Máximo (R$)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    tipo_infracao = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Tipo de Infração',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o tipo'})
    )
    motorista = django_filters.ModelChoiceFilter(
        queryset=Motorista.objects.all(),
        label='Motorista',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    veiculo = django_filters.ModelChoiceFilter(
        queryset=Veiculo.objects.all(),
        label='Veículo',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    local = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Local',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o local'})
    )
    
    class Meta:
        model = Multa
        fields = []

class ManutencaoFilter(django_filters.FilterSet):
    data_inicio = django_filters.DateFilter(
        field_name='data', 
        lookup_expr='gte',
        label='Data Início',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    data_fim = django_filters.DateFilter(
        field_name='data', 
        lookup_expr='lte',
        label='Data Fim',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    valor_min = django_filters.NumberFilter(
        field_name='valor', 
        lookup_expr='gte',
        label='Valor Mínimo (R$)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    valor_max = django_filters.NumberFilter(
        field_name='valor', 
        lookup_expr='lte',
        label='Valor Máximo (R$)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    tipo_servico = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Tipo de Serviço',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o tipo'})
    )
    veiculo = django_filters.ModelChoiceFilter(
        queryset=Veiculo.objects.all(),
        label='Veículo',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Manutencao
        fields = []
