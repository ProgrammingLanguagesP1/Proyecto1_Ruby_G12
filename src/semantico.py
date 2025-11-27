import sys
import os
from datetime import datetime
from sintactico import analizar_sintaxis
from lexico import analizar_archivo

# ============================================
# TABLA DE SÍMBOLOS
# Dhamar Quishpe (@dquishpe)
# ============================================
tabla_simbolos = {
    "variables": {},
    "constantes": {},
    "funciones": {},
    "tipos": {
        "str-funciones": ["length", "upcase", "downcase", "reverse", "to_i", "to_f"],
        "int-funciones": ["to_s", "to_f"],
        "float-funciones": ["to_s", "to_i"],
        "array-funciones": ["length", "push", "pop", "first", "last"],
        "hash-funciones": ["keys", "values", "length"]
    }
}

errores_semanticos = []
warnings_semanticos = []
contexto_actual = 'global'
en_loop = False
en_funcion = False

def reiniciar_analisis():
    """Reinicia las estructuras para un nuevo análisis"""
    global tabla_simbolos, errores_semanticos, warnings_semanticos
    global contexto_actual, en_loop, en_funcion
    
    tabla_simbolos = {
        "variables": {},
        "constantes": {},
        "funciones": {},
        "tipos": {
            "str-funciones": ["length", "upcase", "downcase", "reverse", "to_i", "to_f"],
            "int-funciones": ["to_s", "to_f"],
            "float-funciones": ["to_s", "to_i"],
            "array-funciones": ["length", "push", "pop", "first", "last"],
            "hash-funciones": ["keys", "values", "length"]
        }
    }
    errores_semanticos = []
    warnings_semanticos = []
    contexto_actual = 'global'
    en_loop = False
    en_funcion = False

# ============================================
# REGLAS SEMÁNTICAS - IDENTIFICADORES
# Dhamar Quishpe (@dquishpe)
# ============================================

def verificar_variable_declarada(nombre, linea=0):
    """
    Regla 1: Variable no declarada
    Verifica que la variable haya sido declarada antes de su uso
    """
    # Variables de instancia (@variable) no requieren declaración previa en Ruby
    if nombre.startswith('@'):
        return True

    # Métodos integrados de Ruby que no son variables
    metodos_integrados = ['length', 'size', 'to_i', 'to_f', 'to_s', 'upcase', 'downcase',
                         'reverse', 'push', 'pop', 'first', 'last', 'keys', 'values',
                         'each', 'map', 'select', 'reject', 'sort', 'join', 'split',
                         'new', 'puts', 'print', 'gets', 'chomp', 'strip']
    if nombre in metodos_integrados:
        return True

    # Palabras clave y operadores lógicos de Ruby
    palabras_clave = ['and', 'or', 'not', 'if', 'elsif', 'else', 'end', 'while',
                     'until', 'for', 'in', 'do', 'break', 'next', 'return', 'def',
                     'class', 'module', 'true', 'false', 'nil', 'self', 'super']
    if nombre in palabras_clave:
        return True

    if nombre not in tabla_simbolos["variables"] and nombre not in tabla_simbolos["constantes"]:
        error = f"Error semántico en línea {linea}: Variable '{nombre}' no declarada antes de su uso"
        if error not in errores_semanticos:
            errores_semanticos.append(error)
        return False
    return True

def verificar_constante_modificada(nombre, linea=0):
    """
    Regla 2: Constante modificada
    Asegura que las constantes no puedan ser reasignadas
    """
    if nombre in tabla_simbolos["constantes"]:
        # Solo es error si la línea es diferente a la línea de declaración original
        linea_declaracion = tabla_simbolos['constantes'][nombre]['linea']
        if linea != linea_declaracion:
            error = f"Error semántico en línea {linea}: Constante '{nombre}' no puede ser modificada (ya fue declarada en línea {linea_declaracion})"
            if error not in errores_semanticos:
                errores_semanticos.append(error)
            return False
    return True

# ============================================
# REGLAS SEMÁNTICAS - ASIGNACIÓN DE TIPO
# Angelo Zurita (@aszurita)
# ============================================

def verificar_asignacion_incompatible(nombre, nuevo_tipo, linea=0):
    """
    Regla 3: Asignación incompatible
    Comprueba la coherencia del tipo de dato
    """
    if nombre in tabla_simbolos["variables"]:
        tipo_anterior = tabla_simbolos["variables"][nombre]["tipo"]
        if tipo_anterior != nuevo_tipo and tipo_anterior != 'any' and nuevo_tipo != 'any':
            warning = f"Advertencia semántica en línea {linea}: Variable '{nombre}' cambia de tipo '{tipo_anterior}' a '{nuevo_tipo}'"
            warnings_semanticos.append(warning)
    return True

def verificar_asignacion_palabra_reservada(nombre, linea=0):
    """
    Regla 4: Asignación a palabra reservada
    Impide la asignación a valores literales o palabras reservadas
    """
    palabras_reservadas = ['true', 'false', 'nil', 'if', 'else', 'elsif', 'while',
                           'for', 'until', 'def', 'class', 'module', 'end', 'return',
                           'break', 'next', 'redo', 'puts', 'print', 'gets']

    if nombre.lower() in palabras_reservadas:
        error = f"Error semántico en línea {linea}: No se puede asignar valor a palabra reservada '{nombre}'"
        if error not in errores_semanticos:
            errores_semanticos.append(error)
        return False
    return True

# ============================================
# REGLAS SEMÁNTICAS - OPERACIONES PERMITIDAS
# José Marin (@JoseM0lina)
# ============================================

def verificar_operador_incompatible(operador, tipo_izq, tipo_der, linea=0):
    """
    Regla 5: Operador incompatible
    Verifica que los operadores sean compatibles con los tipos de datos
    """
    operaciones_validas = {
        '+': [('integer', 'integer'), ('float', 'float'), ('integer', 'float'), 
              ('float', 'integer'), ('string', 'string')],
        '-': [('integer', 'integer'), ('float', 'float'), ('integer', 'float'), ('float', 'integer')],
        '*': [('integer', 'integer'), ('float', 'float'), ('integer', 'float'), 
              ('float', 'integer'), ('string', 'integer')],
        '/': [('integer', 'integer'), ('float', 'float'), ('integer', 'float'), ('float', 'integer')],
        '%': [('integer', 'integer')]
    }
    
    if operador in operaciones_validas:
        combinaciones = operaciones_validas[operador]
        if (tipo_izq, tipo_der) not in combinaciones:
            error = f"Error semántico en línea {linea}: Operador '{operador}' incompatible entre tipos '{tipo_izq}' y '{tipo_der}'"
            errores_semanticos.append(error)
            return False
    return True

def verificar_division_por_cero(divisor, linea=0):
    """
    Regla 6: División por cero
    Detecta operaciones que produzcan división entre cero
    """
    if divisor == 0:
        error = f"Error semántico en línea {linea}: División por cero detectada"
        errores_semanticos.append(error)
        return False
    return True

# ============================================
# REGLAS SEMÁNTICAS - ESTRUCTURAS DE CONTROL
# Dhamar Quishpe (@dquishpe)
# ============================================

def verificar_break_en_loop(linea=0):
    """
    Regla 7: Uso incorrecto de break
    Asegura que break o next solo se utilicen dentro de bucles
    """
    global en_loop
    if not en_loop:
        error = f"Error semántico en línea {linea}: 'break' usado fuera de un bucle"
        errores_semanticos.append(error)
        return False
    return True

def verificar_condicion_booleana(tipo_condicion, linea=0):
    """
    Regla 8: Condición no booleana
    Verifica que las expresiones condicionales sean evaluables a booleano
    """
    if tipo_condicion in ['string', 'array', 'hash']:
        warning = f"Advertencia semántica en línea {linea}: Condición de tipo '{tipo_condicion}' podría no ser intencional"
        warnings_semanticos.append(warning)
    return True

# ============================================
# REGLAS SEMÁNTICAS - CONVERSIÓN
# Angelo Zurita (@aszurita)
# ============================================

def verificar_conversion_implicita(tipo_izq, tipo_der, operador, linea=0):
    """
    Regla 9: Conversión implícita inválida
    Requiere conversión explícita entre tipos incompatibles
    """
    if tipo_izq == 'string' and tipo_der in ['integer', 'float'] and operador in ['+', '-', '*', '/']:
        error = f"Error semántico en línea {linea}: Conversión implícita inválida entre '{tipo_izq}' y '{tipo_der}'. Use conversión explícita"
        errores_semanticos.append(error)
        return False
    if tipo_der == 'string' and tipo_izq in ['integer', 'float'] and operador in ['-', '*', '/']:
        error = f"Error semántico en línea {linea}: Conversión implícita inválida entre '{tipo_izq}' y '{tipo_der}'. Use conversión explícita"
        errores_semanticos.append(error)
        return False
    return True

def verificar_conversion_perdida_datos(tipo_origen, tipo_destino, linea=0):
    """
    Regla 10: Conversión con pérdida de datos
    Advierte sobre posibles pérdidas de precisión
    """
    if tipo_origen == 'float' and tipo_destino == 'integer':
        warning = f"Advertencia semántica en línea {linea}: Conversión de '{tipo_origen}' a '{tipo_destino}' puede causar pérdida de precisión"
        warnings_semanticos.append(warning)
    return True

# ============================================
# REGLAS SEMÁNTICAS - RETORNO DE FUNCIONES
# José Marin (@JoseM0lina)
# ============================================

def verificar_retorno_valido(tipo_retorno, linea=0):
    """
    Regla 11: Retorno válido
    Verifica que la función devuelva un valor coherente
    """
    global en_funcion
    if not en_funcion:
        error = f"Error semántico en línea {linea}: 'return' usado fuera de una función"
        errores_semanticos.append(error)
        return False
    return True

def verificar_retorno_incompatible(nombre_funcion, tipo_retorno, linea=0):
    """
    Regla 12: Retorno incompatible
    Comprueba que el valor retornado coincida con el tipo de operación
    """
    if tipo_retorno == 'string' and nombre_funcion in ['suma', 'resta', 'multiplicacion', 'division']:
        warning = f"Advertencia semántica en línea {linea}: Función '{nombre_funcion}' retorna '{tipo_retorno}' cuando se esperaría un valor numérico"
        warnings_semanticos.append(warning)
    return True

# ============================================
# FUNCIONES AUXILIARES
# José Marin (@JoseM0lina)
# ============================================

def extraer_linea(nodo):
    """
    Extrae el número de línea de un nodo del árbol sintáctico.
    El número de línea siempre está al final de la tupla.
    """
    if not isinstance(nodo, tuple):
        return 1
    
    # Buscar el último elemento que sea un entero
    for i in range(len(nodo) - 1, -1, -1):
        if isinstance(nodo[i], int) and nodo[i] > 0:
            return nodo[i]
    
    return 1

def extraer_linea_expresion(expresion):
    """
    Extrae el número de línea de una expresión que puede estar anidada
    """
    if isinstance(expresion, tuple):
        return extraer_linea(expresion)
    elif isinstance(expresion, list) and len(expresion) > 0:
        return extraer_linea_expresion(expresion[0])
    return 1

# ============================================
# FUNCIONES AUXILIARES
# Angelo Zurita (@aszurita)
# ============================================

def obtener_tipo(valor):
    """Obtiene el tipo de un valor del árbol sintáctico"""
    if isinstance(valor, tuple):
        if valor[0] == 'valor':
            return obtener_tipo(valor[1])
        elif valor[0] == 'variable':
            # Puede ser ('variable', nombre) o ('variable', nombre, lineno)
            nombre = valor[1]

            # Variables de instancia siempre retornan 'any'
            if nombre.startswith('@'):
                if nombre in tabla_simbolos["variables"]:
                    return tabla_simbolos["variables"][nombre]["tipo"]
                return 'any'

            # Métodos integrados retornan 'any'
            metodos_integrados = ['length', 'size', 'to_i', 'to_f', 'to_s']
            if nombre in metodos_integrados:
                return 'any'

            if nombre in tabla_simbolos["variables"]:
                return tabla_simbolos["variables"][nombre]["tipo"]
            if nombre in tabla_simbolos["constantes"]:
                return tabla_simbolos["constantes"][nombre]["tipo"]
            return 'any'
        elif valor[0] == 'operacion_binaria':
            return inferir_tipo_operacion(valor[1], valor[2], valor[3])
        elif valor[0] == 'comparacion':
            return 'boolean'
        elif valor[0] == 'operacion_logica':
            return 'boolean'
        elif valor[0] == 'arreglo':
            return 'array'
        elif valor[0] == 'hash':
            return 'hash'
    elif isinstance(valor, int):
        return 'integer'
    elif isinstance(valor, float):
        return 'float'
    elif isinstance(valor, str):
        if valor in ['true', 'false']:
            return 'boolean'
        elif valor == 'nil':
            return 'nil'
        return 'string'
    return 'any'

def inferir_tipo_operacion(operador, izq, der):
    """Infiere el tipo resultado de una operación"""
    tipo_izq = obtener_tipo(izq)
    tipo_der = obtener_tipo(der)
    
    if operador in ['+', '-', '*', '/', '%']:
        if tipo_izq == 'float' or tipo_der == 'float':
            return 'float'
        elif tipo_izq == 'integer' and tipo_der == 'integer':
            return 'integer'
        elif tipo_izq == 'string' and tipo_der == 'string' and operador == '+':
            return 'string'
    return 'any'

# ============================================
# FUNCIONES AUXILIARES
# Angelo Zurita (@aszurita)
# ============================================

def analizar_nodo(nodo, linea=1):
    """
    Recorre el árbol sintáctico generado por sintactico.py
    y aplica las reglas semánticas
    """
    global en_loop, en_funcion, contexto_actual
    
    if not isinstance(nodo, tuple):
        return
    
    tipo_nodo = nodo[0]

    linea_nodo = extraer_linea(nodo)
    for elemento in nodo:
        if isinstance(elemento, int) and elemento > 0 and elemento < 100000:
            linea_nodo = elemento
            break
    
    if tipo_nodo == 'asignacion':
        variable = nodo[1]
        operador = nodo[2]
        expresion = nodo[3]
        linea_nodo = extraer_linea(nodo)

        if isinstance(variable, tuple) and variable[0] == 'variable':
            nombre_var = variable[1]
        else:
            nombre_var = variable

        # No verificar palabras reservadas para variables de instancia
        if not nombre_var.startswith('@'):
            verificar_asignacion_palabra_reservada(nombre_var, linea_nodo)

        tipo_expr = obtener_tipo(expresion)

        # Variables de instancia siempre se aceptan sin verificaciones adicionales
        if nombre_var.startswith('@'):
            # Registrar variable de instancia en la tabla
            tabla_simbolos["variables"][nombre_var] = {
                "tipo": tipo_expr,
                "linea": linea_nodo,
                "valor": None
            }
        else:
            es_constante = nombre_var[0].isupper() if nombre_var else False

            if es_constante:
                # Solo procesar si no fue registrada en la Fase 1 (análisis de tokens)
                if nombre_var not in tabla_simbolos["constantes"]:
                    tabla_simbolos["constantes"][nombre_var] = {
                        "tipo": tipo_expr,
                        "linea": linea_nodo,
                        "valor": None
                    }
                else:
                    # Ya existe (registrada en Fase 1), verificar si es modificación
                    verificar_constante_modificada(nombre_var, linea_nodo)
            else:
                verificar_asignacion_incompatible(nombre_var, tipo_expr, linea_nodo)

                tabla_simbolos["variables"][nombre_var] = {
                    "tipo": tipo_expr,
                    "linea": linea_nodo,
                    "valor": None
                }

        analizar_nodo(expresion, linea_nodo)
    
    elif tipo_nodo == 'operacion_binaria':
        operador = nodo[1]
        izq = nodo[2]
        der = nodo[3]
        linea_nodo = extraer_linea(nodo)
        
        tipo_izq = obtener_tipo(izq)
        tipo_der = obtener_tipo(der)

        verificar_conversion_implicita(tipo_izq, tipo_der, operador, linea_nodo)
        
        verificar_operador_incompatible(operador, tipo_izq, tipo_der, linea_nodo)
        
        if operador == '/' and isinstance(der, int) and der == 0:
            verificar_division_por_cero(0, linea_nodo)
        
        analizar_nodo(izq, linea_nodo)
        analizar_nodo(der, linea_nodo)
    
    elif tipo_nodo == 'variable':
        nombre = nodo[1]
        linea_nodo = extraer_linea(nodo)
        verificar_variable_declarada(nombre, linea_nodo)

    elif tipo_nodo == 'comparacion':
        operador = nodo[1]
        izq = nodo[2]
        der = nodo[3]
        linea_nodo = extraer_linea(nodo)
        
        analizar_nodo(izq, linea_nodo)
        analizar_nodo(der, linea_nodo)

    elif tipo_nodo == 'operacion_logica':
        operador = nodo[1]
        izq = nodo[2]
        der = nodo[3]
        linea_nodo = extraer_linea(nodo)
        
        analizar_nodo(izq, linea_nodo)
        analizar_nodo(der, linea_nodo)

    elif tipo_nodo == 'not':
        expresion = nodo[1]
        linea_nodo = extraer_linea(nodo)
        analizar_nodo(expresion, linea_nodo)
    
    elif tipo_nodo == 'uminus':
        expresion = nodo[1]
        linea_nodo = extraer_linea(nodo)
        analizar_nodo(expresion, linea_nodo)
    
    elif tipo_nodo == 'parentesis':
        expresion = nodo[1]
        linea_nodo = extraer_linea(nodo)
        analizar_nodo(expresion, linea_nodo)
    
    elif tipo_nodo == 'valor':
        valor_interno = nodo[1]
        linea_nodo = extraer_linea(nodo)
        if isinstance(valor_interno, tuple):
            analizar_nodo(valor_interno, linea_nodo)
    
    elif tipo_nodo in ['if', 'if_else', 'if_elsif', 'if_elsif_else']:
        linea_nodo = extraer_linea(nodo)

        condicion = nodo[1]
        tipo_cond = obtener_tipo(condicion)
        verificar_condicion_booleana(tipo_cond, linea_nodo)
        
        analizar_nodo(condicion, linea_nodo)
        for i in range(2, len(nodo)):
            if isinstance(nodo[i], list):
                for sentencia in nodo[i]:
                    analizar_nodo(sentencia, linea_nodo)
            elif not isinstance(nodo[i], tuple):
                analizar_nodo(nodo[i], linea_nodo)

    elif tipo_nodo == 'elsif':
        linea_nodo = extraer_linea(nodo)
        condicion = nodo[1]
        sentencias = nodo[2]
        
        tipo_cond = obtener_tipo(condicion)
        verificar_condicion_booleana(tipo_cond, linea_nodo)
        analizar_nodo(condicion, linea_nodo)
        
        if isinstance(sentencias, list):
            for sentencia in sentencias:
                analizar_nodo(sentencia, linea_nodo)
                
    elif tipo_nodo in ['while', 'until']:
        linea_nodo = extraer_linea(nodo)

        en_loop_anterior = en_loop
        en_loop = True
        
        condicion = nodo[1]
        sentencias = nodo[2]
        
        tipo_cond = obtener_tipo(condicion)
        verificar_condicion_booleana(tipo_cond, linea_nodo)
        analizar_nodo(condicion, linea_nodo)
        
        if isinstance(sentencias, list):
            for sentencia in sentencias:
                analizar_nodo(sentencia, linea_nodo)

        en_loop = en_loop_anterior

    elif tipo_nodo == 'for':
        linea_nodo = extraer_linea(nodo)
        
        en_loop_anterior = en_loop
        en_loop = True
        
        variable = nodo[1]
        rango = nodo[2]
        sentencias = nodo[3]
        
        tabla_simbolos["variables"][variable] = {
            "tipo": 'integer',
            "linea": linea_nodo,
            "valor": None
        }
        
        analizar_nodo(rango, linea_nodo)
        
        if isinstance(sentencias, list):
            for sentencia in sentencias:
                analizar_nodo(sentencia, linea_nodo)
        
        en_loop = en_loop_anterior
    
    elif tipo_nodo in ['rango_inclusivo', 'rango_exclusivo']:
        linea_nodo = extraer_linea(nodo)
        inicio = nodo[1]
        fin = nodo[2]
        
        analizar_nodo(inicio, linea_nodo)
        analizar_nodo(fin, linea_nodo)
    
    elif tipo_nodo == 'control_flujo':
        palabra = nodo[1]
        linea_nodo = extraer_linea(nodo)
        
        if palabra in ['break', 'next', 'redo']:
            verificar_break_en_loop(linea_nodo)
    
    elif tipo_nodo == 'return_valor':
        linea_nodo = extraer_linea(nodo)
        expresion = nodo[1]
        
        verificar_retorno_valido('any', linea_nodo)
        tipo_ret = obtener_tipo(expresion)
        analizar_nodo(expresion, linea_nodo)
    
    elif tipo_nodo == 'funcion':
        nombre = nodo[1]
        parametros = nodo[2]
        cuerpo = nodo[3]
        linea_nodo = extraer_linea(nodo)

        en_funcion_anterior = en_funcion
        en_funcion = True

        # Primero registrar los parámetros ANTES de registrar la función
        params_lista = []
        if parametros:
            if isinstance(parametros, list):
                params_lista = parametros
            elif isinstance(parametros, tuple):
                # Si es una tupla, extraer el primer elemento
                params_lista = [parametros] if parametros[0] != 'vacio' else []
            elif isinstance(parametros, str):
                # Si es un string simple
                params_lista = [parametros] if parametros != 'sin parámetros' else []

        for param in params_lista:
            # Extraer el nombre del parámetro
            nombre_param = param
            if isinstance(param, tuple):
                # Si es una tupla, tomar el segundo elemento (el nombre)
                if len(param) > 1:
                    nombre_param = param[1]
                else:
                    nombre_param = param[0]

            # Registrar el parámetro como variable
            if nombre_param and isinstance(nombre_param, str) and nombre_param not in tabla_simbolos["variables"]:
                tabla_simbolos["variables"][nombre_param] = {
                    "tipo": 'any',
                    "linea": linea_nodo,
                    "valor": None
                }

        tabla_simbolos["funciones"][nombre] = {
            "parametros": params_lista,
            "linea": linea_nodo
        }

        if isinstance(cuerpo, list):
            for sentencia in cuerpo:
                analizar_nodo(sentencia, linea_nodo)

        en_funcion = en_funcion_anterior
    
    elif tipo_nodo == 'llamada_funcion':
        nombre = nodo[1]
        argumentos = nodo[2]
        linea_nodo = extraer_linea(nodo)
        
        if isinstance(argumentos, list):
            for arg in argumentos:
                analizar_nodo(arg, linea_nodo)
    
    elif tipo_nodo == 'impresion':
        tipo_imp = nodo[1]
        argumentos = nodo[2]
        linea_nodo = extraer_linea(nodo)
        
        if isinstance(argumentos, list):
            for arg in argumentos:
                analizar_nodo(arg, linea_nodo)
    
    elif tipo_nodo in ['entrada', 'entrada_asignacion']:
        linea_nodo = extraer_linea(nodo)
        if tipo_nodo == 'entrada_asignacion':
            variable = nodo[1]
            analizar_nodo(variable, linea_nodo)
    
    elif tipo_nodo == 'arreglo':
        elementos = nodo[1]
        linea_nodo = extraer_linea(nodo)
        
        if isinstance(elementos, list):
            for elem in elementos:
                analizar_nodo(elem, linea_nodo)
    
    elif tipo_nodo == 'hash':
        pares = nodo[1]
        linea_nodo = extraer_linea(nodo)
        
        if isinstance(pares, list):
            for par in pares:
                analizar_nodo(par, linea_nodo)
    
    elif tipo_nodo in ['par', 'par_simbolo']:
        clave = nodo[1]
        valor = nodo[2]
        linea_nodo = extraer_linea(nodo)
        
        analizar_nodo(clave, linea_nodo)
        analizar_nodo(valor, linea_nodo)
    
    elif tipo_nodo == 'clase':
        nombre = nodo[1]
        contenido = nodo[2]
        linea_nodo = extraer_linea(nodo)
        
        if isinstance(contenido, list):
            for sentencia in contenido:
                analizar_nodo(sentencia, linea_nodo)
    
    elif tipo_nodo == 'modulo':
        nombre = nodo[1]
        contenido = nodo[2]
        linea_nodo = extraer_linea(nodo)
        
        if isinstance(contenido, list):
            for sentencia in contenido:
                analizar_nodo(sentencia, linea_nodo)
    
    elif tipo_nodo == 'require':
        linea_nodo = extraer_linea(nodo)
        pass
    
    # PROGRAMA
    elif tipo_nodo == 'programa':
        sentencias = nodo[1]
        linea_nodo = extraer_linea(nodo)
        
        if isinstance(sentencias, list):
            for sentencia in sentencias:
                analizar_nodo(sentencia, linea_nodo)
        
# ============================================
# CREAR LOG SEMÁNTICO
# Dhamar Quishpe (@dquishpe)
# ============================================

def crear_log_semantico(errores, warnings, tabla, usuario, archivo_entrada):
    """
    Crea un archivo log del análisis semántico
    """
    fecha = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    
    carpeta_logs = os.path.join(os.path.dirname(__file__), "../logs")
    os.makedirs(carpeta_logs, exist_ok=True)
    
    nombre_log = os.path.join(carpeta_logs, f"semantico-{usuario}-{fecha}.txt")
    
    with open(nombre_log, 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write("ANALIZADOR SEMÁNTICO PARA RUBY\n")
        f.write("="*100 + "\n\n")
        f.write(f"Usuario: {usuario}\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Archivo analizado: {archivo_entrada}\n")
        f.write("="*100 + "\n\n")
        
        # Tabla de símbolos
        f.write("TABLA DE SÍMBOLOS:\n")
        f.write("="*100 + "\n\n")
        
        # Variables
        if tabla["variables"]:
            f.write("VARIABLES:\n")
            f.write("-"*100 + "\n")
            f.write(f"{'Nombre':<30} {'Tipo':<20} {'Línea':<15}\n")
            f.write("-"*100 + "\n")
            for nombre, info in tabla["variables"].items():
                f.write(f"{nombre:<30} {info['tipo']:<20} {info['linea']:<15}\n")
            f.write("-"*100 + "\n")
            f.write(f"Total de variables: {len(tabla['variables'])}\n\n")
        
        # Constantes
        if tabla["constantes"]:
            f.write("CONSTANTES:\n")
            f.write("-"*100 + "\n")
            f.write(f"{'Nombre':<30} {'Tipo':<20} {'Línea':<15}\n")
            f.write("-"*100 + "\n")
            for nombre, info in tabla["constantes"].items():
                f.write(f"{nombre:<30} {info['tipo']:<20} {info['linea']:<15}\n")
            f.write("-"*100 + "\n")
            f.write(f"Total de constantes: {len(tabla['constantes'])}\n\n")
        
        # Funciones
        if tabla["funciones"]:
            f.write("FUNCIONES:\n")
            f.write("-"*100 + "\n")
            f.write(f"{'Nombre':<30} {'Parámetros':<35} {'Línea':<15}\n")
            f.write("-"*100 + "\n")
            for nombre, info in tabla["funciones"].items():
                params = ", ".join(info['parametros']) if info['parametros'] else "sin parámetros"
                f.write(f"{nombre:<30} {params:<35} {info['linea']:<15}\n")
            f.write("-"*100 + "\n")
            f.write(f"Total de funciones: {len(tabla['funciones'])}\n\n")
        
        # Errores semánticos
        if errores:
            f.write("\nERRORES SEMÁNTICOS ENCONTRADOS:\n")
            f.write("="*100 + "\n")
            for i, error in enumerate(errores, 1):
                f.write(f"{i}. {error}\n")
            f.write("="*100 + "\n")
            f.write(f"Total de errores: {len(errores)}\n\n")
        
        # Advertencias
        if warnings:
            f.write("\nADVERTENCIAS SEMÁNTICAS:\n")
            f.write("="*100 + "\n")
            for i, warning in enumerate(warnings, 1):
                f.write(f"{i}. {warning}\n")
            f.write("="*100 + "\n")
            f.write(f"Total de advertencias: {len(warnings)}\n\n")
        
        # Resumen
        f.write("\nRESUMEN DEL ANÁLISIS:\n")
        f.write("="*100 + "\n")
        f.write(f"Variables declaradas:    {len(tabla['variables'])}\n")
        f.write(f"Constantes declaradas:   {len(tabla['constantes'])}\n")
        f.write(f"Funciones declaradas:    {len(tabla['funciones'])}\n")
        f.write(f"Errores encontrados:     {len(errores)}\n")
        f.write(f"Advertencias:            {len(warnings)}\n")
        f.write("="*100 + "\n")
        
        if not errores:
            f.write("\n[OK] ANÁLISIS SEMÁNTICO COMPLETADO SIN ERRORES\n")
        else:
            f.write("\n[ERROR] ANÁLISIS SEMÁNTICO COMPLETADO CON ERRORES\n")
        
        f.write("\n" + "="*100 + "\n")
        
    
    return nombre_log

# ============================================
# ANÁLISIS SEMÁNTICO PRINCIPAL
# José Marin @JoseM0lina
# ============================================

def analizar_tokens_semanticamente(archivo_entrada):
    """
    Analiza semánticamente el código línea por línea usando tokens léxicos.
    Esto captura errores semánticos incluso en código con errores sintácticos.
    """
    import ply.lex as lex
    import lexico as lexico_module

    # Obtener tokens del archivo
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        return

    # Crear lexer
    lexer = lex.lex(module=lexico_module)
    lexer.input(codigo)

    # Analizar tokens línea por línea
    tokens_list = []
    for tok in lexer:
        tokens_list.append(tok)

    # Variables locales para rastrear contexto
    en_loop_local = False
    en_funcion_local = False
    nivel_loop = 0
    nivel_funcion = 0

    # Procesar tokens para encontrar patrones semánticos
    i = 0
    while i < len(tokens_list):
        tok = tokens_list[i]

        # Rastrear contextos de loops
        if tok.type in ['WHILE', 'FOR', 'UNTIL']:
            nivel_loop += 1
            en_loop_local = True
        elif tok.type == 'DEF':
            nivel_funcion += 1
            en_funcion_local = True
        elif tok.type == 'END':
            if nivel_loop > 0:
                nivel_loop -= 1
                if nivel_loop == 0:
                    en_loop_local = False
            elif nivel_funcion > 0:
                nivel_funcion -= 1
                if nivel_funcion == 0:
                    en_funcion_local = False

        # Detectar asignaciones a palabras reservadas
        if tok.type in ['VARIABLE_LOCAL', 'CONSTANTE'] and i + 1 < len(tokens_list):
            if tokens_list[i + 1].type in ['ASIGNACION', 'SUMA_ASIG', 'RESTA_ASIG', 'MULT_ASIG', 'DIV_ASIG']:
                nombre_var = tok.value
                linea = tok.lineno

                # Regla 4: Asignación a palabra reservada
                verificar_asignacion_palabra_reservada(nombre_var, linea)

                # Si es constante, verificar modificación
                if tok.type == 'CONSTANTE':
                    # Solo registrar si es la primera vez que se declara
                    if nombre_var not in tabla_simbolos["constantes"]:
                        tabla_simbolos["constantes"][nombre_var] = {
                            "tipo": 'any',
                            "linea": linea,
                            "valor": None
                        }
                    else:
                        # Ya existe, entonces es una modificación (error)
                        verificar_constante_modificada(nombre_var, linea)
                else:
                    # Registrar variable
                    if nombre_var not in tabla_simbolos["variables"]:
                        tabla_simbolos["variables"][nombre_var] = {
                            "tipo": 'any',
                            "linea": linea,
                            "valor": None
                        }

        # Detectar uso de variables no declaradas
        elif tok.type in ['VARIABLE_LOCAL', 'VARIABLE_GLOBAL', 'VARIABLE_INSTANCIA', 'VARIABLE_CLASE']:
            # Solo verificar si no está siendo declarada (siguiente token no es asignación)
            nombre_var = tok.value
            linea = tok.lineno

            if i + 1 < len(tokens_list) and tokens_list[i + 1].type not in ['ASIGNACION', 'SUMA_ASIG', 'RESTA_ASIG', 'MULT_ASIG', 'DIV_ASIG']:
                # Regla 1: Variable no declarada
                verificar_variable_declarada(nombre_var, linea)

        # Detectar break/next/redo fuera de loop
        elif tok.type in ['BREAK', 'NEXT', 'REDO']:
            linea = tok.lineno
            if not en_loop_local:
                # Regla 7: break fuera de loop
                error = f"Error semántico en línea {linea}: '{tok.value}' usado fuera de un bucle"
                if error not in errores_semanticos:
                    errores_semanticos.append(error)

        # Detectar return fuera de función
        elif tok.type == 'RETURN':
            linea = tok.lineno
            if not en_funcion_local:
                # Regla 11: return fuera de función
                error = f"Error semántico en línea {linea}: 'return' usado fuera de una función"
                if error not in errores_semanticos:
                    errores_semanticos.append(error)

        i += 1

def analizar_semantica(archivo_entrada, usuario_git, mostrar_sintactico=True):
    """
    Realiza el análisis semántico completo de un archivo Ruby
    utilizando el árbol sintáctico generado por sintactico.py
    """
    reiniciar_analisis()

    print("\n" + "="*100)
    print(f"{'ANALIZADOR SEMÁNTICO PARA RUBY':^100}")
    print("="*100)
    print(f"\n{'Usuario:':<20} {usuario_git}")
    print(f"{'Archivo analizado:':<20} {archivo_entrada}")
    print(f"{'Fecha:':<20} {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("\n" + "="*100)
    print("REALIZANDO ANÁLISIS SEMÁNTICO BASADO EN TOKENS...")
    print("-"*100)

    # FASE 1: Análisis basado en tokens (cubre TODO el código, incluso con errores sintácticos)
    analizar_tokens_semanticamente(archivo_entrada)

    print("\n[OK] Análisis de tokens completado")
    print("="*100)
    print("OBTENIENDO ÁRBOL SINTÁCTICO...")
    print("-"*100)

    # Obtener el árbol sintáctico del analizador sintáctico
    resultado_sintactico, errores_sint = analizar_sintaxis(archivo_entrada, usuario_git)

    if errores_sint:
        print("\n[ADVERTENCIA] Errores sintácticos encontrados, pero continuando con análisis semántico...")
        print("="*100)
        # NO retornar, continuar con lo que se pudo parsear

    print("\n[OK] Árbol sintáctico obtenido correctamente")
    print("="*100)
    print("\nREALIZANDO ANÁLISIS SEMÁNTICO PROFUNDO (BASADO EN ÁRBOL)...")
    print("-"*100)

    # FASE 2: Analizar el árbol sintáctico (validaciones más complejas)
    if resultado_sintactico:
        analizar_nodo(resultado_sintactico)

    # Eliminar errores duplicados (pueden aparecer tanto en análisis de tokens como de árbol)
    global errores_semanticos, warnings_semanticos
    errores_semanticos = list(dict.fromkeys(errores_semanticos))  # Mantiene orden y elimina duplicados
    warnings_semanticos = list(dict.fromkeys(warnings_semanticos))

    print("-"*100)
    
    # Mostrar tabla de símbolos
    print("\nTABLA DE SÍMBOLOS:")
    print("="*100)
    
    if tabla_simbolos["variables"]:
        print("\nVARIABLES:")
        print("-"*100)
        print(f"{'Nombre':<30} {'Tipo':<20} {'Línea':<15}")
        print("-"*100)
        for nombre, info in tabla_simbolos["variables"].items():
            print(f"{nombre:<30} {info['tipo']:<20} {info['linea']:<15}")
        print("-"*100)
        print(f"Total: {len(tabla_simbolos['variables'])}\n")
    
    if tabla_simbolos["constantes"]:
        print("CONSTANTES:")
        print("-"*100)
        print(f"{'Nombre':<30} {'Tipo':<20} {'Línea':<15}")
        print("-"*100)
        for nombre, info in tabla_simbolos["constantes"].items():
            print(f"{nombre:<30} {info['tipo']:<20} {info['linea']:<15}")
        print("-"*100)
        print(f"Total: {len(tabla_simbolos['constantes'])}\n")
    
    if tabla_simbolos["funciones"]:
        print("FUNCIONES:")
        print("-"*100)
        print(f"{'Nombre':<30} {'Parámetros':<35} {'Línea':<15}")
        print("-"*100)
        for nombre, info in tabla_simbolos["funciones"].items():
            params = ", ".join(info['parametros']) if info['parametros'] else "sin parámetros"
            print(f"{nombre:<30} {params:<35} {info['linea']:<15}")
        print("-"*100)
        print(f"Total: {len(tabla_simbolos['funciones'])}\n")
    
    # Mostrar errores
    if errores_semanticos:
        print("\nERRORES SEMÁNTICOS:")
        print("="*100)
        for i, error in enumerate(errores_semanticos, 1):
            print(f"{i}. {error}")
        print("="*100)
    
    # Mostrar advertencias
    if warnings_semanticos:
        print("\nADVERTENCIAS:")
        print("="*100)
        for i, warning in enumerate(warnings_semanticos, 1):
            print(f"{i}. {warning}")
        print("="*100)
    
    # Resumen
    print("\nRESUMEN:")
    print("="*100)
    print(f"Variables declaradas:    {len(tabla_simbolos['variables'])}")
    print(f"Constantes declaradas:   {len(tabla_simbolos['constantes'])}")
    print(f"Funciones declaradas:    {len(tabla_simbolos['funciones'])}")
    print(f"Errores encontrados:     {len(errores_semanticos)}")
    print(f"Advertencias:            {len(warnings_semanticos)}")
    print("="*100)
    
    if not errores_semanticos:
        print("\n[OK] ANÁLISIS SEMÁNTICO COMPLETADO SIN ERRORES")
    else:
        print(f"\n[ERROR] ANÁLISIS SEMÁNTICO COMPLETADO CON {len(errores_semanticos)} ERROR(ES)")
    
    print("="*100)
    
    # Crear log
    try:
        nombre_log = crear_log_semantico(errores_semanticos, warnings_semanticos, 
                                         tabla_simbolos, usuario_git, archivo_entrada)
        print(f"\n[LOG] Archivo guardado en: {nombre_log}")
    except Exception as e:
        print(f"\n[ERROR] No se pudo crear el log: {e}")
        print(f"Carpeta actual: {os.getcwd()}")
        print(f"Intentando crear en: {os.path.join(os.path.dirname(__file__), '../logs')}")
    
    print("="*100 + "\n")
    
    return resultado_sintactico, errores_semanticos

# ============================================
# MAIN
# José Marin (@JoseM0lina)
# ============================================

if __name__ == '__main__':
    if len(sys.argv) > 2:
        archivo = sys.argv[1]
        usuario = sys.argv[2]
        
        print("\n" + "="*100)
        print(f"{'COMPILADOR RUBY - ANÁLISIS COMPLETO':^100}")
        print("="*100)
        
        print("\n[FASE 1] ANÁLISIS LÉXICO")
        print("="*100)
        try:
            tokens_lex, errores_lex = analizar_archivo(archivo, usuario)
        except Exception as e:
            print(f"[ERROR] Error en análisis léxico: {e}")
            errores_lex = [str(e)]
        
        # Continuar aunque haya errores léxicos
        print("\n[FASE 2] ANÁLISIS SINTÁCTICO")
        print("="*100)
        
        print("\n[FASE 3] ANÁLISIS SEMÁNTICO")
        print("="*100)
        try:
            analizar_semantica(archivo, usuario)
        except Exception as e:
            print(f"[ERROR] Error en análisis semántico: {e}")
            print(f"Detalles: {type(e).__name__}")
            import traceback
            traceback.print_exc()
    else:
        print("\n" + "="*100)
        print("[ERROR] Uso incorrecto del programa")
        print("="*100)
        print("\n   Uso: python semantico.py <archivo_ruby> <usuario_git>")
        print("   Ejemplo: python semantico.py test.rb dquishpe\n")
        print("="*100)
