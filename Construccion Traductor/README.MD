# Traductor de Lenguajes II - Construcción del Traductor

## Objetivo

Desarrollar un componente específico de un traductor (puede ser un compilador o un intérprete) para un lenguaje de programación simplificado. Este proyecto se realiza en varias fases, cada una centrada en una parte diferente del proceso de traducción.

**Fase Actual:** Análisis Léxico y Sintáctico

## Descripción

En esta fase, se implementa el analizador léxico y sintáctico para el lenguaje de programación asignado. El lenguaje tiene una sintaxis y un conjunto de tokens definidos. El analizador léxico lee el código fuente y lo convierte en una secuencia de tokens que serán utilizados en fases posteriores.

## Lenguaje Soportado

El lenguaje es un subconjunto simplificado de C, con las siguientes características:

- Tipos de datos: `int`, `float`, `char`, `void`
- Estructuras de control: `if`, `while`, `else`
- Funciones con parámetros y retorno
- Variables locales y globales
- Expresiones aritméticas y lógicas
- Asignaciones

### Tokens Definidos

- **Palabras reservadas:** `int`, `float`, `char`, `void`, `if`, `while`, `return`, `else`
- **Identificadores:** Secuencias de letras, dígitos y guiones bajos, empezando por letra o guion bajo
- **Literales:**
  - Enteros: `123`
  - Reales: `123.45`
  - Cadenas: `"texto"`
- **Operadores:**
  - Aritméticos: `+`, `-`, `*`, `/`
  - Relacionales: `<`, `>`, `<=`, `>=`, `==`, `!=`
  - Lógicos: `&&`, `||`, `!`
  - Asignación: `=`
- **Símbolos:** `(`, `)`, `{`, `}`, `;`, `,`

## Implementación

### Analizador Léxico (`lexico/lexico.py`)

- Utiliza expresiones regulares para reconocer patrones de tokens
- Maneja errores léxicos reportando línea y columna
- Produce una lista de tokens con tipo, valor, línea y columna

### Analizador Sintáctico (`sintactico/parserLR.py`)

- Implementa un parser LR(1) basado en tabla precomputada
- Carga la tabla desde `gramatica/compilador.lr`
- Reporta errores sintácticos cuando no puede reducir o desplazar

### Estructuras de Datos

- `Token`: Clase para representar tokens con tipo, valor, posición
- `Pila`: Implementación de pila para el parser
- Tabla LR: Matriz de acciones y transiciones

## Manejo de Errores

- **Errores Léxicos:** Caracteres inválidos, reportados con línea y columna
- **Errores Sintácticos:** Inconsistencias gramaticales, reportados como "ERROR SINTÁCTICO"

## Archivos de Ejemplo

- `ejemplos/correcto.txt`: Código válido
- `ejemplos/error_lexico.txt`: Contiene error léxico (@ inválido)
- `ejemplos/error_sintactico.txt`: Falta punto y coma

## Uso

Ejecutar `python main.py` para probar con el archivo `correcto.txt`.

Para cambiar el archivo de entrada, modificar `main.py`.

## Evaluación

El proyecto cumple con:

- Identificación correcta de todos los tokens
- Mensajes de error útiles para entradas inválidas
- Código bien organizado y comentado
- Documentación clara de la implementación

## Decisiones de Diseño

- **Léxico:** Uso de regex para simplicidad y eficiencia
- **Sintáctico:** Parser LR(1) precomputado para robustez
- **Errores:** Excepciones para léxico, mensajes simples para sintáctico
- **Estructura:** Módulos separados para léxico y sintáctico
