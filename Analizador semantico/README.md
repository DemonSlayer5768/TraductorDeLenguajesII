# Analizador Semántico de C

## Descripción

Analizador semántico para validar código C básico. Detecta errores como:

- Variables no declaradas
- Incompatibilidad de tipos
- Funciones no definidas
- Argumentos incorrectos en funciones

## Características

### Validación Semántica

- **Declaración de variables**: Detecta redeclaraciones y uso de variables no declaradas
- **Compatibilidad de tipos**: Valida asignaciones entre tipos (int, float)
- **Llamadas a funciones**: Verifica que funciones sean definidas y argumentos sean compatibles
- **Operaciones aritméticas**: Detecta incompatibilidades en operaciones con diferentes tipos

### Análisis de Tipos

- Soporta tipos básicos: `int`, `float`, `void`
- Promueve automáticamente `int` a `float` en operaciones mixtas
- Valida asignaciones según compatibilidad

## Cómo Usar

### Ejecución

```bash
python main.py
```

### Interfaz Gráfica

1. **Área de código fuente**: Escribe o pega el código a analizar
2. **Botones de carga rápida**: Carga ejemplos predefinidos
3. **Botón Analizar**: Ejecuta el análisis semántico
4. **Pestañas de resultados**:
   - **Errores**: Muestra errores semánticos encontrados
   - **Advertencias**: Muestra advertencias
   - **Resumen**: Tabla de símbolos y estadísticas

## Ejemplos

### Ejemplo 1: Error de tipos en asignación

```c
int main(){
float a;
int b;
int c;
c = a+b;
c = suma(8,9);
}
```

**Errores esperados:**

- Línea 5: Incompatibilidad de tipos. Se intenta asignar 'float' a variable 'int'
- Línea 6: Función 'suma' no ha sido definida

### Ejemplo 2: Error de tipos en argumentos

```c
int a;
int suma(int a, int b){
return a+b;
}

int main(){
float a;
int b;
int c;
c = a+b;
c = suma(8.5,9.9);
}
```

**Errores esperados:**

- Línea 9: Incompatibilidad de tipos. Se intenta asignar 'float' a variable 'int'
- Línea 10: Argumentos incompatibles en función 'suma' (se esperaban int, se obtuvieron float)

## Estructura del Código

### Clases principales

#### `TokenType`

Enumeración de tipos de tokens (palabras clave, símbolos, números, etc.)

#### `Token`

Representa un token individual con tipo, valor, línea y columna

#### `Lexer`

Realiza el análisis léxico:

- Convierte código fuente en tokens
- Identifica números, identificadores, palabras clave y símbolos

#### `SemanticAnalyzer`

Realiza el análisis semántico:

- **Primera pasada**: Recolecta declaraciones de funciones
- **Segunda pasada**: Valida tipos, variables y funciones
- Genera tabla de símbolos

#### `SemanticAnalyzerGUI`

Proporciona interfaz gráfica con Tkinter:

- Editor de código
- Visor de errores/advertencias
- Tabla de símbolos

## Funcionalidades Implementadas

✓ Análisis léxico completo
✓ Análisis sintáctico básico
✓ Validación de tipos
✓ Tabla de símbolos
✓ Detección de variable no declaradas
✓ Validación de funciones
✓ Interfaz gráfica interactiva
✓ Reportes detallados

## Limitaciones

- No soporta estructuras complejas (while, for, if)
- No soporta arreglos
- No soporta punteros
- Análisis sintáctico limitado a funciones y variables
- Scope limitado a global y local

## Futuras Mejoras

- Soporte para bucles y condicionales
- Análisis de scope más completo
- Soporte para estructuras (struct)
- Análisis de alcance de variables más detallado
- Exportación de reportes a PDF
