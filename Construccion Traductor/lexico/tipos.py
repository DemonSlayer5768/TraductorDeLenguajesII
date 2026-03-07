# Token type constants for LR parser
IDENTIFICADOR = 0
ENTERO = 1
REAL = 2
CADENA = 3
TIPO = 4
OP_SUMA = 5  # + -
OP_MUL = 6  # * /
OP_RELAC = 7  # <= >= < >
OP_OR = 8  # ||
OP_AND = 9  # &&
OP_NOT = 10  # !
OP_IGUALDAD = 11  # == !=
PUNTO_COMA = 12  # ;
COMA = 13  # ,
PAREN_IZQ = 14  # (
PAREN_DER = 15  # )
LLAVE_IZQ = 16  # {
LLAVE_DER = 17  # }
ASIGNACION = 18  # =
IF = 19
WHILE = 20
RETURN = 21
ELSE = 22
PESOS = 23  # $

# Mapping for display
NOMBRES_TOKENS = {
    0: "IDENTIFICADOR",
    1: "ENTERO",
    2: "REAL",
    3: "CADENA",
    4: "TIPO",
    5: "OP_SUMA",
    6: "OP_MUL",
    7: "OP_RELAC",
    8: "OP_OR",
    9: "OP_AND",
    10: "OP_NOT",
    11: "OP_IGUALDAD",
    12: "PUNTO_COMA",
    13: "COMA",
    14: "PAREN_IZQ",
    15: "PAREN_DER",
    16: "LLAVE_IZQ",
    17: "LLAVE_DER",
    18: "ASIGNACION",
    19: "IF",
    20: "WHILE",
    21: "RETURN",
    22: "ELSE",
    23: "PESOS"
}
