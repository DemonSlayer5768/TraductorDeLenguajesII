""""
Objetivo:

Desarrollar un componente específico de un traductor (puede ser un compilador o un intérprete) para un lenguaje de programación simplificado. 
Este proyecto se realizará en varias fases, cada una centrada en una parte diferente del proceso de traducción.
Fase Actual: Análisis Léxico y sintactico 

Descripción:
En esta fase, deberás implementar el analizador léxico para el lenguaje de programación asignado. 
El lenguaje tendrá una sintaxis y un conjunto de tokens definidos previamente por el instructor. 
El analizador léxico deberá ser capaz de leer el código fuente y convertirlo en una secuencia de tokens que serán utilizados en fases posteriores del proceso de traducción.

Requerimientos:
    : Basado en la especificación del lenguaje proporcionada, define los tokens que formarán parte del lenguaje.
    Esto incluye palabras reservadas, identificadores, literales numéricos, operadores, etc.
    : Escribe tu propio analizador en el lenguaje de programación de tu elección. 
    El analizador debe poder leer un archivo de entrada con código fuente y producir una lista de tokens.
    : Tu analizador léxico debe ser capaz de manejar y reportar errores léxicos de manera adecuada, como caracteres inválidos o formatos incorrectos de tokens.

Entregables:
    : El código fuente de tu analizador léxico y sintactico, incluyendo cualquier estructura de datos utilizada para almacenar los tokens.
    : Un breve documento que explique tu diseño, las decisiones importantes que tomaste durante la implementación, y cómo se manejan los errores léxicos y sintacticos.
    : Archivos de entrada de muestra junto con la salida producida por tu analizador léxico y sintactico.
    Incluye casos que demuestren el manejo correcto de los tokens y también ejemplos que muestren cómo se manejan los errores léxicos.

Evaluación:
Tu tarea será evaluada en base a los siguientes criterios:
    : ¿Tu analizador léxico identifica correctamente todos los tokens definidos en la especificación del lenguaje?
    : ¿Tu analizador proporciona mensajes de error útiles y precisos para entradas inválidas?
    : ¿Tu código está bien organizado, comentado y sigue las buenas prácticas de programación?
    : ¿La documentación proporciona una buena visión general de tu implementación y decisiones
"""



from lexico.lexico import tokenize
from sintactico.parserLR import parse
import os

def analizar_archivo(ruta_archivo, mostrar_tokens=True):
    """
    Analiza un archivo de código fuente.
    
    Args:
        ruta_archivo: Ruta al archivo de código fuente
        mostrar_tokens: Si se deben mostrar los tokens (default: True)
    """
    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo '{ruta_archivo}' no existe.")
        return
    
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            codigo = f.read()
        
        print(f"\n{'='*60}")
        print(f"Analizando: {ruta_archivo}")
        print(f"{'='*60}\n")
        
        print("ANÁLISIS LÉXICO:")
        print("-" * 60)
        
        try:
            tokens = tokenize(codigo)
            
            if mostrar_tokens:
                for token in tokens:
                    print(token)
            else:
                print(f"Total de tokens encontrados: {len(tokens)}")
            
            print(f"\n✓ Análisis léxico completado correctamente")
            
        except Exception as e:
            print(f"✗ Error léxico detectado:")
            print(f"  {e}")
            return
        
        print("\n" + "="*60)
        print("ANÁLISIS SINTÁCTICO:")
        print("-" * 60)
        
        try:
            if parse("gramatica/compilador.lr", codigo):
                print("\n✓ Análisis sintáctico completado correctamente")
        except Exception as e:
            print(f"✗ Error sintáctico detectado:")
            print(f"  {e}")
        
        
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

def menu_principal():
    """Muestra un menú para seleccionar qué archivo analizar."""
    while True:
        print("\n" + "="*60)
        print("ANALIZADOR LÉXICO Y SINTÁCTICO")
        print("="*60)
        print("\nSelecciona un archivo para analizar:")
        print("1. correcto.txt - Código sintácticamente correcto")
        print("2. error_lexico.txt - Código con error léxico")
        print("3. error_sintactico.txt - Código con error sintáctico")
        print("4. complejo.txt - Código más complejo")
        print("5. Analizar todos los archivos")
        print("6. Salir")
        
        opcion = input("\nOpción (1-6): ").strip()
        
        archivos = {
            "1": ("ejemplos/correcto.txt", True),
            "2": ("ejemplos/error_lexico.txt", True),
            "3": ("ejemplos/error_sintactico.txt", True),
            "4": ("ejemplos/complejo.txt", True),
        }
        
        if opcion in archivos:
            analizar_archivo(archivos[opcion][0], archivos[opcion][1])
        elif opcion == "5":
            for ruta, _ in archivos.values():
                analizar_archivo(ruta, True)
        elif opcion == "6":
            print("\n¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

def main():
    """Función principal."""
    import sys
    
    # Si se pasan argumentos, analizar ese archivo directamente
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
        analizar_archivo(archivo, True)
    else:
        # Mostrar menú interactivo
        menu_principal()

if __name__ == "__main__":
    main()