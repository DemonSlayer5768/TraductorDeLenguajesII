"""
Script de prueba para el analizador semántico
Ejecuta los ejemplos y genera reportes
"""

from main import Lexer, SemanticAnalyzer
from datetime import datetime

# Ejemplo 1
EJEMPLO1 = """int main(){
float a;
int b;
int c;
c = a+b;
c = suma(8,9);
}"""

# Ejemplo 2
EJEMPLO2 = """int a;
int suma(int a, int b){
return a+b;
}

int main(){
float a;
int b;
int c;
c = a+b;
c = suma(8.5,9.9);
}"""


def generate_report(codigo, ejemplo_num):
    """Genera un reporte de análisis"""
    print(f"\n{'='*70}")
    print(f"EJEMPLO {ejemplo_num} - ANÁLISIS SEMÁNTICO")
    print(f"{'='*70}\n")
    
    print("CÓDIGO FUENTE:")
    print("-" * 70)
    for i, linea in enumerate(codigo.strip().split('\n'), 1):
        print(f"{i:2d}  {linea}")
    print("-" * 70)
    
    # Análisis léxico
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()
    
    print("\nTOKENS IDENTIFICADOS:")
    for token in tokens[:-1]:  # Excluir EOF
        if token.type.value not in ['(', ')', '{', '}', ';', ',', '=', '+', '-', '*', '/']:
            print(f"  {token.type.value:15s} = {token.value:20s} (Línea {token.line}, Columna {token.column})")
    
    # Análisis semántico
    analyzer = SemanticAnalyzer()
    errors, warnings = analyzer.analyze(tokens)
    
    # Tabla de símbolos
    print("\nTABLA DE SÍMBOLOS:")
    print("-" * 70)
    
    if analyzer.variables:
        print("\nVARIABLES:")
        for var_name, var in analyzer.variables.items():
            print(f"  • {var.type:10s} {var_name}")
    
    if analyzer.functions:
        print("\nFUNCIONES:")
        for func_name, func in analyzer.functions.items():
            params_str = ", ".join(f"{ptype} {pname}" for pname, ptype in func.params)
            print(f"  • {func.return_type} {func.name}({params_str})")
    
    # Resultados
    print("\n" + "="*70)
    print("RESULTADOS DEL ANÁLISIS:")
    print("="*70)
    
    if errors:
        print(f"\n ERRORES ENCONTRADOS ({len(errors)}):")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
    else:
        print("\n✓ NO SE ENCONTRARON ERRORES SEMÁNTICOS")
    
    if warnings:
        print(f"\n  ADVERTENCIAS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
    else:
        print("\n✓ NO SE ENCONTRARON ADVERTENCIAS")
    
    # Estadísticas
    print("\n" + "-"*70)
    print(f"ESTADÍSTICAS:")
    print(f"  • Total de errores: {len(errors)}")
    print(f"  • Total de advertencias: {len(warnings)}")
    print(f"  • Variables declaradas: {len(analyzer.variables)}")
    print(f"  • Funciones definidas: {len(analyzer.functions)}")
    print(f"  • Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "    ANALIZADOR SEMÁNTICO DE C - GENERACIÓN DE REPORTES    ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    # Analizar y reportar
    generate_report(EJEMPLO1, 1)
    generate_report(EJEMPLO2, 2)
    
    print("\n" + "="*70)
    print("FIN DE LOS REPORTES")
    print("="*70 + "\n")
