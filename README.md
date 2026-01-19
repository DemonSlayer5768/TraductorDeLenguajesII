# Analizador Léxico

## Descripción General

Este proyecto implementa un **analizador léxico** que identifica y clasifica tokens de diferentes tipos de datos. El analizador reconoce cadenas, booleanos, números enteros, números reales e identificadores.

## Archivos del Proyecto

### `functions.py`

Contiene las funciones principales del analizador léxico:

#### `identificar_tipo(cadena)`
Identifica el tipo de dato de una cadena individual utilizando expresiones regulares.

**Tipos reconocidos:**

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `STRING` | Cadenas entre comillas simples o dobles | `'hola'`, `"mundo"` |
| `BOOLEAN` | Valores booleanos | `true`, `false` |
| `INT` | Números enteros (con signo opcional) | `30`, `-42` |
| `REAL` | Números decimales (con signo opcional) | `29.9`, `-3.14` |
| `IDENTIFICADOR` | Nombres de variables o funciones | `variable`, `_private`, `var123` |
| `DESCONOCIDO` | Token no reconocido | Cualquier otra entrada |

#### `analizador_lexico(cadena)`
Procesa una cadena completa dividiéndola en tokens y clasificando cada uno.

**Entrada:** Una cadena de texto con tokens separados por espacios

**Salida:** Lista de tuplas `(token, tipo)`

### `analizadorLexico.py`

Script de prueba que demuestra el funcionamiento del analizador léxico con varios ejemplos:

```python
x  = "'hola'"        # STRING
x1 = "'hola29'"      # STRING
x2 = "'h_o_l_a'"     # STRING
x3 = '29.9'          # REAL
x4 = '30'            # INT
x5 = 'true'          # BOOLEAN
```

## Cómo Funciona

1. **División en tokens:** La cadena se divide por espacios en blanco
2. **Clasificación:** Cada token se evalúa contra patrones regex en orden
3. **Resultado:** Se retorna una lista con cada token y su tipo

## Ejemplo de Uso

```python
from functions import analizador_lexico

resultado = analizador_lexico("'hola' 30 3.14 true")
# Salida: [("'hola'", 'STRING'), ('30', 'INT'), ('3.14', 'REAL'), ('true', 'BOOLEAN')]
```

## Ejecución

Para ejecutar las pruebas:

```bash
python analizadorLexico.py
```