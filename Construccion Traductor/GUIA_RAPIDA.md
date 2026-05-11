## GUÍA RÁPIDA DE USO

### 1. Ejecutar el Analizador

#### Opción A: Menú Interactivo

```bash
python main.py
```git s

Permite seleccionar qué archivo analizar y ver los resultados detallados.

#### Opción B: Analizar Archivo Específico

```bash
python main.py ejemplos/correcto.txt
```

#### Opción C: Ejecutar Pruebas Automatizadas

```bash
python test_traductor.py
```

### 2. Ejemplos de Salida

#### Código Correcto

```
TIPO('int') [1:4]
IDENTIFICADOR('suma') [1:9]
...
✓ Análisis léxico completado correctamente
✓ Análisis sintáctico completado correctamente
```

#### Con Error Léxico

```
✗ Error léxico detectado:
Error léxico en línea 3, columna 23: caracter inválido '@'
```

#### Con Error Sintáctico

```
✓ Análisis léxico completado correctamente
✗ Error sintáctico detectado:
Error sintáctico: token inesperado 'resultado' en línea 3, columna 14
```

### 3. Archivos de Ejemplo

- `ejemplos/correcto.txt` - Código válido
- `ejemplos/error_lexico.txt` - Contiene carácter inválido `@`
- `ejemplos/error_sintactico.txt` - Falta punto y coma
- `ejemplos/complejo.txt` - Código con estructuras anidadas

### 4. Agregar Nuevo Código para Analizar

```bash
# Crear archivo nuevo
echo 'int x; x = 5;' > ejemplos/micodigo.txt

# Analizar
python main.py ejemplos/micodigo.txt
```

### 5. Información Técnica

**Componentes**:

- `lexico/`: Analizador léxico
- `sintactico/`: Analizador sintáctico LR
- `gramatica/`: Tabla de análisis LR

**Documentación Completa**: Ver `DOCUMENTACION.md`

**Entregables**: Ver `ENTREGABLES.md`
