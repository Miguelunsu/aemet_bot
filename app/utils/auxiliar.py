def string_a_float_con_decimal(s):
    # Convierte un 495 a 49.5
    try:
        s = str(s).strip()  # por si viene como número o con espacios
        if len(s) < 2:
            return float(s)  # ej: "5" → 5.0
        return float(s[:-1] + '.' + s[-1])
    except (ValueError, TypeError):
        return None  # o lanza una excepción