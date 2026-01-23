# Analizador Léxico

## Descripción General

Este proyecto implementa un **analizador léxico** completo para un lenguaje de programación simplificado. El analizador lee caracteres de una fuente y los clasifica en diversos tokens como identificadores, palabras clave reservadas, operadores, números y símbolos. Está diseñado para ser la primera fase de un compilador o intérprete.

## Archivos del Proyecto

### `functions.py`

Contiene la implementación del analizador léxico con dos clases principales:

#### Clase `TipoSimbolo`

Enumeración que define todos los tipos de tokens reconocidos por el analizador:

| Código | Tipo         | Descripción                                            |
| ------ | ------------ | ------------------------------------------------------ |
| 0      | `IDENT`      | Identificadores: nombres de variables y funciones      |
| 1      | `ENTERO`     | Números enteros: secuencias de dígitos                 |
| 2      | `REAL`       | Números decimales: enteros seguidos de punto y dígitos |
| 3      | `CADENA`     | Cadenas de caracteres (reservado para futuro uso)      |
| 4      | `TIPO`       | Palabras clave de tipo: `int`, `float`, `void`         |
| 5      | `OPSUMA`     | Operadores de suma/resta: `+`, `-`                     |
| 6      | `OPMUL`      | Operadores de multiplicación/división: `*`, `/`        |
| 7      | `OPRELAC`    | Operadores relacionales: `<`, `<=`, `>`, `>=`          |
| 8      | `OPOR`       | Operador OR lógico: `\|\|`                             |
| 9      | `OPAND`      | Operador AND lógico: `&&`                              |
| 10     | `OPNOT`      | Operador NOT lógico: `!`                               |
| 11     | `OPIGUALDAD` | Operadores de igualdad: `==`, `!=`                     |
| 12     | `PYC`        | Punto y coma: `;`                                      |
| 13     | `COMA`       | Coma: `,`                                              |
| 14     | `PARI`       | Paréntesis izquierdo: `(`                              |
| 15     | `PARD`       | Paréntesis derecho: `)`                                |
| 16     | `LLAVEI`     | Llave izquierda: `{`                                   |
| 17     | `LLAVED`     | Llave derecha: `}`                                     |
| 18     | `ASIG`       | Operador de asignación: `=`                            |
| 19     | `IF`         | Palabra clave: `if`                                    |
| 20     | `WHILE`      | Palabra clave: `while`                                 |
| 21     | `RETURN`     | Palabra clave: `return`                                |
| 22     | `ELSE`       | Palabra clave: `else`                                  |
| 23     | `PESOS`      | Símbolo especial: `$`                                  |
| 99     | `FIN`        | Fin de entrada (fin de la cadena)                      |
| -1     | `ERROR`      | Token no reconocido                                    |

**Palabras Clave Reservadas:**

El diccionario `RESERVADAS` asocia palabras clave con sus tipos:

```python
RESERVADAS = {
    "if": TipoSimbolo.IF,           # Control de flujo condicional
    "while": TipoSimbolo.WHILE,     # Bucle iterativo
    "return": TipoSimbolo.RETURN,   # Retorno de función
    "else": TipoSimbolo.ELSE,       # Rama alternativa
    "int": TipoSimbolo.TIPO,        # Tipo entero
    "float": TipoSimbolo.TIPO,      # Tipo decimal
    "void": TipoSimbolo.TIPO        # Tipo sin retorno
}
```

#### Clase `Lexico`

Implementa el analizador léxico que procesa la cadena fuente carácter por carácter:

**Atributos:**

- `fuente`: Cadena a analizar
- `ind`: Índice actual en la fuente
- `simbolo`: Token actual acumulado
- `estado`: Estado interno del procesamiento

**Métodos principales:**

- `sigCaracter()`: Obtiene el siguiente carácter de la fuente. Retorna `None` al final.
- `sigSimbolo()`: Procesa y retorna el siguiente token clasificado.
- `retroceso()`: Retrocede el índice un carácter cuando es necesario.

**Características principales:**

1. **Ignorar espacios en blanco:** El analizador automáticamente salta espacios, tabulaciones y saltos de línea.

2. **Identificadores y Palabras Clave:**
   - Comienzan con letra (a-z, A-Z) o guión bajo (\_)
   - Pueden contener letras, dígitos y guiones bajos
   - Se verifica si es palabra reservada antes de clasificar como `IDENT`

3. **Números:**
   - **Enteros:** Secuencias de dígitos (0-9)
   - **Reales:** Enteros seguidos de punto (.) y más dígitos
   - El análisis diferencia automáticamente entre ambos tipos

4. **Operadores complejos:**
   - Operadores de dos caracteres: `<=`, `>=`, `==`, `!=`, `&&`, `||`
   - Validación correcta: por ejemplo, `&` solo por sí es error, pero `&&` es válido

5. **Símbolos especiales:**
   - Paréntesis, llaves, punto y coma, coma
   - Símbolo especial `$` (final de entrada alternativo)

### `analizadorLexico.py`

Script de prueba del analizador léxico con un ejemplo real de código:

```python
codigo = "int x = 12; if (x >= 7) return x; $"
lex = Lexico(codigo)

while True:
    tipo = lex.sigSimbolo()
    if tipo == TipoSimbolo.FIN:
        break
    print(f"{lex.simbolo} -> {tipo}")
```

**Salida esperada:**

```
int -> 4           # TIPO
x -> 0             # IDENT
= -> 18            # ASIG
12 -> 1            # ENTERO
; -> 12            # PYC
if -> 19           # IF
( -> 14            # PARI
x -> 0             # IDENT
>= -> 7            # OPRELAC
7 -> 1             # ENTERO
) -> 15            # PARD
return -> 21       # RETURN
x -> 0             # IDENT
; -> 12            # PYC
$ -> 23            # PESOS
```

## Ejemplo de Uso

```python
from functions import Lexico, TipoSimbolo

# Analizar código fuente
codigo = "int x = 12;"
lex = Lexico(codigo)

while True:
    tipo = lex.sigSimbolo()
    if tipo == TipoSimbolo.FIN:
        break
    print(f"{lex.simbolo} -> {tipo}")
```

## Cómo Funciona

1. **Inicialización:** Se crea una instancia de `Lexico` con la cadena fuente a analizar.
2. **Lectura de caracteres:** `sigCaracter()` lee caracteres uno a uno de la fuente.
3. **Procesamiento de tokens:**
   - **Espacios:** Se ignoran automáticamente
   - **Identificadores/Palabras clave:** Se leen caracteres alfanuméricos, luego se consulta el diccionario `RESERVADAS`
   - **Números:** Se distingue entre enteros y reales según presencia de punto decimal
   - **Operadores:** Se procesan operadores simples y complejos (de uno o dos caracteres)
   - **Símbolos:** Se reconocen paréntesis, llaves, punto y coma, coma
4. **Retroceso:** Cuando es necesario, `retroceso()` devuelve el índice un paso atrás para que el siguiente token procese un carácter ya leído.
5. **Fin de entrada:** Retorna `TipoSimbolo.FIN` cuando `sigCaracter()` devuelve `None` o encuentra `$`.
6. **Errores:** Retorna `TipoSimbolo.ERROR` para caracteres o combinaciones no reconocidas.

## Ejecución

Para ejecutar las pruebas:

```bash
python analizadorLexico.py
```
