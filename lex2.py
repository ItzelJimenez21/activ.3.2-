import ply.lex as lex

# Definir los tokens
tokens = ['PR', 'ID', 'LPAREN', 'RPAREN', 'LLA', 'RLA', 'PUNTO_Y_COMA']

# Definir las palabras reservadas
reserved_words = {
    'for': 'PR',
    'For': 'PR',
    'Main': 'PR',
    'main': 'PR',
    'int': 'PR',
    'Int': 'PR'
}

# Sugerencias para palabras mal escritas
suggestions = {
    'mai': 'main',  # Sugerir 'main' si se escribe 'mai'
    'fo': 'for',  # Sugerir 'for' si se escribe 'fo'
    'In': 'int',  # Sugerir 'int' si se escribe 'In'
    'Ma': 'Main',   # Sugerir 'Main' si se escribe 'Ma'
    'in': 'int'
}

# Variable global para almacenar los errores léxicos
lexer_errors = []

# Expresión regular para palabras reservadas o identificadores
# Expresión regular para palabras reservadas o identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved_words:  # Si la palabra está en las palabras reservadas
        t.type = reserved_words[t.value]
    else:
        # Verificar si hay alguna sugerencia para palabras mal escritas
        suggestion = suggestions.get(t.value[:3], None)  # Buscar en las sugerencias
        if suggestion:
            # Capturar el error léxico con sugerencia
            error_message = f"Error léxico: '{t.value}' no es válido. ¿Quisiste decir '{suggestion}'? Línea {t.lineno}, posición {t.lexpos}."
            lexer_errors.append(error_message)
        else:
            # Si no hay sugerencia, tratarlo como un identificador común
            t.type = 'ID'
    return t

# Token para paréntesis de apertura '('
t_LPAREN = r'\('

# Token para paréntesis de cierre ')'
t_RPAREN = r'\)'

# Token para llave de apertura '{'
t_LLA = r'\{'

# Token para llave de cierre '}'
t_RLA = r'\}'

# Token para el punto y coma ';'
t_PUNTO_Y_COMA = r';'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejador de errores léxicos
def t_error(t):
    global lexer_errors
    
    # Ignorar espacios en blanco que no deberían ser tomados como errores
    if t.value[0].isspace():
        t.lexer.skip(1)
        return
    
    # Buscar sugerencia basada en los primeros tres caracteres de la palabra
    suggestion = suggestions.get(t.value[:3], None)
    
    if suggestion:
        error_message = f"Error léxico: '{t.value}' no es válido. ¿Quisiste decir '{suggestion}'? Línea {t.lineno}, posición {t.lexpos}."
    else:
        error_message = f"Carácter ilegal '{t.value[0]}' en línea {t.lineno}, posición {t.lexpos}."
    
    lexer_errors.append(error_message)
    t.lexer.skip(1)  # Saltar el token no válido para continuar el análisis

# Inicializar el lexer
lexer = lex.lex()

def lexico(text):
    global lexer_errors
    lexer_errors.clear()  # Limpiar los errores léxicos anteriores
    lexer.input(text)
    lexemes = []

    while True:
        tok = lexer.token()
        if not tok:
            break  # No más tokens
        
        nuevo_token = (tok.type, tok.value, tok.lineno, tok.lexpos)
        lexemes.append(nuevo_token)

    return lexemes