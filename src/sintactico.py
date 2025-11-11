import ply.yacc as yacc
from lexico import tokens
from datetime import datetime
import sys
import os

# ============================================
# PRECEDENCIA Y ASOCIATIVIDAD DE OPERADORES
# Angelo Zurita (@aszurita)
# ============================================
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'IGUAL', 'DIFERENTE', 'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION', 'MODULO'),
    ('right', 'UMINUS'),  # Menos unario
)

# ============================================
# VARIABLES GLOBALES PARA MANEJO DE ERRORES
# ============================================
errores_sintacticos = []
tokens_parseados = []

# ============================================
# REGLA INICIAL - PROGRAMA
# Angelo Zurita (@aszurita)
# ============================================
def p_programa(p):
    '''programa : sentencias'''
    p[0] = ('programa', p[1])
    tokens_parseados.append(f"Programa reconocido con {len(p[1]) if isinstance(p[1], list) else 1} sentencia(s)")

def p_sentencias(p):
    '''sentencias : sentencias sentencia
                | sentencia'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_sentencia(p):
    '''sentencia : asignacion
                | impresion PUNTO_COMA
                | impresion
                | entrada_datos
                | estructura_control
                | definicion_funcion
                | definicion_clase
                | definicion_modulo
                | estructura_datos
                | expresion
                | COMENTARIO_LINEA
                | COMENTARIO_MULTILINEA'''
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = p[1]

# ============================================
# ASIGNACIONES
# Angelo Zurita (@aszurita)
# ============================================
def p_asignacion(p):
    '''asignacion : variable ASIGNACION expresion
                | variable SUMA_ASIG expresion
                | variable RESTA_ASIG expresion
                | variable MULT_ASIG expresion
                | variable DIV_ASIG expresion'''
    p[0] = ('asignacion', p[1], p[2], p[3])
    tokens_parseados.append(f"Asignación: {p[1]} {p[2]} [expresión]")

def p_variable(p):
    '''variable : VARIABLE_LOCAL
                | VARIABLE_GLOBAL
                | VARIABLE_INSTANCIA
                | VARIABLE_CLASE
                | CONSTANTE'''
    p[0] = ('variable', p[1])

# ============================================
# EXPRESIONES ARITMÉTICAS
# Angelo Zurita (@aszurita)
# ============================================
def p_expresion_binaria(p):
    '''expresion : expresion SUMA expresion
                | expresion RESTA expresion
                | expresion MULTIPLICACION expresion
                | expresion DIVISION expresion
                | expresion MODULO expresion'''
    p[0] = ('operacion_binaria', p[2], p[1], p[3])
    tokens_parseados.append(f"Operación aritmética: {p[2]}")

def p_expresion_comparacion(p):
    '''expresion : expresion IGUAL expresion
                | expresion DIFERENTE expresion
                | expresion MAYOR expresion
                | expresion MENOR expresion
                | expresion MAYOR_IGUAL expresion
                | expresion MENOR_IGUAL expresion'''
    p[0] = ('comparacion', p[2], p[1], p[3])
    tokens_parseados.append(f"Comparación: {p[2]}")

def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                | expresion OR expresion'''
    p[0] = ('operacion_logica', p[2], p[1], p[3])
    tokens_parseados.append(f"Operación lógica: {p[2]}")

def p_expresion_not(p):
    '''expresion : NOT expresion'''
    p[0] = ('not', p[2])
    tokens_parseados.append("Operación lógica: NOT")

def p_expresion_uminus(p):
    '''expresion : RESTA expresion %prec UMINUS'''
    p[0] = ('uminus', p[2])

def p_expresion_parentesis(p):
    '''expresion : PARENTESIS_IZQ expresion PARENTESIS_DER'''
    p[0] = ('parentesis', p[2])

def p_expresion_valor(p):
    '''expresion : INTEGER
                | FLOAT
                | STRING
                | SIMBOLO
                | TRUE
                | FALSE
                | NIL
                | variable
                | arreglo
                | hash'''
    p[0] = ('valor', p[1])

# ============================================
# ARREGLOS (ESTRUCTURA DE DATOS)
# Angelo Zurita (@aszurita)
# ============================================
def p_estructura_datos(p):
    '''estructura_datos : arreglo
                        | hash'''
    p[0] = p[1]

def p_arreglo(p):
    '''arreglo : CORCHETE_IZQ elementos CORCHETE_DER
            | CORCHETE_IZQ CORCHETE_DER'''
    if len(p) == 4:
        p[0] = ('arreglo', p[2])
        tokens_parseados.append(f"Arreglo con {len(p[2])} elemento(s)")
    else:
        p[0] = ('arreglo', [])
        tokens_parseados.append("Arreglo vacío")

def p_elementos(p):
    '''elementos : elementos COMA expresion
                | expresion'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# ============================================
# ESTRUCTURA DE CONTROL IF
# Angelo Zurita (@aszurita)
# ============================================
def p_estructura_control(p):
    '''estructura_control : if_statement
                          | while_loop
                          | for_loop
                          | until_loop'''
    p[0] = p[1]

def p_if_statement(p):
    '''if_statement : IF expresion sentencias END
                    | IF expresion THEN sentencias END
                    | IF expresion sentencias ELSE sentencias END
                    | IF expresion THEN sentencias ELSE sentencias END
                    | IF expresion sentencias elsif_chain END
                    | IF expresion THEN sentencias elsif_chain END
                    | IF expresion sentencias elsif_chain ELSE sentencias END
                    | IF expresion THEN sentencias elsif_chain ELSE sentencias END'''
    if len(p) == 5:
        p[0] = ('if', p[2], p[3])
    elif len(p) == 6:
        # IF expresion THEN sentencias END
        # IF expresion sentencias elsif_chain END
        if p[3] == 'then':
            p[0] = ('if', p[2], p[4])
        else:
            p[0] = ('if_elsif', p[2], p[3], p[4])
    elif len(p) == 7:
        # IF expresion sentencias ELSE sentencias END
        # IF expresion THEN sentencias elsif_chain END
        if p[3] == 'then':
            p[0] = ('if_elsif', p[2], p[4], p[5])
        else:
            p[0] = ('if_else', p[2], p[3], p[5])
    elif len(p) == 8:
        # IF expresion sentencias elsif_chain ELSE sentencias END
        # IF expresion THEN sentencias ELSE sentencias END
        if p[3] == 'then':
            p[0] = ('if_else', p[2], p[4], p[6])
        else:
            p[0] = ('if_elsif_else', p[2], p[3], p[4], p[6])
    else:
        # IF expresion THEN sentencias elsif_chain ELSE sentencias END
        p[0] = ('if_elsif_else', p[2], p[4], p[5], p[7])
    tokens_parseados.append("Estructura IF completa")


def p_elsif_chain(p):
    '''elsif_chain : elsif_chain elsif_block
                   | elsif_block'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_elsif_block(p):
    '''elsif_block : ELSIF expresion sentencias
                   | ELSIF expresion THEN sentencias'''
    if len(p) == 4:
        p[0] = ('elsif', p[2], p[3])
    else:
        p[0] = ('elsif', p[2], p[4])
