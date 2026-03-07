# TraductorDeLenguajesII

Repositorio de proyectos para el curso de Traductores de Lenguajes II. Este repositorio contiene implementaciones de diferentes componentes de traductores y compiladores, desde analizadores léxicos y sintácticos hasta generadores de código para validación de datos.

## Proyectos Incluidos

### 1. Analizador Léxico (`Analizador Lexico/`)
Implementa un analizador léxico básico en Python que tokeniza código fuente, reconociendo palabras reservadas, identificadores, literales numéricos, operadores y símbolos. Incluye manejo de errores léxicos y generación de tokens con posición (línea y columna).

**Tecnologías:** Python  
**Características:** Tokenización, manejo de errores, estructura de datos Token

### 2. Analizador Sintáctico (`Analizador Sintactico/`)
Desarrolla un parser LR(1) en Python para analizar la sintaxis de un lenguaje simplificado. Utiliza pilas y tablas de parsing precomputadas para validar la estructura gramatical del código fuente.

**Tecnologías:** Python  
**Características:** Parser LR(1), manejo de pilas, validación sintáctica

### 3. Construcción del Traductor (`Construccion Traductor/`)
Proyecto completo que combina análisis léxico y sintáctico para implementar un traductor funcional. Incluye un lenguaje simplificado con funciones, variables, expresiones y estructuras de control (if, while). Maneja errores tanto léxicos como sintácticos.

**Tecnologías:** Python  
**Características:** Traductor completo, lenguaje simplificado, expresiones, funciones, manejo de errores

### 4. Gramática del Compilador (`Gramatica del Compilador/`)
Define la gramática formal del lenguaje de programación y genera las tablas LR necesarias para el parsing. Incluye especificación de reglas gramaticales, tokens y algoritmos para construcción de tablas de análisis.

**Tecnologías:** Python  
**Características:** Definición de gramática, generación de tablas LR, especificación de lenguaje

### 5. Validación de Datos (`Validacion-Datos/`)
Traductor especializado que convierte esquemas JSON Schema en código JavaScript funcional para validación automática de datos. Utiliza la biblioteca Ajv para generar validadores robustos con soporte para estructuras complejas, formatos y restricciones personalizadas.

**Tecnologías:** JavaScript, Node.js, Ajv, JSON Schema  
**Características:** Generación automática de código, validación de esquemas complejos, soporte para formatos (email, fechas), integración con aplicaciones web

## Tecnologías Principales

- **Python**: Análisis léxico y sintáctico, construcción de traductores
- **JavaScript/Node.js**: Generación de código de validación
- **JSON Schema**: Especificación de esquemas de datos
- **Ajv**: Biblioteca de validación JSON Schema
- **Git**: Control de versiones

## Estructura del Repositorio

```
TraductorDeLenguajesII/
├── Analizador Lexico/          # Análisis léxico básico
├── Analizador Sintactico/      # Parser LR(1)
├── Construccion Traductor/     # Traductor completo
├── Gramatica del Compilador/   # Definición de gramática
├── Validacion-Datos/           # Generador de validadores JS
├── .gitignore                  # Archivos ignorados
└── README.md                   # Este archivo
```

## Cómo Usar

Cada proyecto es independiente y contiene su propia documentación:

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/DemonSlayer5768/TraductorDeLenguajesII.git
   cd TraductorDeLenguajesII
   ```

2. **Navega al proyecto deseado:**
   ```bash
   cd "Construccion Traductor"  # o cualquier otro proyecto
   ```

3. **Instala dependencias (para proyectos Node.js):**
   ```bash
   npm install
   ```

4. **Ejecuta el proyecto según su documentación específica**

## Objetivos de Aprendizaje

- Comprensión de los componentes de un compilador/traductor
- Implementación de analizadores léxicos y sintácticos
- Trabajo con gramáticas formales y tablas de parsing
- Generación automática de código
- Validación de datos con estándares modernos
- Desarrollo de aplicaciones prácticas usando conceptos teóricos

## Contribución

Este repositorio es parte de un proyecto educativo. Cada carpeta representa una fase diferente del aprendizaje en construcción de traductores de lenguajes.

## Licencia

Proyecto educativo - Todos los derechos reservados.
