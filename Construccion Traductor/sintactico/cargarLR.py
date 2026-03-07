def cargarLR(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = [line.strip() for line in f if line.strip()]

    index = 0

    numReglas = int(lineas[index])
    index += 1

    idReglas = []
    lonReglas = []

    for _ in range(numReglas):
        partes = lineas[index].split()
        idReglas.append(int(partes[0]))
        lonReglas.append(int(partes[1]))
        index += 1

    filas, columnas = map(int, lineas[index].split())
    index += 1

    tabla = []

    for _ in range(filas):
        fila = list(map(int, lineas[index].split()))
        tabla.append(fila)
        index += 1

    return tabla, idReglas, lonReglas
