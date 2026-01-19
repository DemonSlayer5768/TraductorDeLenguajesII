import re


def identificar_tipo(cadena):
    cadena = cadena.strip()

    # String debe de tener comillas
    if re.fullmatch(r"'[^']*'|\"[^\"]*\"", cadena):
        return "STRING"

    # Booleano
    if cadena.lower() in ("true", "false"):
        return "BOOLEAN"

    # Entero
    if re.fullmatch(r'-?\d+', cadena):
        return "INT"

    # Real
    if re.fullmatch(r'-?\d+\.\d+', cadena):
        return "REAL"

    # Identificador
    if re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', cadena):
        return "IDENTIFICADOR"

    return "DESCONOCIDO"




def analizador_lexico(cadena):
    tokens = cadena.split()
    resultado = []

    for token in tokens:
        tipo = identificar_tipo(token)
        resultado.append((token, tipo))

    return resultado
