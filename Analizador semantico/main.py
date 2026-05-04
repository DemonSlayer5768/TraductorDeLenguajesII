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
    """Analizador semántico"""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.variables: Dict[str, Variable] = {}
        self.functions: Dict[str, Function] = {}
        self.current_scope = "global"
        self.function_scopes: Dict[str, Dict[str, Variable]] = {}
    
    def analyze(self, tokens: List[Token]) -> Tuple[List[str], List[str]]:
        """Analiza el código tokenizado"""
        self.errors = []
        self.warnings = []
        self.variables = {}
        self.functions = {}
        
        try:
            self._first_pass(tokens)  # Recolectar declaraciones de funciones
            self._second_pass(tokens)  # Validación semántica
        except Exception as e:
            self.errors.append(f"Error durante el análisis: {str(e)}")
        
        return self.errors, self.warnings
    
    def _first_pass(self, tokens: List[Token]):
        """Primera pasada: recolectar declaraciones de funciones"""
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Buscar declaración de función: tipo nombre(parámetros)
            if token.type in (TokenType.INT, TokenType.FLOAT, TokenType.VOID):
                return_type = token.value
                
                if i + 1 < len(tokens) and tokens[i + 1].type == TokenType.ID:
                    func_name = tokens[i + 1].value
                    
                    if i + 2 < len(tokens) and tokens[i + 2].type == TokenType.LPAREN:
                        # Extraer parámetros
                        params = self._extract_parameters(tokens, i + 3)
                        
                        # Buscar la llave de apertura
                        j = i + 3
                        paren_count = 1
                        while j < len(tokens) and paren_count > 0:
                            if tokens[j].type == TokenType.LPAREN:
                                paren_count += 1
                            elif tokens[j].type == TokenType.RPAREN:
                                paren_count -= 1
                            j += 1
                        
                        if j < len(tokens) and tokens[j].type == TokenType.LBRACE:
                            self.functions[func_name] = Function(
                                name=func_name,
                                return_type=return_type,
                                params=params,
                                defined=True
                            )
            i += 1
    
    def _second_pass(self, tokens: List[Token]):
        """Segunda pasada: validación semántica"""
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            # Declaración de variable: tipo nombre;
            if token.type in (TokenType.INT, TokenType.FLOAT):
                var_type = token.value
                
                if i + 1 < len(tokens) and tokens[i + 1].type == TokenType.ID:
                    var_name = tokens[i + 1].value
                    
                    if var_name in self.variables and self.variables[var_name].scope == self.current_scope:
                        self.errors.append(
                            f"Línea {token.line}: Variable '{var_name}' ya fue declarada"
                        )
                    else:
                        self.variables[var_name] = Variable(
                            name=var_name,
                            type=var_type,
                            scope=self.current_scope
                        )
                    i += 2
                    continue
            
            # Asignación: variable = expresión;
            if token.type == TokenType.ID and i + 1 < len(tokens):
                var_name = token.value
                
                if tokens[i + 1].type == TokenType.ASSIGN:
                    if var_name not in self.variables:
                        self.errors.append(
                            f"Línea {token.line}: Variable '{var_name}' no ha sido declarada"
                        )
                    else:
                        var_type = self.variables[var_name].type
                        # Validar expresión
                        expr_type = self._analyze_expression(tokens, i + 2)
                        
                        if expr_type and not self._is_compatible(var_type, expr_type):
                            self.errors.append(
                                f"Línea {token.line}: Incompatibilidad de tipos. "
                                f"Se intenta asignar '{expr_type}' a variable '{var_type}'"
                            )
                    i += 1
                    continue
            
            # Llamada a función
            if token.type == TokenType.ID and i + 1 < len(tokens) and tokens[i + 1].type == TokenType.LPAREN:
                func_name = token.value
                
                if func_name not in self.functions:
                    self.errors.append(
                        f"Línea {token.line}: Función '{func_name}' no ha sido definida"
                    )
                else:
                    # Validar argumentos
                    args = self._extract_call_arguments(tokens, i + 2)
                    expected_params = self.functions[func_name].params
                    
                    if len(args) != len(expected_params):
                        self.errors.append(
                            f"Línea {token.line}: Función '{func_name}' espera "
                            f"{len(expected_params)} argumentos, se proporcionaron {len(args)}"
                        )
                    else:
                        for arg_type, (param_name, expected_type) in zip(args, expected_params):
                            if arg_type and not self._is_compatible(expected_type, arg_type):
                                self.errors.append(
                                    f"Línea {token.line}: Argumento incompatible para parámetro '{param_name}'. "
                                    f"Se esperaba '{expected_type}', se obtuvo '{arg_type}'"
                                )
            
            i += 1
    
    def _extract_parameters(self, tokens: List[Token], start: int) -> List[Tuple[str, str]]:
        """Extrae parámetros de función"""
        params = []
        i = start
        
        while i < len(tokens) and tokens[i].type != TokenType.RPAREN:
            if tokens[i].type in (TokenType.INT, TokenType.FLOAT):
                param_type = tokens[i].value
                
                if i + 1 < len(tokens) and tokens[i + 1].type == TokenType.ID:
                    param_name = tokens[i + 1].value
                    params.append((param_name, param_type))
                    i += 2
                    
                    if i < len(tokens) and tokens[i].type == TokenType.COMMA:
                        i += 1
                else:
                    i += 1
            else:
                i += 1
        
        return params
    
    def _extract_call_arguments(self, tokens: List[Token], start: int) -> List[str]:
        """Extrae tipos de argumentos en llamada a función"""
        args = []
        i = start
        paren_count = 1
        arg_start = i
        
        while i < len(tokens) and paren_count > 0:
            if tokens[i].type == TokenType.LPAREN:
                paren_count += 1
            elif tokens[i].type == TokenType.RPAREN:
                paren_count -= 1
                if paren_count == 0:
                    # Procesar último argumento
                    if i > arg_start:
                        arg_type = self._infer_type(tokens[arg_start:i])
                        args.append(arg_type)
            elif tokens[i].type == TokenType.COMMA and paren_count == 1:
                # Procesar argumento
                arg_type = self._infer_type(tokens[arg_start:i])
                args.append(arg_type)
                arg_start = i + 1
            
            i += 1
        
        return args
    
    def _analyze_expression(self, tokens: List[Token], start: int) -> Optional[str]:
        """Analiza una expresión y retorna su tipo"""
        i = start
        expr_tokens = []
        
        while i < len(tokens) and tokens[i].type != TokenType.SEMICOLON:
            expr_tokens.append(tokens[i])
            i += 1
        
        return self._infer_type(expr_tokens)
    
    def _infer_type(self, expr_tokens: List[Token]) -> Optional[str]:
        """Infiere el tipo de una expresión"""
        if not expr_tokens:
            return None
        
        # Limpiar tokens vacíos
        expr_tokens = [t for t in expr_tokens if t.type != TokenType.SEMICOLON]
        
        if len(expr_tokens) == 1:
            token = expr_tokens[0]
            if token.type == TokenType.NUMBER:
                return "float" if '.' in token.value else "int"
            elif token.type == TokenType.ID:
                if token.value in self.variables:
                    return self.variables[token.value].type
            return None
        
        # Expresión con operadores
        result_type = None
        i = 0
        
        while i < len(expr_tokens):
            token = expr_tokens[i]
            
            if token.type == TokenType.NUMBER:
                current_type = "float" if '.' in token.value else "int"
                if result_type is None:
                    result_type = current_type
                elif not self._is_compatible(result_type, current_type):
                    result_type = "float"  # Promover a float
            elif token.type == TokenType.ID:
                if token.value in self.variables:
                    current_type = self.variables[token.value].type
                    if result_type is None:
                        result_type = current_type
                    elif not self._is_compatible(result_type, current_type):
                        result_type = "float"  # Promover a float
            elif token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.MULT, TokenType.DIV):
                # Operador
                pass
            
            i += 1
        
        return result_type
    
    def _is_compatible(self, target_type: str, source_type: str) -> bool:
        """Verifica compatibilidad de tipos"""
        if target_type == source_type:
            return True
        # Se permite asignar int a float, pero no float a int
        if target_type == "float" and source_type == "int":
            return True
        return False


class SemanticAnalyzerGUI:
    """Interfaz gráfica del analizador semántico"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Semántico de C")
        self.root.geometry("1000x700")
        
        # Configurar estilos
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame superior con botones
        top_frame = ttk.Frame(root)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(top_frame, text="Analizar", command=self.analyze).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Limpiar", command=self.clear).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Ejemplo 1", command=self.load_example1).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Ejemplo 2", command=self.load_example2).pack(side=tk.LEFT, padx=5)
        
        # Frame principal con dos columnas
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Columna izquierda - Código fuente
        left_frame = ttk.LabelFrame(main_frame, text="Código Fuente", padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.code_text = scrolledtext.ScrolledText(left_frame, height=25, width=40, 
                                                    font=("Courier", 10))
        self.code_text.pack(fill=tk.BOTH, expand=True)
        
        # Columna derecha - Resultados
        right_frame = ttk.LabelFrame(main_frame, text="Resultados del Análisis", padding=5)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Tab para errores y advertencias
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab de errores
        error_frame = ttk.Frame(self.notebook)
        self.notebook.add(error_frame, text="Errores")
        
        self.error_text = scrolledtext.ScrolledText(error_frame, height=12, width=40, 
                                                    font=("Courier", 9), bg="#ffe6e6")
        self.error_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab de advertencias
        warning_frame = ttk.Frame(self.notebook)
        self.notebook.add(warning_frame, text="Advertencias")
        
        self.warning_text = scrolledtext.ScrolledText(warning_frame, height=12, width=40, 
                                                      font=("Courier", 9), bg="#fffacd")
        self.warning_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab de resumen
        summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(summary_frame, text="Resumen")
        
        self.summary_text = scrolledtext.ScrolledText(summary_frame, height=12, width=40, 
                                                      font=("Courier", 9), bg="#f0f0f0")
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame inferior - Información
        info_frame = ttk.Frame(root)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_label = ttk.Label(info_frame, text="Listo", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X)
    
    def load_example1(self):
        """Carga el primer ejemplo"""
        code = """int main(){
float a;
int b;
int c;
c = a+b;
c = suma(8,9);
}"""
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", code)
    
    def load_example2(self):
        """Carga el segundo ejemplo"""
        code = """int a;
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
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", code)
    
    def analyze(self):
        """Realiza el análisis semántico"""
        code = self.code_text.get("1.0", tk.END)
        
        if not code.strip():
            messagebox.showwarning("Advertencia", "Por favor ingrese código para analizar")
            return
        
        # Análisis léxico
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Análisis semántico
        analyzer = SemanticAnalyzer()
        errors, warnings = analyzer.analyze(tokens)
        
        # Mostrar resultados
        self.error_text.delete("1.0", tk.END)
        self.warning_text.delete("1.0", tk.END)
        self.summary_text.delete("1.0", tk.END)
        
        if errors:
            self.error_text.insert("1.0", "\n".join(errors))
        else:
            self.error_text.insert("1.0", "✓ No se encontraron errores semánticos")
        
        if warnings:
            self.warning_text.insert("1.0", "\n".join(warnings))
        else:
            self.warning_text.insert("1.0", "✓ No se encontraron advertencias")
        
        # Resumen
        summary = f"""RESUMEN DEL ANÁLISIS
════════════════════════════════════

Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ERRORES: {len(errors)}
ADVERTENCIAS: {len(warnings)}

SÍMBOLOS DETECTADOS:
────────────────────

Variables declaradas:
"""
        for var_name, var in analyzer.variables.items():
            summary += f"  • {var.type} {var.name}\n"
        
        summary += "\nFunciones detectadas:\n"
        for func_name, func in analyzer.functions.items():
            params_str = ", ".join(f"{ptype} {pname}" for pname, ptype in func.params)
            summary += f"  • {func.return_type} {func.name}({params_str})\n"
        
        self.summary_text.insert("1.0", summary)
        
        # Actualizar estado
        if errors:
            self.status_label.config(text=f"❌ Análisis completado: {len(errors)} errores encontrados")
        else:
            self.status_label.config(text="✓ Análisis completado exitosamente")
    
    def clear(self):
        """Limpia todos los campos"""
        self.code_text.delete("1.0", tk.END)
        self.error_text.delete("1.0", tk.END)
        self.warning_text.delete("1.0", tk.END)
        self.summary_text.delete("1.0", tk.END)
        self.status_label.config(text="Listo")


if __name__ == "__main__":
    root = tk.Tk()
    gui = SemanticAnalyzerGUI(root)
    root.mainloop()
