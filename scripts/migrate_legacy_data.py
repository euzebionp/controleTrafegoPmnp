import sqlite3
from logistics.models import Motorista, Veiculo, Viagem, Manutencao, Multa
from datetime import datetime

def run():
    conn = sqlite3.connect('traffic_app.db')
    cursor = conn.cursor()

    # 1. Migrate Motoristas
    print("Migrating Motoristas...")
    cursor.execute("SELECT id, nome, cpf, cnh, validade_cnh FROM motoristas")
    motoristas_map = {} # Old ID -> New ID
    for row in cursor.fetchall():
        old_id, nome, cpf, cnh, validade_cnh = row
        # Check if exists to avoid duplicates
        if not Motorista.objects.filter(cpf=cpf).exists():
            obj = Motorista.objects.create(
                nome=nome,
                cpf=cpf,
                cnh=cnh,
                validade_cnh=validade_cnh
            )
            motoristas_map[old_id] = obj.id
            print(f"Created Motorista: {nome}")
        else:
            obj = Motorista.objects.get(cpf=cpf)
            motoristas_map[old_id] = obj.id
            print(f"Skipped existing Motorista: {nome}")

    # 2. Migrate Veiculos
    print("\nMigrating Veiculos...")
    cursor.execute("SELECT id, placa, modelo, ano, renavam, km_atual FROM veiculos")
    veiculos_map = {} # Old ID -> New ID
    for row in cursor.fetchall():
        old_id, placa, modelo, ano, renavam, km_atual = row
        if not Veiculo.objects.filter(placa=placa).exists():
            obj = Veiculo.objects.create(
                placa=placa,
                modelo=modelo,
                ano=ano,
                renavam=renavam,
                km_atual=km_atual
            )
            veiculos_map[old_id] = obj.id
            print(f"Created Veiculo: {placa}")
        else:
            obj = Veiculo.objects.get(placa=placa)
            veiculos_map[old_id] = obj.id
            print(f"Skipped existing Veiculo: {placa}")

    # 3. Migrate Viagens
    print("\nMigrating Viagens...")
    cursor.execute("SELECT id, data, motorista_id, veiculo_id, origem, destino, hora_saida, distancia, km_atual FROM viagens")
    viagens_map = {}
    for row in cursor.fetchall():
        old_id, data, motorista_id, veiculo_id, origem, destino, hora_saida, distancia, km_atual = row
        
        new_motorista_id = motoristas_map.get(motorista_id)
        new_veiculo_id = veiculos_map.get(veiculo_id)

        if new_motorista_id and new_veiculo_id:
             # Check for duplicates (simple check based on data/time/driver)
            if not Viagem.objects.filter(data=data, hora_saida=hora_saida, motorista_id=new_motorista_id).exists():
                obj = Viagem.objects.create(
                    data=data,
                    motorista_id=new_motorista_id,
                    veiculo_id=new_veiculo_id,
                    origem=origem,
                    destino=destino,
                    hora_saida=hora_saida,
                    distancia=distancia,
                    km_atual=km_atual
                )
                viagens_map[old_id] = obj.id
                print(f"Created Viagem: {data} - {destino}")
            else:
                 # Need to get the object to map the ID for fines
                obj = Viagem.objects.get(data=data, hora_saida=hora_saida, motorista_id=new_motorista_id)
                viagens_map[old_id] = obj.id
                print(f"Skipped existing Viagem: {data} - {destino}")
        else:
            print(f"Skipped Viagem (ID {old_id}) due to missing dependencies.")

    # 4. Migrate Manutencoes
    print("\nMigrating Manutencoes...")
    cursor.execute("SELECT id, veiculo_id, data, tipo_servico, descricao, km_realizado, proximo_servico_km, proximo_servico_data, valor FROM manutencoes")
    for row in cursor.fetchall():
        old_id, veiculo_id, data, tipo_servico, descricao, km_realizado, proximo_servico_km, proximo_servico_data, valor = row
        
        new_veiculo_id = veiculos_map.get(veiculo_id)
        
        if new_veiculo_id:
            if not Manutencao.objects.filter(data=data, veiculo_id=new_veiculo_id, tipo_servico=tipo_servico).exists():
                Manutencao.objects.create(
                    veiculo_id=new_veiculo_id,
                    data=data,
                    tipo_servico=tipo_servico,
                    descricao=descricao,
                    km_realizado=km_realizado,
                    proximo_servico_km=proximo_servico_km,
                    proximo_servico_data=proximo_servico_data,
                    valor=valor
                )
                print(f"Created Manutencao: {tipo_servico}")
            else:
                print(f"Skipped existing Manutencao: {tipo_servico}")
        else:
             print(f"Skipped Manutencao (ID {old_id}) due to missing vehicle.")

    # 5. Migrate Multas
    print("\nMigrating Multas...")
    cursor.execute("SELECT id, data, hora_infracao, local, tipo_infracao, descricao, motorista_id, veiculo_id, valor, viagem_id FROM multas")
    for row in cursor.fetchall():
        old_id, data, hora_infracao, local, tipo_infracao, descricao, motorista_id, veiculo_id, valor, viagem_id = row
        
        new_motorista_id = motoristas_map.get(motorista_id)
        new_veiculo_id = veiculos_map.get(veiculo_id)
        new_viagem_id = viagens_map.get(viagem_id) if viagem_id else None

        if new_motorista_id and new_veiculo_id:
            if not Multa.objects.filter(data=data, motorista_id=new_motorista_id, tipo_infracao=tipo_infracao).exists():
                Multa.objects.create(
                    data=data,
                    hora_infracao=hora_infracao,
                    local=local,
                    tipo_infracao=tipo_infracao,
                    descricao=descricao,
                    motorista_id=new_motorista_id,
                    veiculo_id=new_veiculo_id,
                    valor=valor,
                    viagem_id=new_viagem_id
                )
                print(f"Created Multa: {tipo_infracao}")
            else:
                print(f"Skipped existing Multa: {tipo_infracao}")
        else:
            print(f"Skipped Multa (ID {old_id}) due to missing dependencies.")

    conn.close()
    print("\nMigration completed.")
