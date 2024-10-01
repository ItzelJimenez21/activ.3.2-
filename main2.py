from flask import Flask, request, render_template
from lex2 import lexico, lexer_errors
from sintactic2 import sintactico, parser_errors

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    tokens = None
    sintactico_result = None
    sintactico_errors = None
    lexico_error = None

    if request.method == 'POST':
        text = request.form['text']

        # Ejecutar el análisis léxico y recopilar errores
        try:
            tokens = lexico(text)
            if lexer_errors:
                lexico_error = "\n".join(lexer_errors)
        except Exception as e:
            lexico_error = f"Error léxico: {str(e)}"

        # Ejecutar el análisis sintáctico incluso si hay errores léxicos
        try:
            sintactico_result = sintactico(text)
            if parser_errors:
                sintactico_errors = "\n".join(parser_errors)
        except Exception as e:
            sintactico_errors = f"Error general: {str(e)}"

        return render_template('vista2.html', tokens=tokens, text=text, sintactico_result=sintactico_result, 
                               sintactico_errors=sintactico_errors, lexico_error=lexico_error)

    return render_template('vista2.html', tokens=None, text=None, sintactico_result=None, sintactico_errors=None, lexico_error=None)

if __name__ == '__main__':
    app.run(debug=True)