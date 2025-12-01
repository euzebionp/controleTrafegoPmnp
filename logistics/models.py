from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Motorista(models.Model):
    """Driver model"""
    nome = models.CharField(max_length=200, verbose_name="Nome")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    cnh = models.CharField(max_length=20, unique=True, verbose_name="CNH")
    validade_cnh = models.DateField(verbose_name="Validade da CNH")

    class Meta:
        verbose_name = "Motorista"
        verbose_name_plural = "Motoristas"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    """Vehicle model"""
    placa = models.CharField(max_length=10, unique=True, verbose_name="Placa")
    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    ano = models.IntegerField(validators=[MinValueValidator(1900)], verbose_name="Ano")
    renavam = models.CharField(max_length=20, unique=True, verbose_name="RENAVAM")
    km_atual = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="KM Atual")

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ['placa']

    def __str__(self):
        return f"{self.placa} - {self.modelo}"


class Viagem(models.Model):
    """Travel model"""
    data = models.DateField(verbose_name="Data")
    motorista = models.ForeignKey(Motorista, on_delete=models.PROTECT, verbose_name="Motorista")
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, verbose_name="Veículo")
    origem = models.CharField(max_length=200, default='', verbose_name="Origem")
    destino = models.CharField(max_length=200, verbose_name="Destino")
    hora_saida = models.TimeField(verbose_name="Hora de Saída")
    distancia = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name="Distância (km)")
    km_atual = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)], verbose_name="KM no Momento")

    class Meta:
        verbose_name = "Viagem"
        verbose_name_plural = "Viagens"
        ordering = ['-data', '-hora_saida']

    def __str__(self):
        return f"{self.data} - {self.origem} → {self.destino}"

    def save(self, *args, **kwargs):
        """Override save to update vehicle mileage"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Update vehicle mileage when creating new travel
            if self.km_atual:
                self.veiculo.km_atual = self.km_atual
            elif self.distancia > 0:
                self.veiculo.km_atual += self.distancia
            self.veiculo.save()


class Manutencao(models.Model):
    """Maintenance model"""
    TIPO_SERVICO_CHOICES = [
        ('Troca de Óleo', 'Troca de Óleo'),
        ('Revisão', 'Revisão'),
        ('Troca de Pneus', 'Troca de Pneus'),
        ('Alinhamento', 'Alinhamento'),
        ('Balanceamento', 'Balanceamento'),
        ('Freios', 'Freios'),
        ('Suspensão', 'Suspensão'),
        ('Outros', 'Outros'),
    ]
    
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, verbose_name="Veículo")
    data = models.DateField(verbose_name="Data")
    tipo_servico = models.CharField(max_length=50, choices=TIPO_SERVICO_CHOICES, verbose_name="Tipo de Serviço")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    km_realizado = models.FloatField(validators=[MinValueValidator(0)], verbose_name="KM Realizado")
    proximo_servico_km = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)], verbose_name="Próximo Serviço (KM)")
    proximo_servico_data = models.DateField(null=True, blank=True, verbose_name="Próximo Serviço (Data)")
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Valor")

    class Meta:
        verbose_name = "Manutenção"
        verbose_name_plural = "Manutenções"
        ordering = ['-data']

    def __str__(self):
        return f"{self.veiculo.placa} - {self.tipo_servico} ({self.data})"

    def is_due(self):
        """Check if maintenance is due based on current vehicle mileage"""
        if self.proximo_servico_km:
            km_diff = self.proximo_servico_km - self.veiculo.km_atual
            if km_diff <= 0:
                return True, f"⚠️ MANUTENÇÃO VENCIDA! O veículo atingiu {self.veiculo.km_atual} km. Próxima revisão era aos {self.proximo_servico_km} km."
            elif km_diff <= 1000:
                return True, f"⚠️ Manutenção Próxima! Faltam {km_diff:.0f} km para a revisão."
        return False, None


class Multa(models.Model):
    """Fine model"""
    TIPO_INFRACAO_CHOICES = [
        ('Excesso de Velocidade', 'Excesso de Velocidade'),
        ('Estacionamento Irregular', 'Estacionamento Irregular'),
        ('Avanço de Sinal', 'Avanço de Sinal'),
        ('Uso de Celular', 'Uso de Celular'),
        ('Falta de Cinto', 'Falta de Cinto'),
        ('Documentação Irregular', 'Documentação Irregular'),
        ('Outros', 'Outros'),
    ]
    
    data = models.DateField(verbose_name="Data")
    hora_infracao = models.TimeField(null=True, blank=True, verbose_name="Hora da Infração")
    local = models.CharField(max_length=200, verbose_name="Local")
    tipo_infracao = models.CharField(max_length=100, choices=TIPO_INFRACAO_CHOICES, verbose_name="Tipo de Infração")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    motorista = models.ForeignKey(Motorista, on_delete=models.PROTECT, verbose_name="Motorista")
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, verbose_name="Veículo")
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Valor")
    viagem = models.ForeignKey(Viagem, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Viagem")

    class Meta:
        verbose_name = "Multa"
        verbose_name_plural = "Multas"
        ordering = ['-data']

    def __str__(self):
        return f"{self.data} - {self.tipo_infracao} - {self.motorista.nome}"
