import re
import datetime

def parse_message(text: str) -> dict | None:
    """
    Parses a WhatsApp message text to extract trip details.
    
    Expected format (approximate):
    📄 Registro de Viagem
    Nome: Reginaldo 
    Placa: txh2f74 
    Km Inicial: 1301
    Destino: araguari 
    Km final: 1563
    
    Returns:
        dict: Extracted data if pattern matches.
        None: If the message does not match the trip log pattern.
    """
    if not text:
        return None

    # Check for header (case insensitive)
    if "registro de viagem" not in text.lower():
        return None

    data = {
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'raw_text': text
    }

    # Regex patterns for fields
    # Format: FieldName: <value> (handles optional whitespace)
    patterns = {
        'nome': r'Nome\s*:\s*(.+)',
        'placa': r'Placa\s*:\s*(.+)',
        'km_inicial': r'Km\s*Inicial\s*:\s*(\d+)',
        'destino': r'Destino\s*:\s*(.+)',
        'km_final': r'Km\s*final\s*:\s*(\d+)'
    }

    match_count = 0
    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            data[field] = match.group(1).strip()
            match_count += 1
        else:
            data[field] = None

    # If we found at least a few fields, consider it a valid trip message
    # Sometimes fields might be missing, but 'Nome' and 'Placa' are critical usually.
    if match_count >= 3:
        return data
    
    return None

if __name__ == "__main__":
    # Test
    sample = """
    📄 Registro de Viagem

    Nome:Reginaldo 
    Placa:txh2f74 
    Km Inicial:1301
    Destino:araguari 
    Km final:1563
    """
    print(parse_message(sample))
