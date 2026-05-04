"""
Script de pruebas para el traductor léxico y sintáctico.
Verifica que todos los analizadores funcionan correctamente.
"""

from lexico.lexico import tokenize
from sintactico.parserLR import parse
import os

def test_lexico(ruta_archivo):
    """Prueba el analizador léxico con un archivo."""
    print(f"\n{'='*60}")
    print(f"Prueba Léxica: {os.path.basename(ruta_archivo)}")
    print(f"{'='*60}")
    
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            codigo = f.read()
        
        tokens = tokenize(codigo)
        print(f"✓ Análisis léxico exitoso")
        print(f"  Tokens encontrados: {len(tokens)}")
        return True, tokens
    
    except Exception as e:
        print(f"✗ Error léxico detectado:")
        print(f"  {e}")
        return False, None

def test_sintactico(tokens, ruta_archivo, ruta_gramatica):
    """Prueba el analizador sintáctico."""
    print(f"\nPrueba Sintáctica: {os.path.basename(ruta_archivo)}")
    print("-" * 60)
    
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            codigo = f.read()
        
        parse(ruta_gramatica, codigo)
        print(f"✓ Análisis sintáctico exitoso")
        return True
    
    except Exception as e:
        print(f"✗ Error sintáctico detectado:")
        print(f"  {e}")
        return False

def main():
    """Ejecuta todas las pruebas."""
    print("\n" + "="*60)
    print("PRUEBAS DEL TRADUCTOR LÉXICO Y SINTÁCTICO")
    print("="*60)
    
    ruta_gramatica = "gramatica/compilador.lr"
    archivos_test = [
        ("ejemplos/correcto.txt", "debe_pasar", True),
        ("ejemplos/error_lexico.txt", "debe_fallar_lexico", False),
        ("ejemplos/error_sintactico.txt", "debe_fallar_sintactico", False),
        ("ejemplos/complejo.txt", "debe_pasar", True),
    ]
    
    resultados = []
    
    for ruta_archivo, tipo_prueba, debe_pasar in archivos_test:
        if not os.path.exists(ruta_archivo):
            print(f"\n⚠ Archivo no encontrado: {ruta_archivo}")
            resultados.append({
                "archivo": ruta_archivo,
                "estado": "NO_ENCONTRADO"
            })
            continue
        
        # Test léxico
        lexico_ok, tokens = test_lexico(ruta_archivo)
        
        # Determinar resultado esperado
        if tipo_prueba == "debe_fallar_lexico":
            lexico_resultado = not lexico_ok  # Esperamos fallo
        else:
            lexico_resultado = lexico_ok  # Esperamos éxito
        
        # Test sintáctico solo si el análisis léxico fue exitoso
        sintactico_ok = False
        if lexico_ok:
            sintactico_ok = test_sintactico(tokens, ruta_archivo, ruta_gramatica)
        
        # Determinar resultado esperado para sintáctico
        if tipo_prueba == "debe_fallar_sintactico":
            sintactico_resultado = not sintactico_ok  # Esperamos fallo
        elif tipo_prueba == "debe_fallar_lexico":
            sintactico_resultado = True  # No se ejecuta sintáctico
        else:
            sintactico_resultado = sintactico_ok  # Esperamos éxito
        
        # Guardar resultado
        estado_final = "PASÓ" if (lexico_resultado and sintactico_resultado) else "FALLÓ"
        
        resultados.append({
            "archivo": ruta_archivo,
            "lexico": "✓" if lexico_resultado else "✗",
            "sintactico": "✓" if sintactico_resultado else "✗",
            "estado": estado_final
        })
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    print(f"\n{'Archivo':<30} {'Léxico':<10} {'Sintáctico':<10} {'Estado':<15}")
    print("-" * 65)
    
    pruebas_pasadas = 0
    for resultado in resultados:
        archivo = os.path.basename(resultado.get("archivo", ""))
        lexico = resultado.get("lexico", "-")
        sintactico = resultado.get("sintactico", "-")
        estado = resultado.get("estado", "")
        
        print(f"{archivo:<30} {lexico:<10} {sintactico:<10} {estado:<15}")
        
        if estado == "PASÓ":
            pruebas_pasadas += 1
    
    print("-" * 65)
    print(f"\nTotal de pruebas: {len(resultados)}")
    print(f"Pruebas pasadas: {pruebas_pasadas}")
    print(f"Pruebas fallidas: {len(resultados) - pruebas_pasadas}")
    
    if pruebas_pasadas == len(resultados):
        print("\n✓ ¡Todas las pruebas pasaron!")
    else:
        print("\n✗ Algunas pruebas fallaron.")
    
    return pruebas_pasadas == len(resultados)

if __name__ == "__main__":
    exito = main()
    exit(0 if exito else 1)
