import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime


class TokenType(Enum):
    """Tipos de tokens"""
    INT = "int"
    FLOAT = "float"
    VOID = "void"
    ID = "ID"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    SEMICOLON = ";"
    COMMA = ","
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    MULT = "*"
    DIV = "/"
    NUMBER = "NUMBER"
    EOF = "EOF"
    RETURN = "return"


@dataclass
class Token:
    """Representa un token en el código"""
    type: TokenType
    value: str
    line: int
    column: int


@dataclass
class Variable:
    """Representa una variable"""
    name: str
    type: str
    scope: str


@dataclass
class Function:
    """Representa una función"""
    name: str
    return_type: str
    params: List[Tuple[str, str]]  # [(nombre, tipo), ...]
    defined: bool


class Lexer:
    """Análisis léxico"""
    
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        self.keywords = {
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'void': TokenType.VOID,
            'return': TokenType.RETURN,
        }
        
        self.symbols = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
            '=': TokenType.ASSIGN,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULT,
            '/': TokenType.DIV,
        }

    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.code):
            return None
        return self.code[self.pos]
    
    def peek_char(self, offset=1) -> Optional[str]:
        pos = self.pos + offset
        if pos >= len(self.code):
            return None
        return self.code[pos]
    
    def advance(self):
        if self.pos < len(self.code) and self.code[self.pos] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def read_number(self) -> Token:
        start_line = self.line
        start_column = self.column
        num_str = ''
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            num_str += self.current_char()
            self.advance()
        
        return Token(TokenType.NUMBER, num_str, start_line, start_column)
    
    def read_identifier(self) -> Token:
        start_line = self.line
        start_column = self.column
        id_str = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()
        
        token_type = self.keywords.get(id_str, TokenType.ID)
        return Token(token_type, id_str, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        while self.current_char():
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            # Números
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
            # Identificadores y palabras clave
            elif self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.read_identifier())
            # Símbolos
            elif self.current_char() in self.symbols:
                sym = self.current_char()
                token = Token(self.symbols[sym], sym, self.line, self.column)
                self.tokens.append(token)
                self.advance()
            else:
                self.advance()
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens


class SemanticAnalyzer:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.global_vars = {}
        self.local_vars = {}
        self.functions = {}
        self.current_scope = "global"

    def dime_tipo(self, tipo_str):
        return {
            "int": 'i',
            "float": 'f',
            "void": 'v'
        }.get(tipo_str, 'v')

    def _get_variable(self, name):
        # Local primero
        if self.current_scope in self.local_vars:
            if name in self.local_vars[self.current_scope]:
                return self.local_vars[self.current_scope][name]
        # Global
        return self.global_vars.get(name)

    def _is_compatible(self, target, source):
        if target == source:
            return True
        if target == 'f' and source == 'i':
            return True
        return False

    def add_variable(self, name, tipo_str, line):
        tipo = self.dime_tipo(tipo_str)

        if self.current_scope == "global":
            if name in self.global_vars:
                self.errors.append(f"Línea {line}: Variable global '{name}' redefinida")
            else:
                self.global_vars[name] = Variable(name, tipo, "global")
        else:
            if self.current_scope not in self.local_vars:
                self.local_vars[self.current_scope] = {}

            if name in self.local_vars[self.current_scope]:
                self.errors.append(f"Línea {line}: Variable local '{name}' redefinida")
            else:
                self.local_vars[self.current_scope][name] = Variable(name, tipo, self.current_scope)

    def add_function(self, name, return_type, params, line):
        if name in self.functions:
            self.errors.append(f"Línea {line}: Función '{name}' redefinida")
        else:
            self.functions[name] = Function(
                name=name,
                return_type=self.dime_tipo(return_type),
                params=[(pname, self.dime_tipo(ptype)) for pname, ptype in params],
                defined=True
            )

    def analyze(self, tokens):
        self.errors.clear()
        self.warnings.clear()
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Detectar declaración de función
            if token.type in (TokenType.INT, TokenType.FLOAT, TokenType.VOID):
                if i + 1 < len(tokens) and tokens[i + 1].type == TokenType.ID:
                    # Verificar si es función
                    if i + 2 < len(tokens) and tokens[i + 2].type == TokenType.LPAREN:
                        # Es una función
                        func_name = tokens[i + 1].value
                        return_type = token.value
                        
                        # Extraer parámetros
                        j = i + 3
                        params = []
                        while j < len(tokens) and tokens[j].type != TokenType.RPAREN:
                            if tokens[j].type in (TokenType.INT, TokenType.FLOAT):
                                param_type = tokens[j].value
                                if j + 1 < len(tokens) and tokens[j + 1].type == TokenType.ID:
                                    param_name = tokens[j + 1].value
                                    params.append((param_name, param_type))
                                    j += 2
                                    if j < len(tokens) and tokens[j].type == TokenType.COMMA:
                                        j += 1
                                    continue
                            j += 1
                        
                        self.add_function(func_name, return_type, params, token.line)
                        
                        # Cambiar al ámbito de la función
                        self.current_scope = func_name
                        if func_name not in self.local_vars:
                            self.local_vars[func_name] = {}
                        
                        # Agregar parámetros como variables locales
                        for param_name, param_type in params:
                            self.add_variable(param_name, param_type, token.line)
                        
                        # Saltar a la llave de apertura
                        while i < len(tokens) and tokens[i].type != TokenType.LBRACE:
                            i += 1
                        i += 1
                        continue
                    
                    # Si no es función, es declaración de variable
                    else:
                        self.add_variable(tokens[i + 1].value, token.value, token.line)
                        i += 2
                        continue
            
            # Detectar fin de función
            if token.type == TokenType.RBRACE and self.current_scope != "global":
                self.current_scope = "global"
            
            # Detectar asignaciones y usos de variables
            if token.type == TokenType.ID:
                # Verificar si es una llamada a función
                if i + 1 < len(tokens) and tokens[i + 1].type == TokenType.LPAREN:
                    # Llamada a función
                    func_name = token.value
                    if func_name not in self.functions:
                        self.errors.append(f"Línea {token.line}: Función '{func_name}' no definida")
                    # Verificar argumentos (simplificado)
                    i += 1
                else:
                    # Uso de variable
                    var = self._get_variable(token.value)
                    if not var:
                        self.errors.append(f"Línea {token.line}: Variable '{token.value}' no definida")
                    
                    # Verificar asignación
                    if i + 1 < len(tokens) and tokens[i + 1].type == TokenType.ASSIGN:
                        # Análisis simplificado de tipos en la asignación
                        i += 2
                        # Aquí se podría agregar análisis de tipos de la expresión
            
            i += 1
        
        return self.errors, self.warnings


class CompilerIDE:
    """Interfaz gráfica para el compilador"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador - Analizador Léxico y Semántico")
        self.root.geometry("1200x700")
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Crear widgets
        self.create_widgets()
        
        # Variable para el código de ejemplo
        self.example_code = '''int x;
float y;

int suma(int a, int b) {
    int resultado;
    resultado = a + b;
    return resultado;
}

void main() {
    int z;
    z = suma(5, 10);
    
    // Prueba de errores (descomentar para probar)
    // int x;  // Error: variable redeclarada
    // w = 10; // Error: variable no definida
    // funcion_no_existe(); // Error: función no definida
}'''
        
        # Cargar código de ejemplo
        self.code_area.insert(1.0, self.example_code)
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Analizador Léxico y Semántico", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Frame para el área de código y botones
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        top_frame.columnconfigure(0, weight=1)
        top_frame.rowconfigure(0, weight=1)
        
        # Área de código
        code_label = ttk.Label(top_frame, text="Código Fuente:", font=('Arial', 10, 'bold'))
        code_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.code_area = scrolledtext.ScrolledText(top_frame, height=15, font=('Courier', 10))
        self.code_area.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Frame para botones
        button_frame = ttk.Frame(top_frame)
        button_frame.grid(row=2, column=0, pady=10)
        
        # Botones
        self.analyze_btn = ttk.Button(button_frame, text="Analizar Código", 
                                       command=self.analyze_code, width=15)
        self.analyze_btn.grid(row=0, column=0, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="Limpiar", 
                                     command=self.clear_all, width=10)
        self.clear_btn.grid(row=0, column=1, padx=5)
        
        self.load_example_btn = ttk.Button(button_frame, text="Cargar Ejemplo", 
                                            command=self.load_example, width=15)
        self.load_example_btn.grid(row=0, column=2, padx=5)
        
        # Frame para resultados (usando Notebook con pestañas)
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        main_frame.rowconfigure(2, weight=1)
        
        # Pestaña de Tokens
        tokens_frame = ttk.Frame(notebook)
        notebook.add(tokens_frame, text="Tokens")
        
        self.tokens_text = scrolledtext.ScrolledText(tokens_frame, font=('Courier', 9))
        self.tokens_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña de Errores
        errors_frame = ttk.Frame(notebook)
        notebook.add(errors_frame, text="Errores y Advertencias")
        
        self.errors_text = scrolledtext.ScrolledText(errors_frame, font=('Courier', 9))
        self.errors_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña de Tabla de Símbolos
        symbols_frame = ttk.Frame(notebook)
        notebook.add(symbols_frame, text="Tabla de Símbolos")
        
        self.symbols_text = scrolledtext.ScrolledText(symbols_frame, font=('Courier', 9))
        self.symbols_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Barra de estado
        self.status_bar = ttk.Label(main_frame, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def analyze_code(self):
        """Ejecuta el análisis léxico y semántico del código"""
        
        # Limpiar resultados anteriores
        self.tokens_text.delete(1.0, tk.END)
        self.errors_text.delete(1.0, tk.END)
        self.symbols_text.delete(1.0, tk.END)
        
        # Obtener código
        code = self.code_area.get(1.0, tk.END)
        
        if not code.strip():
            messagebox.showwarning("Advertencia", "Por favor ingrese código para analizar")
            return
        
        # Actualizar estado
        self.status_bar.config(text="Analizando código...")
        self.root.update()
        
        try:
            # Análisis léxico
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            
            # Mostrar tokens
            self.tokens_text.insert(tk.END, "═" * 80 + "\n")
            self.tokens_text.insert(tk.END, f"{'TIPO':<20} {'VALOR':<20} {'LÍNEA':<8} {'COLUMNA':<8}\n")
            self.tokens_text.insert(tk.END, "═" * 80 + "\n")
            
            for token in tokens:
                if token.type != TokenType.EOF:
                    self.tokens_text.insert(tk.END, 
                        f"{token.type.value:<20} {token.value:<20} {token.line:<8} {token.column:<8}\n")
            
            self.tokens_text.insert(tk.END, f"\nTotal de tokens: {len(tokens) - 1}\n")
            
            # Análisis semántico
            semantic = SemanticAnalyzer()
            errors, warnings = semantic.analyze(tokens)
            
            # Mostrar errores y advertencias
            if errors or warnings:
                self.errors_text.insert(tk.END, "═" * 80 + "\n")
                self.errors_text.insert(tk.END, "ERRORES ENCONTRADOS:\n")
                self.errors_text.insert(tk.END, "═" * 80 + "\n\n")
                
                for error in errors:
                    self.errors_text.insert(tk.END, f"❌ {error}\n")
                
                if warnings:
                    self.errors_text.insert(tk.END, "\n" + "═" * 80 + "\n")
                    self.errors_text.insert(tk.END, "ADVERTENCIAS:\n")
                    self.errors_text.insert(tk.END, "═" * 80 + "\n\n")
                    for warning in warnings:
                        self.errors_text.insert(tk.END, f"⚠️ {warning}\n")
                
                self.status_bar.config(text=f"Análisis completado - {len(errors)} errores, {len(warnings)} advertencias")
            else:
                self.errors_text.insert(tk.END, "✅ ¡No se encontraron errores semánticos!\n")
                self.status_bar.config(text="Análisis completado - Sin errores")
            
            # Mostrar tabla de símbolos
            self.symbols_text.insert(tk.END, "═" * 80 + "\n")
            self.symbols_text.insert(tk.END, "VARIABLES GLOBALES:\n")
            self.symbols_text.insert(tk.END, "═" * 80 + "\n")
            
            if semantic.global_vars:
                for var_name, var_info in semantic.global_vars.items():
                    tipo_str = { 'i': 'int', 'f': 'float' }.get(var_info.type, var_info.type)
                    self.symbols_text.insert(tk.END, f"  • {var_name} : {tipo_str}\n")
            else:
                self.symbols_text.insert(tk.END, "  No hay variables globales\n")
            
            self.symbols_text.insert(tk.END, "\n" + "═" * 80 + "\n")
            self.symbols_text.insert(tk.END, "FUNCIONES:\n")
            self.symbols_text.insert(tk.END, "═" * 80 + "\n")
            
            if semantic.functions:
                for func_name, func_info in semantic.functions.items():
                    tipo_str = { 'i': 'int', 'f': 'float', 'v': 'void' }.get(func_info.return_type, func_info.return_type)
                    params_str = ", ".join([f"{p[1]} {p[0]}" for p in func_info.params])
                    self.symbols_text.insert(tk.END, f"  • {func_name}({params_str}) : {tipo_str}\n")
                    
                    # Mostrar variables locales
                    if func_name in semantic.local_vars and semantic.local_vars[func_name]:
                        self.symbols_text.insert(tk.END, f"    Variables locales:\n")
                        for var_name, var_info in semantic.local_vars[func_name].items():
                            tipo_local = { 'i': 'int', 'f': 'float' }.get(var_info.type, var_info.type)
                            self.symbols_text.insert(tk.END, f"      - {var_name} : {tipo_local}\n")
            else:
                self.symbols_text.insert(tk.END, "  No hay funciones definidas\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante el análisis:\n{str(e)}")
            self.status_bar.config(text="Error durante el análisis")
            import traceback
            traceback.print_exc()
    
    def clear_all(self):
        """Limpia todas las áreas de texto"""
        self.code_area.delete(1.0, tk.END)
        self.tokens_text.delete(1.0, tk.END)
        self.errors_text.delete(1.0, tk.END)
        self.symbols_text.delete(1.0, tk.END)
        self.status_bar.config(text="Todo limpiado")
    
    def load_example(self):
        """Carga el código de ejemplo"""
        self.code_area.delete(1.0, tk.END)
        self.code_area.insert(1.0, self.example_code)
        self.status_bar.config(text="Código de ejemplo cargado")


def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = CompilerIDE(root)
    root.mainloop()


if __name__ == "__main__":
    main()