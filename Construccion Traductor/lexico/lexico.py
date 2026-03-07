# ConstruccionTraductor/lexico/lexico.py

import re
from .tipos import *


class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __str__(self):
        nombre = NOMBRES_TOKENS.get(self.tipo, f"TIPO_{self.tipo}")
        return f"{nombre}('{self.valor}') [{self.linea}:{self.columna}]"


class Lexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.linea = 1
        self.columna = 1
        self.simbolo = ""
        self.tipo = None
        self.indice = 0

        self.patrones = [
            (REAL, r'\d+\.\d+'),
            (ENTERO, r'\d+'),
            (CADENA, r'"[^"]*"'),
            (TIPO, r'\b(int|float|char|void)\b'),
            (IF, r'\bif\b'),
            (WHILE, r'\bwhile\b'),
            (RETURN, r'\breturn\b'),
            (ELSE, r'\belse\b'),
            (IDENTIFICADOR, r'[a-zA-Z_][a-zA-Z0-9_]*'),
            (OP_IGUALDAD, r'==|!='),  # before opRelac
            (OP_RELAC, r'<=|>=|<|>'),
            (OP_OR, r'\|\|'),
            (OP_AND, r'&&'),
            (OP_NOT, r'!'),
            (OP_SUMA, r'\+|-'),
            (OP_MUL, r'\*|/'),
            (PUNTO_COMA, r';'),
            (COMA, r','),
            (PAREN_IZQ, r'\('),
            (PAREN_DER, r'\)'),
            (LLAVE_IZQ, r'\{'),
            (LLAVE_DER, r'\}'),
            (ASIGNACION, r'='),  # after == !=
        ]

    def sigSimbolo(self):
        if self.indice >= len(self.codigo):
            self.simbolo = "$"
            self.tipo = PESOS
            return

        # Skip whitespace
        while self.indice < len(self.codigo) and self.codigo[self.indice].isspace():
            if self.codigo[self.indice] == '\n':
                self.linea += 1
                self.columna = 1
            else:
                self.columna += 1
            self.indice += 1

        if self.indice >= len(self.codigo):
            self.simbolo = "$"
            self.tipo = PESOS
            return

        for tipo, patron in self.patrones:
            regex = re.compile(patron)
            match = regex.match(self.codigo[self.indice:])
            if match:
                self.simbolo = match.group(0)
                self.tipo = tipo
                self.indice += len(self.simbolo)
                self.columna += len(self.simbolo)
                return

        # If no match, lexical error
        raise Exception(f"Error léxico en línea {self.linea}, columna {self.columna}: caracter inválido '{self.codigo[self.indice]}'")

    def terminado(self):
        return self.tipo == PESOS

    def get_tokens(self):
        tokens = []
        while not self.terminado():
            tokens.append(Token(self.tipo, self.simbolo, self.linea, self.columna))
            self.sigSimbolo()
        return tokens


def tokenize(codigo):
    lexico = Lexico(codigo)
    lexico.sigSimbolo()
    return lexico.get_tokens()