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