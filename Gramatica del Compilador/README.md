@'
# 📘 Gramática del Compilador

Este subproyecto implementa un analizador sintáctico **LR(1)** junto con un analizador léxico sencillo. Se utiliza para cargar una gramática en formato LR, procesar una cadena de entrada y determinar si pertenece al lenguaje definido.

---

## 🧩 Estructura de archivos

- `cargar_lr.py`  
  Lee los archivos generados de la gramática (`.lr`, `.csv`, `.inf`) y construye las tablas de análisis.

- `parserLR.py`  
  Contiene el núcleo del analizador sintáctico LR(1). Usa las tablas cargadas para decidir desplazamientos/reducciones.

- `llexico.py`  
  Proporciona el analizador léxico que tokeniza la entrada de acuerdo a la gramática.

- `pila.py`  
  Implementa una pila auxiliar utilizada por el parser para almacenar estados y símbolos.

- `main.py`  
  Programa principal que coordina la lectura de la gramática, la tokenización de un archivo de entrada y la llamada al parser.

- `compilador.lr`, `compilador.csv`, `compilador.inf`  
  Archivos de salida generados por una herramienta previa (o por `cargar_lr.py`) que describen la gramática en formato LR.

- `README.md`  
  Este documento.

---

## 🚀 Cómo usar el proyecto

1. **Preparar la gramática**  
   Si modifica la gramática, vuelva a generar los archivos `.lr`, `.csv` y `.inf` usando la herramienta correspondiente (fuera de este repositorio).

2. **Tokenizar y parsear un archivo**  
   \`\`\`bash
   cd "Gramatica del Compilador"
   python main.py <ruta_al_archivo_de_entrada>
   \`\`\`
   - El lexer (`llexico.py`) lee el archivo y produce una lista de tokens.
   - `parserLR.py` procesa los tokens con tablas cargadas desde `compilador.lr`.
   - En pantalla se mostrará si la cadena es aceptada o se reporta un error sintáctico.

3. **Ejemplo mínimo**  
   Suponga que tenemos un archivo `entrada.txt` con código en el lenguaje definido.  
   \`\`\`text
   if ( x ) { y = 2; }
   \`\`\`
   > `python main.py entrada.txt`  
   Si la gramática admite esa sintaxis, el parser imprimirá un mensaje de aceptación.

---

## 🔧 Dependencias

- Python 3.x (probado con 3.10+)
- No se requieren librerías externas; todo está en la biblioteca estándar.

---

## 🛠️ Desarrollo

- La lógica del parser está diseñada para ser didáctica: estados y acciones se mantienen en `parserLR.py`.
- Para depurar, se puede añadir impresión de la pila o de los tokens en `main.py`.
- Los módulos están separados para facilitar pruebas unitarias (aunque no se incluyen en este repositorio).

---

## 📄 Licencia y Créditos

Este proyecto forma parte de la asignatura *Traductores de Lenguajes II* en la **CUCEI**. Puedes adaptarlo libremente con atribución.

---

> 💡 **Tip:** si modificas la gramática, asegúrate de regenerar los archivos `.lr` antes de ejecutar `main.py`.
