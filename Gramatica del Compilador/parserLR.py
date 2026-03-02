from pila import Pila
from cargar_lr import cargarLR
from llexico import Lexico

def parse(rutaLR, codigo):
    tablaLR, idReglas, lonReglas = cargarLR(rutaLR)

    pila = Pila()
    lexico = Lexico(codigo)

    pila.push(0)
    lexico.sigSimbolo()

    while True:
        estado = pila.top()
        columna = lexico.tipo   # IMPORTANTE: debe coincidir con .inf

        accion = tablaLR[estado][columna]

        if accion > 0:  # SHIFT
            pila.push(columna)
            pila.push(accion)
            lexico.sigSimbolo()

        elif accion < 0:

            if accion == -1:
                print("CADENA ACEPTADA")
                break

            numRegla = -accion - 2

            for _ in range(lonReglas[numRegla] * 2):
                pila.pop()

            estado = pila.top()
            pila.push(idReglas[numRegla])
            pila.push(tablaLR[estado][idReglas[numRegla]])

        else:
            print("ERROR SINTÁCTICO")
            break