import ply.lex as lex
from datetime import datetime
import sys
import os

reserved = {
    # Jose Marin (@JoseM0lina)
    "if": "IF",
    "else": "ELSE",
    "elsif": "ELSIF",
    "while": "WHILE",
    "for": "FOR",
    "until": "UNTIL",
    "def": "DEF",
    "return": "RETURN",
    "end": "END",
    "class": "CLASS",
    "module": "MODULE",
    "true": "TRUE",
    "false": "FALSE",
    "nil": "NIL",
    "break": "BREAK",
    "next": "NEXT",
    "redo": "REDO",
    # Jose Marin (@JoseM0lina)
    # Angelo Zurita (@aszurita)
    'puts': 'PUTS',  
    'print': 'PRINT',
    'gets': 'GETS',
    'require': 'REQUIRE',
    'then': 'THEN',
    'do': 'DO',
    'in': 'IN',
    # Angelo Zurita (@aszurita)
}

# Lista de tokens
tokens = [
    # Tipos de datos
    'INTEGER',
    'FLOAT',
    'STRING',
    'SIMBOLO',

    # Variables y constantes
    'VARIABLE_LOCAL',
    'VARIABLE_GLOBAL',
    'VARIABLE_INSTANCIA',
    'VARIABLE_CLASE',
    'CONSTANTE',

    # Operadores aritméticos
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'MODULO',
    
    # Operadores de asignación
    'ASIGNACION',
    'SUMA_ASIG',
    'RESTA_ASIG',
    'MULT_ASIG',
    'DIV_ASIG',

    # Operadores de comparación
    'IGUAL',
    'DIFERENTE',
    'MAYOR',
    'MENOR',
    'MAYOR_IGUAL',
    'MENOR_IGUAL',
    # Operadores lógicos
    'AND',
    'OR',
    'NOT',

    # Delimitadores
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    'LLAVE_IZQ',
    'LLAVE_DER',
    'CORCHETE_IZQ',
    'CORCHETE_DER',
    'COMA',
    'PUNTO_COMA',
    'DOS_PUNTOS',
    'PUNTO',
    'FLECHA',
    
    # Comentarios
    'COMENTARIO_LINEA',
    'COMENTARIO_MULTILINEA',
] + list(reserved.values())

# ============================================
# Operadores aritméticos y de asignación Angelo Zurita (@aszurita)
# ============================================
t_SUMA_ASIG = r'\+='
t_RESTA_ASIG = r'-='
t_MULT_ASIG = r'\*='
t_DIV_ASIG = r'/='

# ============================================
# Operadores de asignación Angelo Zurita (@aszurita)
# ============================================
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_MODULO = r'%'

# ============================================
# Operadores de comparación Angelo Zurita (@aszurita)
# ============================================
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
t_IGUAL = r'=='
t_DIFERENTE = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_ASIGNACION = r'='

# ============================================
# Operadores lógicos Dhamar Quishpe (@dquishpe)
# ============================================
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

# ============================================
# Delimitadores Dhamar Quishpe (@dquishpe)
# ============================================
t_FLECHA = r'=>'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_COMA = r','
t_PUNTO_COMA = r';'
t_DOS_PUNTOS = r':'
t_PUNTO = r'\.'


# ============================================
# Ignorar espacios y tabs Angelo Zurita (@aszurita)
# ============================================
t_ignore = ' \t'

# ============================================
# Tipos de datos  Jose Marin (@JoseM0lina)
# ============================================
def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'("([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\')'
    # Remover las comillas
    t.value = t.value[1:-1]
    return t

def t_SIMBOLO(t):
    r':[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# ============================================
# Variables y constantes  Jose Marin (@JoseM0lina)
# ============================================

def t_VARIABLE_CLASE(t):
    r'@@[a-zA-Z_]\w*'
    return t

def t_VARIABLE_INSTANCIA(t):
    r'@[a-zA-Z_]\w*'
    return t

def t_VARIABLE_GLOBAL(t):
    r'\$[a-zA-Z_]\w*'
    return t

def t_CONSTANTE(t):
    r'[A-Z][a-zA-Z0-9_]*'
    return t

def t_VARIABLE_LOCAL(t):
    r'[a-z_][a-zA-Z0-9_]*'
    # Verificar si es palabra reservada
    t.type = reserved.get(t.value, 'VARIABLE_LOCAL')
    return t

# ============================================================================
# Comentarios Dhamar Quishpe (@dquishpe)
# ============================================================================

def t_COMENTARIO_MULTILINEA(t):
    r'=begin(.|\n)*?=end'
    t.lexer.lineno += t.value.count('\n')
    return t #Se puede usar pass si no se quiere retornar el token (usado para ignorar comentarios)

def t_COMENTARIO_LINEA(t):
    r'\#.*'
    return t


# ============================================
# Manejo de saltos de línea Angelo Zurita (@aszurita)
# ============================================
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ============================================
# Manejo de errores léxicos Angelo Zurita (@aszurita)
# ============================================
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


# ============================================
# Crear log Angelo Zurita (@aszurita)
# ============================================
def crear_log(tokens, errores, usuario, archivo_entrada):
    """
    Crea un archivo log
    """
    fecha = datetime.now().strftime("%d-%m-%Y-%Hh%M")

    carpeta_logs = os.path.join(os.path.dirname(__file__), "../logs")
    os.makedirs(carpeta_logs, exist_ok=True) 

    nombre_log = os.path.join(carpeta_logs, f"lexico-{usuario}-{fecha}.txt")
    
    with open(nombre_log, 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write("ANALIZADOR LÉXICO PARA RUBY\n")
        f.write("="*100 + "\n\n")
        f.write(f"Usuario: {usuario}\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Archivo analizado: {archivo_entrada}\n")
        f.write("="*100 + "\n\n")
        
        if tokens:
            f.write("TOKENS RECONOCIDOS:\n")
            f.write("-"*100 + "\n")
            f.write(f"{'Tipo':<25} {'Valor':<30} {'Línea':<10} {'Posición':<10}\n")
            f.write("-"*100 + "\n")
            for tok in tokens:
                tipo = tok.type
                valor = str(tok.value)
                linea = tok.lineno
                pos = tok.lexpos
                if len(valor) > 30 and tipo == 'COMENTARIO_MULTILINEA':
                    valor = valor.replace('\n', ' ')
                f.write(f"{tipo:<25} {valor:<30} {linea:<10} {pos:<10}\n")
            f.write("-"*100 + "\n")
            f.write(f"Total de tokens: {len(tokens)}\n\n")
        
        if errores:
            f.write("ERRORES LÉXICOS ENCONTRADOS:\n")
            f.write("-"*100 + "\n")
            for error in errores:
                f.write(f"{error}\n")
            f.write("-"*100 + "\n")
            f.write(f"Total de errores: {len(errores)}\n\n")
        
        if not errores:
            f.write("\n ANÁLISIS COMPLETADO SIN ERRORES\n")
        else:
            f.write("\n ANÁLISIS COMPLETADO CON ERRORES\n")
        
        f.write("\n" + "="*100 + "\n")
    
    return nombre_log

# ============================================
# Analizar archivo Dhamar Quishpe (@dquishpe)
# ============================================
def analizar_archivo(archivo_entrada, usuario_git):
    """
    Analiza un archivo Ruby y genera el log correspondiente
    """
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_entrada}'")
        return
    
    # Construir el lexer
    lexer = lex.lex()
    lexer.input(data)
    
    # Tokenizar
    tokens = []
    errores = []
    
    print("\n" + "="*100)
    print(f"{'ANALIZADOR LÉXICO PARA RUBY':^100}")
    print("="*100)
    print(f"\n{'Usuario:':<20} {usuario_git}")
    print(f"{'Archivo analizado:':<20} {archivo_entrada}")
    print(f"{'Fecha:':<20} {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("\n" + "="*100)
    print("TOKENS RECONOCIDOS:")
    print("-"*100)
    print(f"{'TIPO':<30} {'VALOR':<35} {'LÍNEA':<10} {'POSICIÓN':<10}")
    print("-"*100)
    
    while True:
        try:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(tok)
            tipo = tok.type
            valor = str(tok.value)
            # Textos largos
            if len(valor) > 32:
                valor = valor[:29] + "..."
            linea = tok.lineno
            pos = tok.lexpos
            print(f"{tipo:<30} {valor:<35} {linea:<10} {pos:<10}")
        except Exception as e:
            error_msg = f"Error en línea {lexer.lineno}: {str(e)}"
            errores.append(error_msg)
            print(f"\n{error_msg}\n")
    
    if errores:
        print("\n" + "="*100)
        print("ERRORES LÉXICOS ENCONTRADOS:")
        print("-"*100)
        for i, error in enumerate(errores, 1):
            print(f"{i}. {error}")
        print("-"*100)
        print("\n ANÁLISIS COMPLETADO CON ERRORES")
    else:
        print("\n ANÁLISIS COMPLETADO SIN ERRORES")
    
    print("="*100)
    
    # Crear log
    nombre_log = crear_log(tokens, errores, usuario_git, archivo_entrada)
    print(f"\n Log guardado en: {nombre_log}")
    print("="*100 + "\n")
    
    return tokens, errores

# ============================================
# Main Inicial  Jose Marin (@JoseM0lina)
# ============================================
if __name__ == '__main__':
    if len(sys.argv) > 2:
        archivo = sys.argv[1]
        usuario = sys.argv[2]
        analizar_archivo(archivo, usuario)
    else:
        print("Error al ejecutar el programa")