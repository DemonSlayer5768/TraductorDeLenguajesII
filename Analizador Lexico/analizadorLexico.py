import functions

x  = "'hola'"
x1 = "'hola29'"
x2 = "'h_o_l_a'"
x3 = '29.9'
x4 = '30'
x5 = 'true'

for var in [x, x1, x2, x3, x4, x5]:
    print(functions.analizador_lexico(var))
