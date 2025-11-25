import sqlite3
import pandas as pd
import os

DB_NAME = "traffic_app.db"

def get_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    """Initializes the database with the required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table: motoristas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS motoristas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            cnh TEXT NOT NULL UNIQUE,
            validade_cnh TEXT NOT NULL
        )
    ''')
    
    # Table: veiculos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL UNIQUE,
            modelo TEXT NOT NULL,
            ano INTEGER NOT NULL,
            renavam TEXT NOT NULL UNIQUE
        )
    ''')
    
    # Table: multas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS multas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            hora_infracao TEXT,
            local TEXT NOT NULL,
            tipo_infracao TEXT NOT NULL,
            descricao TEXT,
            motorista_id INTEGER NOT NULL,
            veiculo_id INTEGER NOT NULL,
            valor REAL NOT NULL,
            viagem_id INTEGER,
            FOREIGN KEY (motorista_id) REFERENCES motoristas (id),
            FOREIGN KEY (veiculo_id) REFERENCES veiculos (id),
            FOREIGN KEY (viagem_id) REFERENCES viagens (id)
        )
    ''')
    
    # Table: viagens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS viagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            motorista_id INTEGER NOT NULL,
            veiculo_id INTEGER NOT NULL,
            destino TEXT NOT NULL,
            hora_saida TEXT NOT NULL,
            FOREIGN KEY (motorista_id) REFERENCES motoristas (id),
            FOREIGN KEY (veiculo_id) REFERENCES veiculos (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_driver(nome, cpf, cnh, validade_cnh):
    """Adds a new driver to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO motoristas (nome, cpf, cnh, validade_cnh)
            VALUES (?, ?, ?, ?)
        ''', (nome, cpf, cnh, validade_cnh))
        conn.commit()
        return True, "Motorista cadastrado com sucesso!"
    except sqlite3.IntegrityError as e:
        return False, f"Erro ao cadastrar motorista: {e}"
    finally:
        conn.close()

def add_vehicle(placa, modelo, ano, renavam):
    """Adds a new vehicle to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO veiculos (placa, modelo, ano, renavam)
            VALUES (?, ?, ?, ?)
        ''', (placa, modelo, ano, renavam))
        conn.commit()
        return True, "Veículo cadastrado com sucesso!"
    except sqlite3.IntegrityError as e:
        return False, f"Erro ao cadastrar veículo: {e}"
    finally:
        conn.close()

def add_fine(data, local, tipo_infracao, descricao, motorista_id, veiculo_id, valor, hora_infracao=None, viagem_id=None):
    """Adds a new fine to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO multas (data, hora_infracao, local, tipo_infracao, descricao, motorista_id, veiculo_id, valor, viagem_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data, hora_infracao, local, tipo_infracao, descricao, motorista_id, veiculo_id, valor, viagem_id))
        conn.commit()
        return True, "Multa cadastrada com sucesso!"
    except Exception as e:
        return False, f"Erro ao cadastrar multa: {e}"
    finally:
        conn.close()

def get_drivers():
    """Returns a DataFrame with all drivers."""
    conn = get_connection()
    query = "SELECT * FROM motoristas"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_vehicles():
    """Returns a DataFrame with all vehicles."""
    conn = get_connection()
    query = "SELECT * FROM veiculos"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_fines_df():
    """Returns a DataFrame with details of all fines."""
    conn = get_connection()
    query = '''
        SELECT 
            m.id, 
            m.data, 
            m.local, 
            m.tipo_infracao, 
            m.descricao, 
            m.valor,
            mot.nome as motorista, 
            v.placa as veiculo_placa,
            v.modelo as veiculo_modelo
        FROM multas m
        JOIN motoristas mot ON m.motorista_id = mot.id
        JOIN veiculos v ON m.veiculo_id = v.id
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ============ UPDATE FUNCTIONS ============

def update_driver(driver_id, nome, cpf, cnh, validade_cnh):
    """Updates an existing driver's information."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE motoristas 
            SET nome = ?, cpf = ?, cnh = ?, validade_cnh = ?
            WHERE id = ?
        ''', (nome, cpf, cnh, validade_cnh, driver_id))
        conn.commit()
        return True, "Motorista atualizado com sucesso!"
    except sqlite3.IntegrityError as e:
        return False, f"Erro ao atualizar motorista: {e}"
    finally:
        conn.close()

def update_vehicle(vehicle_id, placa, modelo, ano, renavam):
    """Updates an existing vehicle's information."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE veiculos 
            SET placa = ?, modelo = ?, ano = ?, renavam = ?
            WHERE id = ?
        ''', (placa, modelo, ano, renavam, vehicle_id))
        conn.commit()
        return True, "Veículo atualizado com sucesso!"
    except sqlite3.IntegrityError as e:
        return False, f"Erro ao atualizar veículo: {e}"
    finally:
        conn.close()

def update_fine(fine_id, data, local, tipo_infracao, descricao, motorista_id, veiculo_id, valor):
    """Updates an existing fine's information."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE multas 
            SET data = ?, local = ?, tipo_infracao = ?, descricao = ?, 
                motorista_id = ?, veiculo_id = ?, valor = ?
            WHERE id = ?
        ''', (data, local, tipo_infracao, descricao, motorista_id, veiculo_id, valor, fine_id))
        conn.commit()
        return True, "Multa atualizada com sucesso!"
    except Exception as e:
        return False, f"Erro ao atualizar multa: {e}"
    finally:
        conn.close()

# ============ DELETE FUNCTIONS ============

def delete_driver(driver_id):
    """Deletes a driver from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if driver has associated fines
        cursor.execute("SELECT COUNT(*) FROM multas WHERE motorista_id = ?", (driver_id,))
        count = cursor.fetchone()[0]
        if count > 0:
            return False, f"Não é possível excluir. Este motorista possui {count} multa(s) associada(s)."
        
        cursor.execute("DELETE FROM motoristas WHERE id = ?", (driver_id,))
        conn.commit()
        return True, "Motorista excluído com sucesso!"
    except Exception as e:
        return False, f"Erro ao excluir motorista: {e}"
    finally:
        conn.close()

def delete_vehicle(vehicle_id):
    """Deletes a vehicle from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if vehicle has associated fines
        cursor.execute("SELECT COUNT(*) FROM multas WHERE veiculo_id = ?", (vehicle_id,))
        count = cursor.fetchone()[0]
        if count > 0:
            return False, f"Não é possível excluir. Este veículo possui {count} multa(s) associada(s)."
        
        cursor.execute("DELETE FROM veiculos WHERE id = ?", (vehicle_id,))
        conn.commit()
        return True, "Veículo excluído com sucesso!"
    except Exception as e:
        return False, f"Erro ao excluir veículo: {e}"
    finally:
        conn.close()

def delete_fine(fine_id):
    """Deletes a fine from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM multas WHERE id = ?", (fine_id,))
        conn.commit()
        return True, "Multa excluída com sucesso!"
    except Exception as e:
        return False, f"Erro ao excluir multa: {e}"
    finally:
        conn.close()

# ============ GETTER FUNCTIONS FOR SINGLE RECORDS ============

def get_driver_by_id(driver_id):
    """Returns a single driver by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM motoristas WHERE id = ?", (driver_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'id': result[0],
            'nome': result[1],
            'cpf': result[2],
            'cnh': result[3],
            'validade_cnh': result[4]
        }
    return None

def get_vehicle_by_id(vehicle_id):
    """Returns a single vehicle by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM veiculos WHERE id = ?", (vehicle_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'id': result[0],
            'placa': result[1],
            'modelo': result[2],
            'ano': result[3],
            'renavam': result[4]
        }
    return None

def get_fine_by_id(fine_id):
    """Returns a single fine by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM multas WHERE id = ?", (fine_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'id': result[0],
            'data': result[1],
            'local': result[2],
            'tipo_infracao': result[3],
            'descricao': result[4],
            'motorista_id': result[5],
            'veiculo_id': result[6],
            'valor': result[7]
        }
    return None

# ============ TRAVEL FUNCTIONS ============

def add_travel(data, motorista_id, veiculo_id, destino, hora_saida):
    """Adds a new travel to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO viagens (data, motorista_id, veiculo_id, destino, hora_saida)
            VALUES (?, ?, ?, ?, ?)
        ''', (data, motorista_id, veiculo_id, destino, hora_saida))
        conn.commit()
        return True, "Viagem cadastrada com sucesso!"
    except Exception as e:
        return False, f"Erro ao cadastrar viagem: {e}"
    finally:
        conn.close()

def get_travels():
    """Returns a DataFrame with all travels."""
    conn = get_connection()
    query = '''
        SELECT 
            v.id,
            v.data,
            v.hora_saida,
            v.destino,
            m.nome as motorista,
            ve.placa as veiculo_placa,
            ve.modelo as veiculo_modelo
        FROM viagens v
        JOIN motoristas m ON v.motorista_id = m.id
        JOIN veiculos ve ON v.veiculo_id = ve.id
        ORDER BY v.data DESC, v.hora_saida DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_travel_by_id(travel_id):
    """Returns a single travel by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM viagens WHERE id = ?", (travel_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'id': result[0],
            'data': result[1],
            'motorista_id': result[2],
            'veiculo_id': result[3],
            'destino': result[4],
            'hora_saida': result[5]
        }
    return None

def update_travel(travel_id, data, motorista_id, veiculo_id, destino, hora_saida):
    """Updates an existing travel's information."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE viagens 
            SET data = ?, motorista_id = ?, veiculo_id = ?, destino = ?, hora_saida = ?
            WHERE id = ?
        ''', (data, motorista_id, veiculo_id, destino, hora_saida, travel_id))
        conn.commit()
        return True, "Viagem atualizada com sucesso!"
    except Exception as e:
        return False, f"Erro ao atualizar viagem: {e}"
    finally:
        conn.close()

def delete_travel(travel_id):
    """Deletes a travel from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if travel has associated fines
        cursor.execute("SELECT COUNT(*) FROM multas WHERE viagem_id = ?", (travel_id,))
        count = cursor.fetchone()[0]
        if count > 0:
            return False, f"Não é possível excluir. Esta viagem possui {count} multa(s) associada(s)."
        
        cursor.execute("DELETE FROM viagens WHERE id = ?", (travel_id,))
        conn.commit()
        return True, "Viagem excluída com sucesso!"
    except Exception as e:
        return False, f"Erro ao excluir viagem: {e}"
    finally:
        conn.close()
