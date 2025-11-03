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
] + list(reserved.values())

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