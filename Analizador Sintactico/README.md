# Analizador Sintáctico LR1

## Descripción General

Este proyecto implementa un **analizador sintáctico LR(1)** que es un compilador que analiza secuencias de símbolos para validar que cumplan con una gramática específica. El analizador utiliza una técnica de análisis ascendente (bottom-up) con una pila para procesar tokens de entrada.

---

## Estructura de Archivos

### 📄 `llexico.py`
**Propósito:** Análisis léxico (tokenización)

Realiza el análisis léxico de la cadena de entrada, identificando y clasificando cada símbolo.

**Componentes principales:**
- **`TipoSimbolo`**: Enumeración que define los tipos de símbolos
  - `ID` (0): Identificadores (letras a-z, A-Z)
  - `MAS` (1): Operador suma (+)
  - `PESOS` (2): Símbolo de fin de entrada ($)

- **`Lexico`**: Clase que procesa la cadena de entrada
  - `__init__(fuente)`: Inicializa con la cadena a analizar
  - `sigSimbolo()`: Obtiene el siguiente símbolo de la entrada
  - `terminado()`: Verifica si se alcanzó el final

**Ejemplo de uso:**
```python
lexico = Lexico("a+b")
lexico.sigSimbolo()  # Primera llamada
print(lexico.simbolo)  # "id"
print(lexico.tipo)     # 0 (ID)
```

---

### 📄 `pila.py`
**Propósito:** Estructura de datos de pila

Implementa una pila simple necesaria para el analizador LR(1), que almacena estados y símbolos durante el análisis.

**Métodos:**
- `push(x)`: Inserta un elemento en la pila
- `pop()`: Extrae el elemento del tope
- `top()`: Retorna el elemento del tope sin extraerlo
- `muestra()`: Imprime el contenido actual de la pila

**Ejemplo de uso:**
```python
pila = Pila()
pila.push(0)
pila.push(1)
print(pila.top())  # 1
pila.pop()
```

---

### 📄 `parser_LR1.py`
**Propósito:** Analizador sintáctico LR(1)

Implementa el algoritmo de análisis sintáctico LR(1) que utiliza tablas de análisis predefinidas para validar si una cadena pertenece a la gramática.

**Componentes principales:**
- **Tablas LR1 y LR2**: Matrices de transición que definen las acciones del analizador
  - Valores positivos: desplazamiento (shift) + nuevo estado
  - Valores negativos: reducción (reduce) usando una regla
  - -1: Aceptación (cadena válida)
  - 0: Error sintáctico

- **Funciones:**
  - `ejercicio1()`: Analiza la cadena "a+b"
  - `ejercicio2()`: Analiza la cadena "a+b+c+d+e+f"

**Funcionamiento:**
1. Inicializa la pila con estado 0
2. Lee el primer símbolo
3. Busca la acción en la tabla LR usando: fila = estado actual, columna = tipo de símbolo
4. Ejecuta la acción (desplazamiento o reducción)
5. Continúa hasta aceptación o error

---

### 📄 `main.py`
**Propósito:** Punto de entrada del programa

Ejecuta los dos ejercicios de prueba del analizador sintáctico.

---

## Cómo Funciona el Analizador LR(1)

### Algoritmo:
```
1. Push(0) en la pila
2. Leer primer símbolo de entrada
3. MIENTRAS entrada no sea procesada:
   a. fila ← tope de la pila
   b. columna ← tipo de símbolo actual
   c. acción ← tabla[fila][columna]
   
   d. Si acción > 0:
      - Push(columna) y Push(acción) en la pila
      - Leer siguiente símbolo
   
   e. Si acción < 0:
      - Si acción == -1: ACEPTAR
      - Si no: aplicar regla de reducción
   
   f. Si acción == 0: ERROR SINTÁCTICO
```

---

## Ejemplo de Salida en Terminal

### Ejecutar el programa:
```bash
python main.py
```

### Salida esperada:

```
=== EJERCICIO 1 ===
Pila: [0]
entrada: id
accion: 2
Pila: [0, 0, 2]
entrada: +
accion: 0
Pila: [0, 0, 2, 0]
entrada: id
accion: 3
Pila: [0, 0, 2, 0, 1, 3]
entrada: $
accion: -2
Pila: [0, 1]
entrada: $
accion: -1
ACEPTACIÓN

=== EJERCICIO 2 ===
Pila: [0]
entrada: id
accion: 2
Pila: [0, 0, 2]
entrada: +
accion: 0
Pila: [0, 0, 2, 0]
entrada: id
accion: 3
Pila: [0, 0, 2, 0, 1, 3]
entrada: +
accion: -3
Pila: [0, 1]
entrada: +
accion: 0
Pila: [0, 1, 1, 0]
entrada: id
accion: 3
Pila: [0, 1, 1, 0, 1, 3]
entrada: +
accion: -3
Pila: [0, 1]
entrada: +
accion: 0
Pila: [0, 1, 1, 0]
entrada: id
accion: 3
Pila: [0, 1, 1, 0, 1, 3]
entrada: +
accion: -3
Pila: [0, 1]
entrada: +
accion: 0
Pila: [0, 1, 1, 0]
entrada: id
accion: 3
Pila: [0, 1, 1, 0, 1, 3]
entrada: +
accion: -3
Pila: [0, 1]
entrada: +
accion: 0
Pila: [0, 1, 1, 0]
entrada: id
accion: 3
Pila: [0, 1, 1, 0, 1, 3]
entrada: +
accion: -3
Pila: [0, 1]
entrada: +
accion: 0
Pila: [0, 1, 1, 0]
entrada: id
accion: 3
Pila: [0, 1, 1, 0, 1, 3]
entrada: $
accion: -2
Pila: [0, 1]
entrada: $
accion: -1
ACEPTACIÓN

```

---

## Teoría de Gramáticas

Este analizador implementa la siguiente gramática simple:

```
E → E + T | T
T → id
```

Donde:
- **E**: Expresión (símbolo inicial)
- **T**: Término
- **id**: Identificador (una letra)
- **+**: Operador de suma

Esta gramática reconoce expresiones aritméticas con suma asociativa a izquierda, como:
- `a+b`
- `a+b+c+d+e+f`

---

## Requisitos

- Python 3.6+
- No requiere dependencias externas

---

## Ejecución

```bash
# Ejecutar todos los ejercicios
python main.py

# O ejecutar directamente ejercicios específicos
python parser_LR1.py
```

---

## Notas

- Las tablas LR1 y LR2 están predefinidas en `parser_LR1.py`
- El analizador espera cadenas sin espacios en blanco
- Los identificadores se limitan a caracteres alfabéticos simples
- Se muestra el contenido de la pila en cada paso para fines educativos

