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

# ============================================================================
# IMPRESIÓN Y ENTRADA DE DATOS
# Dhamar Quishpe (@dquishpe)
# ============================================================================
def p_impresion(p):
    '''impresion : PUTS argumentos_impresion
                 | PRINT argumentos_impresion'''
    p[0] = ('impresion', p[1], p[2])
    tokens_parseados.append(f"Instrucción de impresión: {p[1]}")

def p_argumentos_impresion(p):
    '''argumentos_impresion : argumentos_impresion COMA expresion
                            | expresion'''
    if len(p) == 4:
        if isinstance(p[1], list):
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1], p[3]]
    else:
        p[0] = [p[1]] if not isinstance(p[1], list) else p[1]

def p_entrada_datos(p):
    '''entrada_datos : GETS
                     | variable ASIGNACION GETS'''
    if len(p) == 2:
        p[0] = ('entrada', 'gets')
    else:
        p[0] = ('entrada_asignacion', p[1], p[3])
    tokens_parseados.append("Instrucción de entrada de datos: gets")

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

# ============================================================================
# HASH (ESTRUCTURA DE DATOS)
# Dhamar Quishpe (@dquishpe)
# ============================================================================
def p_hash(p):
    '''hash : LLAVE_IZQ pares LLAVE_DER
            | LLAVE_IZQ LLAVE_DER'''
    if len(p) == 4:
        p[0] = ('hash', p[2])
        tokens_parseados.append(f"Hash con {len(p[2])} par(es) clave-valor")
    else:
        p[0] = ('hash', [])
        tokens_parseados.append("Hash vacío")

def p_pares(p):
    '''pares : pares COMA par
             | par'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_par(p):
    '''par : VARIABLE_LOCAL DOS_PUNTOS expresion
           | STRING FLECHA expresion
           | expresion FLECHA expresion'''
    if p[2] == ':':
        p[0] = ('par_simbolo', p[1], p[3])
    else:
        p[0] = ('par', p[1], p[3])

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

# ============================================================================
# ESTRUCTURA DE CONTROL WHILE
# Dhamar Quishpe (@dquishpe)
# ============================================================================
def p_while_loop(p):
    '''while_loop : WHILE expresion sentencias END
                  | WHILE expresion DO sentencias END'''
    if len(p) == 5:
        p[0] = ('while', p[2], p[3])
    else:
        p[0] = ('while', p[2], p[4])
    tokens_parseados.append("Estructura WHILE")

# ============================================================================
# LLAMADAS A FUNCIONES
# Dhamar Quishpe (@dquishpe)
# ============================================================================
def p_llamada_funcion(p):
    '''expresion : VARIABLE_LOCAL PARENTESIS_IZQ argumentos PARENTESIS_DER
                 | VARIABLE_LOCAL PARENTESIS_IZQ PARENTESIS_DER
                 | CONSTANTE PUNTO VARIABLE_LOCAL PARENTESIS_IZQ argumentos PARENTESIS_DER
                 | CONSTANTE PUNTO VARIABLE_LOCAL PARENTESIS_IZQ PARENTESIS_DER'''
    if len(p) == 5:
        p[0] = ('llamada_funcion', p[1], p[3])
        tokens_parseados.append(f"Llamada a función: {p[1]} con {len(p[3])} argumento(s)")
    elif len(p) == 4:
        p[0] = ('llamada_funcion', p[1], [])
        tokens_parseados.append(f"Llamada a función: {p[1]} sin argumentos")
    elif len(p) == 7:
        nombre = f"{p[1]}.{p[3]}"
        p[0] = ('llamada_funcion', nombre, p[5])
        tokens_parseados.append(f"Llamada a función: {nombre} con {len(p[5])} argumento(s)")
    else:
        nombre = f"{p[1]}.{p[3]}"
        p[0] = ('llamada_funcion', nombre, [])
        tokens_parseados.append(f"Llamada a función: {nombre} sin argumentos")

# ============================================================================
# CREAR LOG DE ANÁLISIS SINTÁCTICO
# Dhamar Quishpe (@dquishpe)
# ============================================================================
def crear_log_sintactico(tokens_reconocidos, errores, usuario, archivo_entrada, resultado_parser):
    """
    Crea un archivo log del análisis sintáctico
    """
    fecha = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    
    carpeta_logs = os.path.join(os.path.dirname(__file__), "../logs")
    os.makedirs(carpeta_logs, exist_ok=True)
    
    nombre_log = os.path.join(carpeta_logs, f"sintactico-{usuario}-{fecha}.txt")
    
    with open(nombre_log, 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write("ANALIZADOR SINTÁCTICO PARA RUBY\n")
        f.write("="*100 + "\n\n")
        f.write(f"Usuario: {usuario}\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Archivo analizado: {archivo_entrada}\n")
        f.write("="*100 + "\n\n")
        
        if resultado_parser:
            f.write("[OK] ANÁLISIS SINTÁCTICO EXITOSO\n\n")
            f.write("ESTRUCTURA DEL PROGRAMA:\n")
            f.write("-"*100 + "\n")
            f.write(f"{resultado_parser}\n")
            f.write("-"*100 + "\n\n")
        
        if tokens_reconocidos:
            f.write("CONSTRUCCIONES SINTÁCTICAS RECONOCIDAS:\n")
            f.write("-"*100 + "\n")
            for i, token in enumerate(tokens_reconocidos, 1):
                f.write(f"{i}. {token}\n")
            f.write("-"*100 + "\n")
            f.write(f"Total de construcciones: {len(tokens_reconocidos)}\n\n")
        
        if errores:
            f.write("ERRORES SINTÁCTICOS ENCONTRADOS:\n")
            f.write("-"*100 + "\n")
            for i, error in enumerate(errores, 1):
                f.write(f"{i}. {error}\n")
            f.write("-"*100 + "\n")
            f.write(f"Total de errores: {len(errores)}\n\n")
        
        if not errores:
            f.write("\n[OK] ANÁLISIS COMPLETADO SIN ERRORES SINTÁCTICOS\n")
        else:
            f.write("\n[ERROR] ANÁLISIS COMPLETADO CON ERRORES SINTÁCTICOS\n")
        
        f.write("\n" + "="*100 + "\n")
    
    return nombre_log

# ============================================================================
# ANALIZAR ARCHIVO
# Dhamar Quishpe (@dquishpe)
# ============================================================================
def analizar_sintaxis(archivo_entrada, usuario_git):
    """
    Analiza sintácticamente un archivo Ruby y genera el log correspondiente
    """
    global errores_sintacticos, tokens_parseados
    errores_sintacticos = []
    tokens_parseados = []
    
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo '{archivo_entrada}'")
        return
    
    print("\n" + "="*100)
    print(f"{'ANALIZADOR SINTÁCTICO PARA RUBY':^100}")
    print("="*100)
    print(f"\n{'Usuario:':<20} {usuario_git}")
    print(f"{'Archivo analizado:':<20} {archivo_entrada}")
    print(f"{'Fecha:':<20} {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("\n" + "="*100)
    print("ANALIZANDO SINTAXIS...")
    print("-"*100)
    
    # Construir el parser
    parser = yacc.yacc()
    
    # Parsear el código
    resultado = parser.parse(data, tracking=True)
    
    print("-"*100)
    
    if errores_sintacticos:
        print("\n" + "="*100)
        print("ERRORES SINTÁCTICOS ENCONTRADOS:")
        print("-"*100)
        for i, error in enumerate(errores_sintacticos, 1):
            print(f"{i}. {error}")
        print("-"*100)
        print(f"\n[ERROR] ANÁLISIS COMPLETADO CON {len(errores_sintacticos)} ERROR(ES)")
    else:
        print(f"\n[OK] ANÁLISIS COMPLETADO SIN ERRORES")
        print(f"[OK] Se reconocieron {len(tokens_parseados)} construcciones sintácticas")
    
    print("="*100)
    
    # Crear log
    nombre_log = crear_log_sintactico(tokens_parseados, errores_sintacticos, usuario_git, archivo_entrada, resultado)
    print(f"\n[LOG] Archivo guardado en: {nombre_log}")
    print("="*100 + "\n")
    
    return resultado, errores_sintacticos