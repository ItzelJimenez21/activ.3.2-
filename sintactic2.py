import ply.yacc as yacc
from lex2 import tokens

# Variable global para almacenar los errores sintácticos
parser_errors = []

# Reglas de la gramática

# Regla para el bloque main con tipo de retorno
def p_main_block(p):
    '''statement : PR PR LPAREN RPAREN LLA statements RLA'''
    p[0] = ('main_block', p[2], 'correcta')

# Regla para múltiples statements
def p_statements_multiple(p):
    '''statements : statements statement'''
    pass

def p_statements_single(p):
    '''statements : statement'''
    pass

# Regla para la declaración de variables (con verificación de punto y coma y nombre de variable)
def p_declaration(p):
    '''statement : PR ID PUNTO_Y_COMA'''
    # Validar que solo la variable 'x' sea permitida
    if p[2] != 'x':  
        error_message = f"Error de sintaxis: Se esperaba la variable 'x', pero se encontró '{p[2]}'. Línea {p.lineno(2)}, posición {p.lexpos(2)}."
        parser_errors.append(error_message)

    # Validar que haya un punto y coma
    if p[3] != ';':
        error_message = f"Error de sintaxis: Falta el punto y coma ';' al final de la declaración. Línea {p.lineno(3)}, posición {p.lexpos(3)}."
        parser_errors.append(error_message)

# Capturar declaraciones incompletas (como falta de punto y coma)
def p_declaration_incomplete(p):
    '''statement : PR ID'''
    error_message = f"Error de sintaxis: Declaración incompleta, falta el punto y coma ';' al final. Línea {p.lineno(2)}, posición {p.lexpos(2)}."
    parser_errors.append(error_message)

# Manejar llaves de apertura y cierre
def p_brace_block(p):
    '''statement : LLA statements RLA'''
    p[0] = ('brace_block', 'correcta')

# Capturar error cuando falta la llave de cierre '}'
def p_missing_brace(p):
    '''statement : LLA statements
                 | statements RLA'''
    if len(p) == 3 and p[1] == '{':
        error_message = "Error de sintaxis: Falta una llave de cierre '}' para completar el bloque."
        parser_errors.append(error_message)
    elif len(p) == 3 and p[2] == '}':
        error_message = "Error de sintaxis: Falta una llave de apertura '{'."
        parser_errors.append(error_message)

# Capturar errores sintácticos en general
def p_error(p):
    if p:
        error_message = f"Error de sintaxis: Token inesperado '{p.value}' en la línea {p.lineno}, posición {p.lexpos}."
        parser_errors.append(error_message)
    else:
        error_message = "Error de sintaxis: Se encontró el final del archivo sin cerrar correctamente (falta '}' probablemente)."
        parser_errors.append(error_message)

# Construir el parser
parser = yacc.yacc()

def sintactico(text):
    global parser_errors
    parser_errors.clear()  # Limpiar errores anteriores
    try:
        result = parser.parse(text)
        return result
    except Exception as e:
        return str(e)