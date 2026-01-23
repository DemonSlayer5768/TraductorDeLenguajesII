
class TipoSimbolo:
    IDENT = 0
    ENTERO = 1
    REAL = 2
    CADENA = 3
    TIPO = 4          # int, float, void
    OPSUMA = 5        # + -
    OPMUL = 6         # * /
    OPRELAC = 7       # < <= > >=
    OPOR = 8          # ||
    OPAND = 9         # &&
    OPNOT = 10        # !
    OPIGUALDAD = 11   # == !=
    PYC = 12          # ;
    COMA = 13         # ,
    PARI = 14         # (
    PARD = 15         # )
    LLAVEI = 16       # {
    LLAVED = 17       # }
    ASIG = 18         # =
    IF = 19
    WHILE = 20
    RETURN = 21
    ELSE = 22
    PESOS = 23
    FIN = 99
    ERROR = -1


RESERVADAS = {
    "if": TipoSimbolo.IF,
    "while": TipoSimbolo.WHILE,
    "return": TipoSimbolo.RETURN,
    "else": TipoSimbolo.ELSE,
    "int": TipoSimbolo.TIPO,
    "float": TipoSimbolo.TIPO,
    "void": TipoSimbolo.TIPO
}

class Lexico:
    def __init__(self, fuente=""):
        self.fuente = fuente
        self.ind = 0
        self.simbolo = ""
        self.estado = 0

    def sigCaracter(self):
        if self.ind >= len(self.fuente):
            return None
        c = self.fuente[self.ind]
        self.ind += 1
        return c

    def retroceso(self):
        self.ind -= 1

    def sigSimbolo(self):
        self.simbolo = ""

        while True:
            c = self.sigCaracter()

            if c is None:
                return TipoSimbolo.FIN

            # Ignorar espacios
            if c.isspace():
                continue

            # IDENTIFICADORES / RESERVADAS
            if c.isalpha() or c == '_':
                self.simbolo += c
                while True:
                    c = self.sigCaracter()
                    if c is not None and (c.isalnum() or c == '_'):
                        self.simbolo += c
                    else:
                        if c is not None:
                            self.retroceso()
                        break

                return RESERVADAS.get(self.simbolo, TipoSimbolo.IDENT)

            # ENTERO / REAL
            if c.isdigit():
                self.simbolo += c
                es_real = False

                while True:
                    c = self.sigCaracter()
                    if c is not None and c.isdigit():
                        self.simbolo += c
                    elif c == '.' and not es_real:
                        es_real = True
                        self.simbolo += c
                    else:
                        if c is not None:
                            self.retroceso()
                        break

                return TipoSimbolo.REAL if es_real else TipoSimbolo.ENTERO

            # OPERADORES
            if c == '+':
                self.simbolo = c
                return TipoSimbolo.OPSUMA
            if c == '-':
                self.simbolo = c
                return TipoSimbolo.OPSUMA
            if c == '*':
                self.simbolo = c
                return TipoSimbolo.OPMUL
            if c == '/':
                self.simbolo = c
                return TipoSimbolo.OPMUL

            if c == '<':
                self.simbolo = c
                c2 = self.sigCaracter()
                if c2 == '=':
                    self.simbolo += c2
                else:
                    if c2 is not None:
                        self.retroceso()
                return TipoSimbolo.OPRELAC

            if c == '>':
                self.simbolo = c
                c2 = self.sigCaracter()
                if c2 == '=':
                    self.simbolo += c2
                else:
                    if c2 is not None:
                        self.retroceso()
                return TipoSimbolo.OPRELAC

            if c == '=':
                self.simbolo = c
                c2 = self.sigCaracter()
                if c2 == '=':
                    self.simbolo += c2
                    return TipoSimbolo.OPIGUALDAD
                else:
                    if c2 is not None:
                        self.retroceso()
                    return TipoSimbolo.ASIG

            if c == '!':
                self.simbolo = c
                c2 = self.sigCaracter()
                if c2 == '=':
                    self.simbolo += c2
                    return TipoSimbolo.OPIGUALDAD
                else:
                    if c2 is not None:
                        self.retroceso()
                    return TipoSimbolo.OPNOT

            if c == '&':
                c2 = self.sigCaracter()
                if c2 == '&':
                    self.simbolo = "&&"
                    return TipoSimbolo.OPAND
                return TipoSimbolo.ERROR

            if c == '|':
                c2 = self.sigCaracter()
                if c2 == '|':
                    self.simbolo = "||"
                    return TipoSimbolo.OPOR
                return TipoSimbolo.ERROR

            # SIMBOLOS
            simbolos = {
                ';': TipoSimbolo.PYC,
                ',': TipoSimbolo.COMA,
                '(': TipoSimbolo.PARI,
                ')': TipoSimbolo.PARD,
                '{': TipoSimbolo.LLAVEI,
                '}': TipoSimbolo.LLAVED,
                '$': TipoSimbolo.PESOS
            }

            if c in simbolos:
                self.simbolo = c
                return simbolos[c]

            return TipoSimbolo.ERROR

