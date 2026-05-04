from .pila import Pila
from .cargarLR import cargarLR
from lexico.lexico import Lexico

def parse(rutaLR, codigo):
    """
    Realiza análisis sintáctico LR.
    
    Args:
        rutaLR: Ruta al archivo de tabla LR
        codigo: Código fuente a analizar
        
    Raises:
        Exception: Si hay un error sintáctico
    """
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
                return True  # Cadena aceptada

            numRegla = -accion - 2

            for _ in range(lonReglas[numRegla] * 2):
                pila.pop()

            estado = pila.top()
            pila.push(idReglas[numRegla])
            pila.push(tablaLR[estado][idReglas[numRegla]])

        else:
            # Error sintáctico
            raise Exception(f"Error sintáctico: token inesperado '{lexico.simbolo}' en línea {lexico.linea}, columna {lexico.columna}")

