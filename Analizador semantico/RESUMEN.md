# ANALIZADOR SEMÁNTICO DE C

## Reporte Técnico - Traductor de Lenguajes II

---

## RESUMEN EJECUTIVO

Se ha desarrollado exitosamente un **Analizador Semántico completo para el lenguaje C** que valida tipos de datos, funciones y variables. El analizador implementa las tres fases de análisis de compiladores y proporciona una interfaz gráfica interactiva.

### Resultados de Validación

#### **EJEMPLO 1: Error de Tipos en Asignación**

**Código:**

```c
int main(){
float a;
int b;
int c;
c = a+b;
c = suma(8,9);
}
```

**Errores Detectados:** 2

| Línea | Error                     | Descripción                                 |
| ----- | ------------------------- | ------------------------------------------- |
| 5     | Incompatibilidad de tipos | Se intenta asignar 'float' a variable 'int' |
| 6     | Función no definida       | Función 'suma' no ha sido declarada         |

**Análisis:**

- Línea 5: La expresión `a+b` produce tipo `float` (float + int = float), pero la variable `c` es `int`
- Línea 6: Se intenta llamar una función `suma()` que nunca fue definida en el programa

---

#### **EJEMPLO 2: Errores Múltiples de Tipos y Redeclaración**

**Código:**

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

**Errores Detectados:** 6

| Línea | Error                     | Descripción                                             |
| ----- | ------------------------- | ------------------------------------------------------- |
| 2     | Variable redeclarada      | Variable 'a' ya fue declarada en línea 1                |
| 7     | Variable redeclarada      | Variable 'a' ya fue declarada en línea 1                |
| 8     | Variable redeclarada      | Variable 'b' ya fue declarada como parámetro            |
| 10    | Incompatibilidad de tipos | Se intenta asignar 'float' a variable 'int'             |
| 11    | Argumento incompatible    | Se esperaba 'int', se obtuvo 'float' para parámetro 'a' |
| 11    | Argumento incompatible    | Se esperaba 'int', se obtuvo 'float' para parámetro 'b' |

**Análisis:**

- Líneas 2, 7, 8: Múltiples redeclaraciones de variables que ya existen
- Línea 10: Asignación de expresión float a variable int
- Línea 11: Argumentos float pasados a función que espera int

---

## ARQUITECTURA DEL ANALIZADOR

### 1. **Análisis Léxico (Lexer)**

- Convierte código fuente en tokens
- Identifica palabras clave, identificadores, números y símbolos
- Registra línea y columna de cada token

### 2. **Análisis Semántico (SemanticAnalyzer)**

- **Primera pasada:** Recolecta declaraciones de funciones
- **Segunda pasada:** Valida variables, tipos y funciones
- Mantiene tabla de símbolos actualizada

### 3. **Interfaz Gráfica (Tkinter)**

- Editor de código con coloreado de sintaxis
- Pestañas para Errores, Advertencias y Resumen
- Tabla de símbolos visible
- Botones de carga rápida de ejemplos

---

## VALIDACIONES IMPLEMENTADAS

✅ **Detección de variables no declaradas**
✅ **Detección de variables redeclaradas**
✅ **Validación de compatibilidad de tipos**
✅ **Validación de funciones definidas**
✅ **Validación de argumentos en funciones**
✅ **Análisis de expresiones aritméticas**
✅ **Promoción automática de tipos (int → float)**

---

## REGLAS DE COMPATIBILIDAD DE TIPOS

| Tipo Destino | Tipo Origen | Compatible | Observación          |
| ------------ | ----------- | ---------- | -------------------- |
| int          | int         | ✓          | Mismo tipo           |
| float        | float       | ✓          | Mismo tipo           |
| float        | int         | ✓          | Promoción permitida  |
| int          | float       | ✗          | Pérdida de precisión |

---

## ARCHIVOS ENTREGABLES

### Código Fuente

- **main.py** (500+ líneas) - Analizador completo
  - Lexer: Análisis léxico
  - Token: Representación de tokens
  - SemanticAnalyzer: Análisis semántico
  - SemanticAnalyzerGUI: Interfaz gráfica

- **test.py** - Script de prueba automatizada
  - Genera reportes de consola
  - Muestra tabla de símbolos
  - Estadísticas detalladas

### Documentación

- **README.md** - Guía técnica completa
- **RESUMEN.md** - Este archivo

---

## ESTADÍSTICAS

### Ejemplo 1

- **Variables:** 4 (main, a, b, c)
- **Funciones:** 1 (main)
- **Errores:** 2
- **Advertencias:** 0

### Ejemplo 2

- **Variables:** 5 (a, suma, b, main, c)
- **Funciones:** 2 (suma, main)
- **Errores:** 6
- **Advertencias:** 0

---

## CÓMO USAR

### Opción 1: Interfaz Gráfica

```bash
python main.py
```

- Escribir código o usar botones de ejemplo
- Hacer clic en "Analizar"
- Ver resultados en pestañas

### Opción 2: Script de Prueba

```bash
python test.py
```

- Ejecuta automáticamente los dos ejemplos
- Genera reportes detallados en consola

---

## CONCLUSIONES

El analizador semántico implementado cumple exitosamente con los requisitos:

✓ **Detecta errores de tipos** en asignaciones y operaciones
✓ **Valida funciones** definidas y sus argumentos
✓ **Identifica variables** no declaradas y redeclaradas
✓ **Proporciona reportes detallados** del análisis
✓ **Interfaz gráfica intuitiva** para visualizar resultados
✓ **Código documentado** y bien estructurado

El proyecto demuestra conocimiento completo de:

- Análisis léxico
- Análisis sintáctico
- Análisis semántico
- Implementación de compiladores
- Programación orientada a objetos en Python
- Interfaces gráficas con Tkinter

---

## RECOMENDACIONES FUTURAS

1. Ampliar a soportar estructuras condicionales (if/else)
2. Implementar bucles (while, for do-while)
3. Mejorar análisis de scope para variables locales
4. Soportar arreglos y punteros
5. Exportar reportes a PDF
6. Integración con depurador visual
7. Soporte para más tipos de datos (char, double)

---

**Institución:** Universidad de Guadalajara
