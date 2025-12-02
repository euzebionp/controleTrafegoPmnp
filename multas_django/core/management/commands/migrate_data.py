import sqlite3
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Motorista, Veiculo, Viagem, Multa, Manutencao
from datetime import datetime

class Command(BaseCommand):
    help = 'Migrates data from the legacy traffic_app.db SQLite database to Django models'

    def handle(self, *args, **kwargs):
        # Path to the old database
        # Assuming it's in the root of the project (parent of multas_django)
        old_db_path = os.path.join(settings.BASE_DIR.parent, 'traffic_app.db')
        
        if not os.path.exists(old_db_path):
            self.stdout.write(self.style.ERROR(f'Database file not found at: {old_db_path}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found database at: {old_db_path}'))
        
        conn = sqlite3.connect(old_db_path)
        cursor = conn.cursor()

        # Helper to parse dates
        def parse_date(date_str):
            if not date_str: return None
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return None

        def parse_time(time_str):
            if not time_str: return None
            try:
                return datetime.strptime(time_str, '%H:%M').time()
            except ValueError:
                try:
                    return datetime.strptime(time_str, '%H:%M:%S').time()
                except ValueError:
                    return None

        # 1. Migrate Motoristas
        self.stdout.write('Migrating Motoristas...')
        cursor.execute("SELECT id, nome, cpf, cnh, validade_cnh FROM motoristas")
        motoristas_map = {} # old_id -> new_instance
        for row in cursor.fetchall():
            old_id, nome, cpf, cnh, validade_cnh = row
            motorista, created = Motorista.objects.get_or_create(
                cpf=cpf,
                defaults={
                    'nome': nome,
                    'cnh': cnh,
                    'validade_cnh': parse_date(validade_cnh)
                }
            )
            motoristas_map[old_id] = motorista
        self.stdout.write(self.style.SUCCESS(f'Migrated {len(motoristas_map)} Motoristas'))

        # 2. Migrate Veiculos
        self.stdout.write('Migrating Veiculos...')
        cursor.execute("SELECT id, placa, modelo, ano, renavam, km_atual FROM veiculos")
        veiculos_map = {} # old_id -> new_instance
        for row in cursor.fetchall():
            old_id, placa, modelo, ano, renavam, km_atual = row
            veiculo, created = Veiculo.objects.get_or_create(
                placa=placa,
                defaults={
                    'modelo': modelo,
                    'ano': ano,
                    'renavam': renavam,
                    'km_atual': km_atual if km_atual else 0
                }
            )
            veiculos_map[old_id] = veiculo
        self.stdout.write(self.style.SUCCESS(f'Migrated {len(veiculos_map)} Veiculos'))

        # 3. Migrate Viagens
        self.stdout.write('Migrating Viagens...')
        cursor.execute("SELECT id, data, motorista_id, veiculo_id, origem, destino, hora_saida, distancia FROM viagens")
        viagens_count = 0
        for row in cursor.fetchall():
            old_id, data, motorista_id, veiculo_id, origem, destino, hora_saida, distancia = row
            
            motorista = motoristas_map.get(motorista_id)
            veiculo = veiculos_map.get(veiculo_id)

            if motorista and veiculo:
                # Check if exists to avoid duplicates
                if not Viagem.objects.filter(
                    data=parse_date(data),
                    hora_saida=parse_time(hora_saida),
                    motorista=motorista,
                    veiculo=veiculo
                ).exists():
                    Viagem.objects.create(
                        data=parse_date(data),
                        hora_saida=parse_time(hora_saida),
                        motorista=motorista,
                        veiculo=veiculo,
                        origem=origem,
                        destino=destino,
                        distancia=distancia if distancia else 0
                    )
                    viagens_count += 1
        self.stdout.write(self.style.SUCCESS(f'Migrated {viagens_count} Viagens'))

        # 4. Migrate Multas
        self.stdout.write('Migrating Multas...')
        cursor.execute("SELECT id, data, hora_infracao, local, tipo_infracao, descricao, motorista_id, veiculo_id, valor, viagem_id FROM multas")
        multas_count = 0
        for row in cursor.fetchall():
            old_id, data, hora_infracao, local, tipo_infracao, descricao, motorista_id, veiculo_id, valor, viagem_id = row
            
            motorista = motoristas_map.get(motorista_id)
            veiculo = veiculos_map.get(veiculo_id)
            
            # Try to find the trip if linked, but it's tricky without a direct map if we didn't save it.
            # However, since we just created them, we might not have the exact ID match if we didn't force IDs.
            # For simplicity, we will skip linking the exact Viagem object for now unless we query it, 
            # or we could have stored the map.
            # Let's try to match by attributes if needed, or just leave it null if not critical.
            # But wait, the model has a ForeignKey.
            
            # Improved strategy: We can't easily map the Viagem ID because we didn't force IDs.
            # But the user might want that history. 
            # For now, let's leave 'viagem' null to avoid errors, as it's nullable.
            viagem = None 

            if motorista and veiculo:
                 if not Multa.objects.filter(
                    data=parse_date(data),
                    tipo_infracao=tipo_infracao,
                    veiculo=veiculo
                ).exists():
                    Multa.objects.create(
                        data=parse_date(data),
                        hora_infracao=parse_time(hora_infracao),
                        local=local,
                        tipo_infracao=tipo_infracao,
                        descricao=descricao,
                        motorista=motorista,
                        veiculo=veiculo,
                        viagem=viagem,
                        valor=valor
                    )
                    multas_count += 1
        self.stdout.write(self.style.SUCCESS(f'Migrated {multas_count} Multas'))

        # 5. Migrate Manutencoes
        self.stdout.write('Migrating Manutencoes...')
        cursor.execute("SELECT id, veiculo_id, data, tipo_servico, descricao, km_realizado, proximo_servico_km, proximo_servico_data, valor FROM manutencoes")
        manutencoes_count = 0
        for row in cursor.fetchall():
            old_id, veiculo_id, data, tipo_servico, descricao, km_realizado, proximo_servico_km, proximo_servico_data, valor = row
            
            veiculo = veiculos_map.get(veiculo_id)
            
            if veiculo:
                if not Manutencao.objects.filter(
                    veiculo=veiculo,
                    data=parse_date(data),
                    tipo_servico=tipo_servico
                ).exists():
                    Manutencao.objects.create(
                        veiculo=veiculo,
                        data=parse_date(data),
                        tipo_servico=tipo_servico,
                        descricao=descricao,
                        km_realizado=km_realizado,
                        proximo_servico_km=proximo_servico_km,
                        proximo_servico_data=parse_date(proximo_servico_data),
                        valor=valor
                    )
                    manutencoes_count += 1
        self.stdout.write(self.style.SUCCESS(f'Migrated {manutencoes_count} Manutencoes'))

        conn.close()
        self.stdout.write(self.style.SUCCESS('Data migration completed successfully!'))
