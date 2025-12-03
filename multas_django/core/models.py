from django.db import models
from django.core.validators import MinValueValidator

class Motorista(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True, db_index=True)
    cnh = models.CharField(max_length=20, unique=True, db_index=True)
    validade_cnh = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['validade_cnh']),
            models.Index(fields=['-created_at']),
        ]
        verbose_name = 'Motorista'
        verbose_name_plural = 'Motoristas'

    def __str__(self):
        return f"{self.nome} ({self.cnh})"

class Veiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True, db_index=True)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField(db_index=True)
    renavam = models.CharField(max_length=20, unique=True)
    km_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)], db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['km_atual']),
            models.Index(fields=['ano']),
            models.Index(fields=['-created_at']),
        ]
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'

    def __str__(self):
        return f"{self.modelo} - {self.placa}"

class Viagem(models.Model):
    data = models.DateField(db_index=True)
    hora_saida = models.TimeField()
    motorista = models.ForeignKey(Motorista, on_delete=models.PROTECT, db_index=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, db_index=True)
    origem = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    distancia = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['-data']),
            models.Index(fields=['motorista', 'data']),
            models.Index(fields=['veiculo', 'data']),
        ]
        verbose_name = 'Viagem'
        verbose_name_plural = 'Viagens'
        ordering = ['-data', '-hora_saida']

    def __str__(self):
        return f"{self.data} - {self.origem} -> {self.destino}"


class Multa(models.Model):
    data = models.DateField(db_index=True)
    hora_infracao = models.TimeField(null=True, blank=True)
    local = models.CharField(max_length=200)
    tipo_infracao = models.CharField(max_length=100, db_index=True)
    descricao = models.TextField(blank=True)
    motorista = models.ForeignKey(Motorista, on_delete=models.PROTECT, db_index=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, db_index=True)
    viagem = models.ForeignKey(Viagem, on_delete=models.SET_NULL, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['-data']),
            models.Index(fields=['motorista', 'data']),
            models.Index(fields=['veiculo', 'data']),
            models.Index(fields=['tipo_infracao']),
        ]
        verbose_name = 'Multa'
        verbose_name_plural = 'Multas'
        ordering = ['-data']

    def __str__(self):
        return f"{self.tipo_infracao} - {self.veiculo.placa} ({self.data})"

class Manutencao(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, db_index=True)
    data = models.DateField(db_index=True)
    tipo_servico = models.CharField(max_length=100, db_index=True)
    descricao = models.TextField(blank=True)
    km_realizado = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    proximo_servico_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    proximo_servico_data = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['-data']),
            models.Index(fields=['veiculo', 'data']),
            models.Index(fields=['tipo_servico']),
            models.Index(fields=['proximo_servico_km']),
        ]
        verbose_name = 'Manutenção'
        verbose_name_plural = 'Manutenções'
        ordering = ['-data']

    def __str__(self):
        return f"{self.tipo_servico} - {self.veiculo.placa}"
