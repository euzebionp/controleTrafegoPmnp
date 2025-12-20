import pandas as pd
import os

EXCEL_FILE = "dados_extraidos.xlsx"

def save_to_excel(data_list: list[dict], filename: str = EXCEL_FILE):
    """
    Saves a list of dictionaries to an Excel file.
    Appends to existing file if it exists.
    """
    if not data_list:
        return

    df_new = pd.DataFrame(data_list)
    
    if os.path.exists(filename):
        try:
            # Read existing
            df_existing = pd.read_excel(filename)
            # Concat
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            # Save
            df_combined.to_excel(filename, index=False)
            print(f"✅ {len(data_list)} novos registros salvos em {filename}")
        except Exception as e:
            print(f"❌ Erro ao salvar Excel: {e}")
    else:
        # Create new
        try:
            df_new.to_excel(filename, index=False)
            print(f"✅ Arquivo {filename} criado com {len(data_list)} registros")
        except Exception as e:
            print(f"❌ Erro ao criar Excel: {e}")

if __name__ == "__main__":
    # Test
    dummy = [{'timestamp': '2023-10-20', 'nome': 'Teste', 'placa': 'ABC', 'km_inicial': 100, 'km_final': 200}]
    save_to_excel(dummy)
