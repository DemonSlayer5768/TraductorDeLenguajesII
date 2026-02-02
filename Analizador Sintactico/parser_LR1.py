from pila import Pila
from llexico import Lexico, TipoSimbolo


# =======================
# TABLAS Y REGLAS
# =======================

tablaLR1 = [
    [2, 0, 0, 1],
    [0, 0, -1, 0],
    [0, 3, 0, 0],
    [4, 0, 0, 0],
    [0, 0, -2, 0]
]

idReglas1  = [3]
lonReglas1 = [3]


tablaLR2 = [
    [2, 0, 0, 1],
    [0, 0, -1, 0],
    [0, 3, -3, 0],
    [2, 0, 0, 4],
    [0, 0, -2, 0]
]

idReglas2  = [3, 3]
lonReglas2 = [3, 1]


# =======================
# EJERCICIO 1
# =======================

def ejercicio1():
    print("=== EJERCICIO 1 ===")
    pila = Pila()
    lexico = Lexico("a+b")

    pila.push(0)
    lexico.sigSimbolo()

    while True:
        fila = pila.top()
        columna = lexico.tipo
        accion = tablaLR1[fila][columna]

        pila.muestra()
        print("entrada:", lexico.simbolo)
        print("accion:", accion)

        if accion > 0:
            pila.push(columna)
            pila.push(accion)
            lexico.sigSimbolo()

        elif accion < 0:
            if accion == -1:
                print("ACEPTACIÓN\n")
                break

            numRegla = -accion - 2
            for _ in range(lonReglas1[numRegla] * 2):
                pila.pop()

            fila = pila.top()
            pila.push(idReglas1[numRegla])
            pila.push(tablaLR1[fila][idReglas1[numRegla]])

        else:
            print("ERROR SINTÁCTICO")
            break


# =======================
# EJERCICIO 2
# =======================

def ejercicio2():
    print("=== EJERCICIO 2 ===")
    pila = Pila()
    lexico = Lexico("a+b+c+d+e+f")

    pila.push(0)
    lexico.sigSimbolo()

    while True:
        fila = pila.top()
        columna = lexico.tipo
        accion = tablaLR2[fila][columna]

        pila.muestra()
        print("entrada:", lexico.simbolo)
        print("accion:", accion)

        if accion > 0:
            pila.push(columna)
            pila.push(accion)
            lexico.sigSimbolo()

        elif accion < 0:
            if accion == -1:
                print("ACEPTACIÓN\n")
                break

            numRegla = -accion - 2
            for _ in range(lonReglas2[numRegla] * 2):
                pila.pop()

            fila = pila.top()
            pila.push(idReglas2[numRegla])
            pila.push(tablaLR2[fila][idReglas2[numRegla]])

        else:
            print("ERROR SINTÁCTICO")
            break
