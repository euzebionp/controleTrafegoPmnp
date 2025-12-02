from django.db import models
from django.core.validators import MinValueValidator

class Motorista(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    cnh = models.CharField(max_length=20, unique=True)
    validade_cnh = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.cnh})"

class Veiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    renavam = models.CharField(max_length=20, unique=True)
    km_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.modelo} - {self.placa}"

class Viagem(models.Model):
    data = models.DateField()
    hora_saida = models.TimeField()
    motorista = models.ForeignKey(Motorista, on_delete=models.PROTECT)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    origem = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    distancia = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.data} - {self.origem} -> {self.destino}"


class Multa(models.Model):
    data = models.DateField()
    hora_infracao = models.TimeField(null=True, blank=True)
    local = models.CharField(max_length=200)
    tipo_infracao = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    motorista = models.ForeignKey(Motorista, on_delete=models.PROTECT)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    viagem = models.ForeignKey(Viagem, on_delete=models.SET_NULL, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo_infracao} - {self.veiculo.placa} ({self.data})"

class Manutencao(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    data = models.DateField()
    tipo_servico = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    km_realizado = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    proximo_servico_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    proximo_servico_data = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo_servico} - {self.veiculo.placa}"
