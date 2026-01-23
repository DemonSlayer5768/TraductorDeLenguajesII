# Analizador Léxico

## Descripción General

Este proyecto implementa un **analizador léxico** basado en un **autómata finito determinista (AFD)** que lee caracteres de una fuente y los clasifica en tokens. El analizador utiliza una máquina de estados para reconocer identificadores (CHAR), números enteros (INT), números decimales (FLOAT), símbolos especiales (PESOS) y detectar el fin de entrada.

## Archivos del Proyecto

### `functions.py`

Contiene la implementación del analizador léxico con dos clases principales:

#### Clase `TipoSimbolo`

Enumeración que define los tipos de tokens reconocidos:

| Tipo    | Descripción                                                                      |
| ------- | -------------------------------------------------------------------------------- |
| `CHAR`  | Identificadores: comienzan con letra o guión bajo, pueden contener alfanuméricos |
| `INT`   | Números enteros: secuencias de dígitos                                           |
| `FLOAT` | Números decimales: enteros seguidos de punto y dígitos fraccionarios             |
| `PESOS` | Símbolo especial `$`                                                             |
| `FIN`   | Fin de entrada (fin de la cadena)                                                |
| `ERROR` | Token no reconocido                                                              |

#### Clase `Lexico`

Implementa el autómata finito mediante máquina de estados:

**Atributos principales:**

- `fuente`: Cadena a analizar
- `ind`: Índice actual en la fuente
- `estado`: Estado actual del autómata (0=inicio, 1=CHAR, 2=INT, 3=FLOAT, 4=PESOS, 99=FIN)
- `simbolo`: Token actual acumulado
- `c`: Carácter actual
- `continua`: Bandera para continuar o terminar análisis

**Métodos principales:**

- `sigCaracter()`: Obtiene el siguiente carácter de la fuente. Retorna `None` al final.
- `sigSimbolo()`: Procesa y retorna el siguiente símbolo/token clasificado.
- `clasificar()`: Convierte el estado actual en un tipo de símbolo.
- `aceptar(estado)`: Marca un estado como final y detiene el procesamiento.
- `retroceso()`: Retrocede un carácter cuando es necesario.

**Diagrama de Estados:**

```
          [letra/_]  →  ESTADO 1 (CHAR)
         ↙
ESTADO 0 → [dígito] → ESTADO 2 (INT) → [.] → ESTADO 3 (FLOAT)
         ↘
          [$]        →  ESTADO 4 (PESOS)
         ↓
         [None]      →  ESTADO 99 (FIN)
```

### `analizadorLexico.py`

Script de demostración que prueba el analizador con diversos casos:

```python
x  = "'hola'"        # Identificador (CHAR)
x1 = "'hola29'"      # Identificador (CHAR)
x2 = "'h_o_l_a'"     # Identificador (CHAR)
x3 = '29.9'          # Número decimal (FLOAT)
x4 = '30'            # Número entero (INT)
x5 = 'true'          # Identificador (CHAR)
x6 = '$29.90'        # Símbolo PESOS + FLOAT
```

## Ejemplo de Uso

```python
from functions import Lexico, TipoSimbolo

lex = Lexico("hola 29.9 $")

while True:
    tipo = lex.sigSimbolo()
    if tipo == TipoSimbolo.FIN:
        break
    print(f"{lex.simbolo} -> {tipo}")

# Salida esperada:
# hola -> CHAR
# 29.9 -> FLOAT
# $ -> PESOS
```

## Cómo Funciona

1. **Inicialización:** Se crea una instancia de `Lexico` con la cadena fuente.
2. **Lectura caracteres:** `sigCaracter()` lee caracteres uno a uno.
3. **Transiciones de estado:** El autómata transita entre estados según los caracteres leídos.
4. **Aceptación:** Cuando se alcanza un estado final, se clasifica el token.
5. **Retroceso:** Si es necesario, se retrocede un carácter para procesar el siguiente token.
6. **Fin:** Se retorna `TipoSimbolo.FIN` cuando se agota la entrada.

## Ejecución

Para ejecutar las pruebas:

```bash
python analizadorLexico.py
```
