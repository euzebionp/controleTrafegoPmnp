from datetime import datetime, date


def format_date_br(date_str):
    """
    Converts date from YYYY-MM-DD format to DD/MM/YYYY (Brazilian format).

    Args:
        date_str: Date string in YYYY-MM-DD format

    Returns:
        Date string in DD/MM/YYYY format
    """
    try:
        if isinstance(date_str, str):
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        elif isinstance(date_str, date):
            date_obj = date_str
        else:
            return str(date_str)

        return date_obj.strftime("%d/%m/%Y")
    except:
        return str(date_str)


def is_cnh_expired(validade_cnh):
    """
    Checks if a CNH (driver's license) is expired.

    Args:
        validade_cnh: CNH validity date (string YYYY-MM-DD or date object)

    Returns:
        Boolean indicating if CNH is expired
    """
    try:
        if isinstance(validade_cnh, str):
            date_obj = datetime.strptime(validade_cnh, "%Y-%m-%d").date()
        elif isinstance(validade_cnh, date):
            date_obj = validade_cnh
        else:
            return False

        return date_obj < date.today()
    except:
        return False


def days_until_expiration(validade_cnh):
    """
    Calculates days until CNH expiration.

    Args:
        validade_cnh: CNH validity date (string YYYY-MM-DD or date object)

    Returns:
        Number of days until expiration (negative if expired)
    """
    try:
        if isinstance(validade_cnh, str):
            date_obj = datetime.strptime(validade_cnh, "%Y-%m-%d").date()
        elif isinstance(validade_cnh, date):
            date_obj = validade_cnh
        else:
            return 0

        delta = date_obj - date.today()
        return delta.days
    except:
        return 0


def get_cnh_status(validade_cnh):
    """
    Gets the status of a CNH (expired, expiring soon, or valid).

    Args:
        validade_cnh: CNH validity date

    Returns:
        Tuple of (status_text, status_color, icon)
    """
    days = days_until_expiration(validade_cnh)

    if days < 0:
        return ("VENCIDA", "red", "🔴")
    elif days <= 30:
        return (f"Vence em {days} dias", "orange", "⚠️")
    elif days <= 90:
        return (f"Vence em {days} dias", "yellow", "⚡")
    else:
        return ("Válida", "green", "✅")
