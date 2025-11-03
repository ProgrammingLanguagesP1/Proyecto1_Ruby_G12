import ply.lex as lex

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
# Tipos de datos  Jose Marin (@JoseM0lina)
# ============================================
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'("([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\')'
    # Remover las comillas
    t.value = t.value[1:-1]
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
    r'[A-Z][A-Z0-9_]*'
    return t

def t_VARIABLE_LOCAL(t):
    r'[a-z_][a-zA-Z0-9_]*'
    # Verificar si es palabra reservada
    t.type = reserved.get(t.value, 'VARIABLE_LOCAL')
    return t


# ============================================
# Crear log Angelo Zurita (@aszurita)
# ============================================
def crear_log(tokens, errores, usuario, archivo_entrada):
    """
    Crea un archivo log
    """
    fecha = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    nombre_log = f"logs/lexico-{usuario}-{fecha}.txt"
    
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
            f.write("\n✓ ANÁLISIS COMPLETADO SIN ERRORES\n")
        else:
            f.write("\n✗ ANÁLISIS COMPLETADO CON ERRORES\n")
        
        f.write("\n" + "="*100 + "\n")
    
    return nombre_log