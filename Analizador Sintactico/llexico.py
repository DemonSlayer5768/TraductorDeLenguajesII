class TipoSimbolo:
    ID = 0
    MAS = 1
    PESOS = 2


class Lexico:
    def __init__(self, fuente):
        self.fuente = fuente
        self.indice = 0
        self.simbolo = ""
        self.tipo = None

    def sigSimbolo(self):
        if self.indice >= len(self.fuente):
            self.simbolo = "$"
            self.tipo = TipoSimbolo.PESOS
            return

        c = self.fuente[self.indice]
        self.indice += 1

        if c.isalpha():
            self.simbolo = "id"
            self.tipo = TipoSimbolo.ID
        elif c == "+":
            self.simbolo = "+"
            self.tipo = TipoSimbolo.MAS
        else:
            self.simbolo = "$"
            self.tipo = TipoSimbolo.PESOS

    def terminado(self):
        return self.tipo == TipoSimbolo.PESOS
