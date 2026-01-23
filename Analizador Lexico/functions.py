
class TipoSimbolo:
    CHAR = "CHAR"
    INT = "INT"
    FLOAT = "FLOAT"
    PESOS = "PESOS"
    FIN = "FIN"
    ERROR = "ERROR"


class Lexico:
    def __init__(self, fuente=""):
        self.fuente = fuente
        self.ind = 0
        self.estado = 0
        self.simbolo = ""
        self.c = ""
        self.continua = True

    def sigCaracter(self):
        if self.ind >= len(self.fuente):
            return None   # ← FIN DE ENTRADA REAL
        c = self.fuente[self.ind]
        self.ind += 1
        return c

    def retroceso(self):
        if self.c != None:
            self.ind -= 1
        self.continua = False

    def aceptar(self, estado):
        self.estado = estado
        self.continua = False

    def sigSimbolo(self):
        self.estado = 0
        self.simbolo = ""
        self.continua = True

        while self.continua:
            self.c = self.sigCaracter()

            # ESTADO 0 - inicio
            if self.estado == 0:
                if self.c is None:
                    self.aceptar(99)

                elif self.c == '$':
                    self.simbolo += self.c
                    self.aceptar(4)   # SIMBOLO PESOS

                elif self.c.isalpha() or self.c == '_':
                    self.simbolo += self.c
                    self.aceptar(1)

                elif self.c.isdigit():
                    self.simbolo += self.c
                    self.estado = 2


            # ESTADO 2 - INT
            elif self.estado == 2:
                if self.c is not None and self.c.isdigit():
                    self.simbolo += self.c

                elif self.c == '.':
                    self.simbolo += self.c
                    self.estado = 3  # FLOAT

                else:
                    self.retroceso()
                    self.aceptar(2)


            # ESTADO 3 - FLOAT
            elif self.estado == 3:
                if self.c is not None and self.c.isdigit():
                    self.simbolo += self.c
                else:
                    self.retroceso()
                    self.aceptar(3) 


        return self.clasificar()

    def clasificar(self):
        if self.estado == 1:
            return TipoSimbolo.CHAR
        if self.estado == 2:
            return TipoSimbolo.INT
        if self.estado == 3:
            return TipoSimbolo.FLOAT
        if self.estado == 4:
            return TipoSimbolo.PESOS
        if self.estado == 99:
            return TipoSimbolo.FIN
        return TipoSimbolo.ERROR

