
import os
import sys
import django
import openpyxl
from datetime import date, time

# Setup Django environment
sys.path.append(os.path.join(os.getcwd(), 'multas_django'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') # Assuming config.settings based on urls.py path
try:
    from multas_django.config import settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multas_django.config.settings')
except ImportError:
    pass

# Try standard path
if 'multas_django' in os.listdir('.'):
     sys.path.append(os.path.join(os.getcwd(), 'multas_django'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "multas_django.config.settings")

django.setup()

from core.models import Motorista, Veiculo

def create_test_file():
    motorista = Motorista.objects.first()
    veiculo = Veiculo.objects.first()
    
    if not motorista:
        print("Creating dummy motorista...")
        motorista = Motorista.objects.create(nome="Motorista Teste", cpf="12345678901", cnh="123456789", validade_cnh=date(2025,1,1))
        
    if not veiculo:
        print("Creating dummy veiculo...")
        veiculo = Veiculo.objects.create(placa="ABC1234", modelo="Modelo Teste", ano=2020, renavam="12345678901", km_atual=1000)

    print(f"Using Motorista: {motorista.cpf}, Veiculo: {veiculo.placa}")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Modelo Importação Viagens"
    
    headers = ['Data (DD/MM/AAAA)', 'Hora Saida (HH:MM)', 'CPF Motorista (apenas números)', 'Placa Veiculo', 'Origem', 'Destino', 'Distancia (KM)']
    ws.append(headers)
    
    # Add a valid row
    ws.append([
        date(2023, 10, 25),
        time(8, 0),
        motorista.cpf,
        veiculo.placa,
        "Sao Paulo",
        "Rio de Janeiro",
        400
    ])

    filename = 'test_import.xlsx'
    wb.save(filename)
    print(f"Created {filename} at {os.path.abspath(filename)}")

if __name__ == "__main__":
    create_test_file()
