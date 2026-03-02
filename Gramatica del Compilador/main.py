"""
Utilizando tu analizador léxico y tu algoritmo para trabajar con las tablas lr. 
Carga e implementa la siguiente gramática.
https://github.com/TraductoresLenguajes2/Traductores/tree/master/Modulo4
"""

from parserLR import parse

codigo = "int x; $"
parse("compilador.lr", codigo)