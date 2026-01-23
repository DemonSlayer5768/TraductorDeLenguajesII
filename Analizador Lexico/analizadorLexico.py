from functions import Lexico, TipoSimbolo

x  = "'hola'"
x1 = "'hola29'"
x2 = "'h_o_l_a'"
x3 = '29.9'
x4 = '30'
x5 = 'true'
x6 = '$29.90'

entradas = [x, x1, x2, x3, x4, x5, x6]

for e in entradas:
    print(f"\nEntrada: {e}")
    lex = Lexico(e)

    while True:
        tipo = lex.sigSimbolo()
        if tipo == TipoSimbolo.FIN:
            break
        print(f"{lex.simbolo} -> {tipo}")