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
    if nombre not in tabla_simbolos["variables"] and nombre not in tabla_simbolos["constantes"]:
        error = f"Error semántico en línea {linea}: Variable '{nombre}' no declarada antes de su uso"
        errores_semanticos.append(error)
        return False
    return True

def verificar_constante_modificada(nombre, linea=0):
    """
    Regla 2: Constante modificada
    Asegura que las constantes no puedan ser reasignadas
    """
    if nombre in tabla_simbolos["constantes"]:
        error = f"Error semántico en línea {linea}: Constante '{nombre}' no puede ser modificada (ya fue declarada en línea {tabla_simbolos['constantes'][nombre]['linea']})"
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
# FUNCIONES AUXILIARES
# Angelo Zurita (@aszurita)
# ============================================

def obtener_tipo(valor):
    """Obtiene el tipo de un valor del árbol sintáctico"""
    if isinstance(valor, tuple):
        if valor[0] == 'valor':
            return obtener_tipo(valor[1])
        elif valor[0] == 'variable':
            nombre = valor[1]
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
    
    if tipo_nodo == 'asignacion':
        variable = nodo[1]
        operador = nodo[2]
        expresion = nodo[3]
        
        nombre_var = variable[1] if isinstance(variable, tuple) else variable
        verificar_asignacion_palabra_reservada(nombre_var, linea)
        
        tipo_expr = obtener_tipo(expresion)
        
        es_constante = nombre_var[0].isupper() if nombre_var else False
        
        if es_constante:
            if verificar_constante_modificada(nombre_var, linea):
                tabla_simbolos["constantes"][nombre_var] = {
                    "tipo": tipo_expr,
                    "linea": linea,
                    "valor": None
                }
        else:
            verificar_asignacion_incompatible(nombre_var, tipo_expr, linea)
            
            tabla_simbolos["variables"][nombre_var] = {
                "tipo": tipo_expr,
                "linea": linea,
                "valor": None
            }
        
        analizar_nodo(expresion, linea)
    
    elif tipo_nodo == 'operacion_binaria':
        operador = nodo[1]
        izq = nodo[2]
        der = nodo[3]
        
        tipo_izq = obtener_tipo(izq)
        tipo_der = obtener_tipo(der)

        verificar_conversion_implicita(tipo_izq, tipo_der, operador, linea)
        
        verificar_operador_incompatible(operador, tipo_izq, tipo_der, linea)
        
        if operador == '/' and isinstance(der, int) and der == 0:
            verificar_division_por_cero(0, linea)
        
        analizar_nodo(izq, linea)
        analizar_nodo(der, linea)
    
    elif tipo_nodo == 'variable':
        nombre = nodo[1]
        verificar_variable_declarada(nombre, linea)
    
    elif tipo_nodo in ['if', 'if_else', 'if_elsif', 'if_elsif_else']:
        condicion = nodo[1]
        tipo_cond = obtener_tipo(condicion)
        verificar_condicion_booleana(tipo_cond, linea)
        
        analizar_nodo(condicion, linea)
        for i in range(2, len(nodo)):
            if isinstance(nodo[i], list):
                for sentencia in nodo[i]:
                    analizar_nodo(sentencia, linea + 1)
            else:
                analizar_nodo(nodo[i], linea + 1)
                
    elif tipo_nodo in ['while', 'until', 'for']:
        en_loop_anterior = en_loop
        en_loop = True
        
        if tipo_nodo in ['while', 'until']:
            condicion = nodo[1]
            sentencias = nodo[2]
            tipo_cond = obtener_tipo(condicion)
            verificar_condicion_booleana(tipo_cond, linea)
            analizar_nodo(condicion, linea)
        else:  
            sentencias = nodo[3] if len(nodo) > 3 else nodo[2]
        
        if isinstance(sentencias, list):
            for sentencia in sentencias:
                analizar_nodo(sentencia, linea + 1)
        
        en_loop = en_loop_anterior
    
    elif tipo_nodo == 'control_flujo':
        palabra = nodo[1]
        if palabra in ['break', 'next', 'redo']:
            verificar_break_en_loop(linea)
    
    elif tipo_nodo == 'funcion':
        nombre = nodo[1]
        parametros = nodo[2]
        cuerpo = nodo[3]
        
        en_funcion_anterior = en_funcion
        en_funcion = True
        
        tabla_simbolos["funciones"][nombre] = {
            "parametros": parametros,
            "linea": linea
        }
        
        for param in parametros:
            if param not in tabla_simbolos["variables"]:
                tabla_simbolos["variables"][param] = {
                    "tipo": 'any',
                    "linea": linea,
                    "valor": None
                }
        
        if isinstance(cuerpo, list):
            for sentencia in cuerpo:
                analizar_nodo(sentencia, linea + 1)
        
        en_funcion = en_funcion_anterior
    
    elif tipo_nodo == 'return_valor':
        verificar_retorno_valido('any', linea)
        expresion = nodo[1]
        tipo_ret = obtener_tipo(expresion)
        analizar_nodo(expresion, linea)
    
    # PROGRAMA
    elif tipo_nodo == 'programa':
        sentencias = nodo[1]
        if isinstance(sentencias, list):
            for sentencia in sentencias:
                analizar_nodo(sentencia, linea)
    
    elif tipo_nodo == 'valor':
        valor_interno = nodo[1]
        analizar_nodo(valor_interno, linea)
        
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