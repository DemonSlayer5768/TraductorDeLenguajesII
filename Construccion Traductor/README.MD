# Traductor Léxico y Sintáctico

## Objetivo

Implementar un analizador léxico y sintáctico para un lenguaje de programación simplificado que identifique tokens correctamente, detecte errores léxicos y sintácticos, y acepte códigos válidos.

## Descripción del Proyecto

Este proyecto implementa dos componentes principales de un compilador/intérprete:

1. **Analizador Léxico**: Convierte el código fuente en una secuencia de tokens
2. **Analizador Sintáctico (LR)**: Verifica que la secuencia de tokens cumpla con la gramática del lenguaje

## Arquitectura y Diseño

### Estructura de Directorios

```
.
├── main.py                      # Programa principal con menú interactivo
├── test_traductor.py            # Script de pruebas automatizadas
├── lexico/
│   ├── __init__.py
│   ├── lexico.py               # Analizador léxico
│   └── tipos.py                # Definiciones de tokens
├── sintactico/
│   ├── __init__.py
│   ├── parserLR.py             # Analizador sintáctico LR
│   ├── cargarLR.py             # Cargador de tabla LR
│   └── pila.py                 # Estructura de pila para el parser LR
├── gramatica/
│   ├── compilador.lr           # Tabla del analizador LR
│   ├── compilador.csv          # Definición de la gramática
│   └── compilador.inf          # Información de la gramática
└── ejemplos/
    ├── correcto.txt            # Código correctamente formado
    ├── error_lexico.txt        # Código con error léxico
    ├── error_sintactico.txt    # Código con error sintáctico
    └── complejo.txt            # Código más complejo correcto
```

### Componentes

#### 1. Analizador Léxico (`lexico/lexico.py`)

**Responsabilidad**: Convertir caracteres en tokens

**Características**:

- Recognoce todos los tokens del lenguaje mediante expresiones regulares
- Mantiene información de línea y columna para reportar errores precisos
- Salta espacios en blanco automáticamente
- Genera excepciones para caracteres inválidos

**Tokens Soportados**:

- **Palabras clave**: `int`, `float`, `char`, `void`, `if`, `while`, `return`, `else`
- **Identificadores**: Nombres de variables y funciones
- **Literales**: Números enteros, números flotantes, cadenas
- **Operadores**:
  - Aritméticos: `+`, `-`, `*`, `/`
  - Relacionales: `<`, `>`, `<=`, `>=`
  - Igualdad: `==`, `!=`
  - Lógicos: `&&`, `||`, `!`
- **Símbolos**: `(`, `)`, `{`, `}`, `;`, `,`, `=`

#### 2. Analizador Sintáctico (`sintactico/parserLR.py`)

**Responsabilidad**: Verificar que los tokens cumplan la gramática

**Características**:

- Utiliza el método LR (Left-to-Right, Rightmost derivation) con tabla de análisis precalculada
- Mantiene una pila de estados para el análisis
- Genera excepciones descriptivas cuando hay errores sintácticos

**Algoritmo LR**:

1. Carga la tabla LR de estados y acciones
2. Procesa tokens uno a uno
3. Realiza acciones SHIFT (apilar) o REDUCE (reducir por regla)
4. Acepta la cadena cuando alcanza el estado de aceptación

#### 3. Estructura de Datos

**Clase Token**: Almacena tipo, valor, línea y columna del token

**Clase Pila**: Implementación simple de pila para el parser LR

## Decisiones de Implementación

### 1. Uso de Expresiones Regulares

Se utilizaron expresiones regulares para reconocer tokens por su mayor simplicidad y facilidad de mantenimiento en comparación con máquinas de estados.

**Orden de las reglas**: Es crítico que las reglas se verifiquen en el orden correcto:

- Operadores de múltiples caracteres antes de sus prefijos (`==` antes de `=`)
- Palabras clave antes de identificadores (`if` antes de identificadores generales)

### 2. Parser LR

Se eligió un parser LR porque:

- Es más potente que parsers descendentes para gramáticas más complejas
- Permite detectar errores lo antes posible (al procesar cada token)
- Es determinista y eficiente

### 3. Manejo de Errores

#### Errores Léxicos

Se reportan cuando se encuentra un carácter no reconocido por ningún patrón. Se proporciona:

- Número de línea y columna exacta
- El carácter problemático
- Un mensaje descriptivo

Ejemplo:

```
Error léxico en línea 3, columna 23: caracter inválido '@'
```

#### Errores Sintácticos

Se reportan cuando el parser LR no encuentra una acción válida. Se proporciona:

- Token inesperado encontrado
- Línea y columna donde ocurrió el error

Ejemplo:

```
Error sintáctico: token inesperado 'resultado' en línea 3, columna 14
```

### 4. Seguimiento de Posición

Se mantiene contadores de línea y columna para proporcionar ubicaciones precisas de errores, lo que facilita que el usuario corrija el código.

## Gramática del Lenguaje

El lenguaje soporta:

```
programa → definiciones
definiciones → ε | definiciones definicion
definicion → defVar | defFunc
defVar → tipo listaVar ;
tipo → int | float | char | void
listaVar → ID | listaVar , ID
defFunc → tipo ID ( parametros ) bloquFunc
parametros → ε | listaParam
listaParam → tipo ID | listaParam , tipo ID
bloquFunc → { defLocales sentencias }
defLocales → ε | defLocales defLocal
defLocal → tipo ID ;
sentencias → ε | sentencias sentencia
sentencia → asignacion ; | bloque | if ( expresion ) sentencia | if ( expresion ) sentencia else sentencia | while ( expresion ) sentencia | return valRegresa ;
asignacion → ID = expresion | ID = llamadaFunc
bloque → { sentencias }
valRegresa → ε | expresion
llamadaFunc → ID ( argumentos )
argumentos → ε | listaArgumentos
listaArgumentos → termino | listaArgumentos , termino
expresion → termino | expresion + termino | expresion - termino | expresion * termino | expresion / termino | expresion == termino | expresion != termino | expresion < termino | expresion > termino | expresion <= termino | expresion >= termino | expresion && termino | expresion || termino
termino → ENTERO | REAL | CADENA | ID | ! expresion | ( expresion )
```

## Cómo Usar el Programa

### Opción 1: Menú Interactivo

```bash
python main.py
```

Se abrirá un menú que permite:

- Analizar archivos individuales
- Ver tokens generados
- Ejecutar análisis léxico y sintáctico
- Cargar todos los archivos de ejemplo

### Opción 2: Línea de Comandos

```bash
python main.py <ruta_al_archivo>
```

Analiza directamente el archivo especificado.

### Opción 3: Pruebas Automatizadas

```bash
python test_traductor.py
```

Ejecuta un conjunto de pruebas en todos los archivos de ejemplo y genera un reporte.

## Pruebas

El proyecto incluye cuatro archivos de prueba:

### 1. `ejemplos/correcto.txt`

Código sintáctica y léxicamente correcto de una función suma.

- **Resultado esperado**: Análisis exitoso en ambas fases

### 2. `ejemplos/error_lexico.txt`

Contiene un carácter inválido (`@`) que no es reconocido por el analizador léxico.

- **Resultado esperado**: Error léxico detectado en línea 3

### 3. `ejemplos/error_sintactico.txt`

Falta un punto y coma después de una declaración de variable.

- **Resultado esperado**: Error sintáctico detectado

### 4. `ejemplos/complejo.txt`

Código más complejo con estructuras de control anidadas.

- **Resultado esperado**: Análisis exitoso en ambas fases

## Resultados de Pruebas

```
Total de pruebas: 4
Pruebas pasadas: 4
Pruebas fallidas: 0
✓ ¡Todas las pruebas pasaron!
```

## Calidad del Código

### Buenas Prácticas Implementadas

1. **Modularización**: Cada componente (léxico, sintáctico) está separado en módulos
2. **Documentación**: Todas las funciones incluyen docstrings explicativos
3. **Manejo de Errores**: Excepciones informativas y recuperables
4. **Nombres Descriptivos**: Variables y funciones con nombres claros
5. **Estructura Limpia**: Organización lógica del código

### Tecnologías Utilizadas

- **Python 3**: Lenguaje de programación
- **Regex**: Para el análisis léxico
- **Tabla LR**: Para el análisis sintáctico determinista

## Extensiones Posibles

El diseño permite fácilmente:

1. **Agregar nuevos tokens**: Solo modificar patrones en `lexico.py`
2. **Cambiar la gramática**: Reemplazar tabla LR con una nueva
3. **Análisis semántico**: Agregar fase posterior al sintáctico
4. **Generación de código**: Agregar código generador
5. **Optimización**: Agregar optimizador de código

## Requisitos

- Python 3.6 o superior
- No requiere dependencias externas

## Ejecución

```bash
# Opción 1: Menú interactivo
python main.py

# Opción 2: Analizar archivo específico
python main.py ejemplos/correcto.txt

# Opción 3: Ejecutar pruebas
python test_traductor.py
```

## Conclusiones

Este traductor implementa satisfactoriamente:

- ✓ Identificación correcta de todos los tokens
- ✓ Detección y reporte preciso de errores léxicos
- ✓ Detección y reporte de errores sintácticos
- ✓ Código bien organizado y documentado
- ✓ Pruebas exhaustivas de funcionalidad

El proyecto demuestra una comprensión sólida de compiladores, tokenización y análisis sintáctico determinista.
