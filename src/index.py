import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import os
import sys

# Importar los analizadores
from lexico import analizar_archivo as analizar_lexico
from sintactico import analizar_sintaxis
import semantico

class AnalizadorRubyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Ruby - Análisis Léxico, Sintáctico y Semántico")
        self.root.geometry("1400x800")
        self.root.configure(bg='#1e1e2e')
        
        # Variables
        self.errores_lexico = 0
        self.errores_sintactico = 0
        self.errores_semantico = 0
        self.exito = False
        
        # Crear interfaz
        self.crear_header()
        self.crear_main_container()
        self.crear_footer()
        
    def crear_header(self):
        """Crear el encabezado de la aplicación"""
        header = tk.Frame(self.root, bg='#2d2d44', height=80)
        header.pack(fill='x', padx=10, pady=(10, 0))
        header.pack_propagate(False)
        
        # Título
        titulo_frame = tk.Frame(header, bg='#2d2d44')
        titulo_frame.pack(side='left', padx=20, pady=10)
        
        tk.Label(
            titulo_frame,
            text="🔍 Analizador Ruby",
            font=('Segoe UI', 24, 'bold'),
            bg='#2d2d44',
            fg='#ffffff'
        ).pack(anchor='w')
        
        tk.Label(
            titulo_frame,
            text="Análisis Léxico, Sintáctico y Semántico",
            font=('Segoe UI', 11),
            bg='#2d2d44',
            fg='#a0a0a0'
        ).pack(anchor='w')
        
        # Botón analizar - CORREGIDO: separar creación de pack()
        btn_frame = tk.Frame(header, bg='#2d2d44')
        btn_frame.pack(side='right', padx=20)
        
        self.btn_analizar = tk.Button(
            btn_frame,
            text="▶ ANALIZAR",
            font=('Segoe UI', 12, 'bold'),
            bg='#50fa7b',
            fg='#1e1e2e',
            activebackground='#5af78e',
            activeforeground='#1e1e2e',
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=15,
            command=self.analizar_codigo
        )
        self.btn_analizar.pack()
        
    def crear_main_container(self):
        """Crear el contenedor principal con editor y panel de resultados"""
        main_container = tk.Frame(self.root, bg='#1e1e2e')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Editor
        self.crear_panel_editor(main_container)
        
        # Panel derecho - Resultados
        self.crear_panel_resultados(main_container)
        
    def crear_panel_editor(self, parent):
        """Crear el panel del editor de código"""
        editor_frame = tk.Frame(parent, bg='#2d2d44', width=700)
        editor_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Header del editor
        editor_header = tk.Frame(editor_frame, bg='#3d3d5c', height=50)
        editor_header.pack(fill='x')
        editor_header.pack_propagate(False)
        
        tk.Label(
            editor_header,
            text="📝 Editor de Código",
            font=('Segoe UI', 12, 'bold'),
            bg='#3d3d5c',
            fg='#ffffff'
        ).pack(side='left', padx=15, pady=10)
        
        # Frame para el texto con números de línea
        text_frame = tk.Frame(editor_frame, bg='#2d2d44')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Números de línea
        self.line_numbers = tk.Text(
            text_frame,
            width=4,
            padx=5,
            pady=5,
            font=('Consolas', 10),
            bg='#252535',
            fg='#6272a4',
            state='disabled',
            relief='flat'
        )
        self.line_numbers.pack(side='left', fill='y')
        
        # Editor de código
        self.editor = scrolledtext.ScrolledText(
            text_frame,
            wrap='none',
            font=('Consolas', 10),
            bg='#282a36',
            fg='#f8f8f2',
            insertbackground='#50fa7b',
            selectbackground='#44475a',
            relief='flat',
            padx=10,
            pady=5
        )
        self.editor.pack(side='left', fill='both', expand=True)
        
        # Código de ejemplo
        codigo_ejemplo = '''# Escriba o pegue su código Ruby aquí...
# Ejemplo:
nombre = "Ruby"
edad = 25

if edad >= 18
  puts "Mayor de edad"
end'''
        self.editor.insert('1.0', codigo_ejemplo)
        
        # Bind para actualizar números de línea - múltiples eventos para mantenerlo dinámico
        self.editor.bind('<KeyRelease>', self.actualizar_numeros_linea)
        self.editor.bind('<Return>', self.actualizar_numeros_linea)
        self.editor.bind('<BackSpace>', self.actualizar_numeros_linea)
        self.editor.bind('<Delete>', self.actualizar_numeros_linea)
        self.editor.bind('<MouseWheel>', self.actualizar_numeros_linea)
        self.editor.bind('<Button-1>', self.actualizar_numeros_linea)
        self.editor.bind('<<Modified>>', self.actualizar_numeros_linea)
        self.editor.bind('<<Change>>', self.actualizar_numeros_linea)
        self.editor.bind('<<Paste>>', self.actualizar_numeros_linea)
        self.actualizar_numeros_linea()
        
    def actualizar_numeros_linea(self, event=None):
        """Actualizar los números de línea dinámicamente"""
        try:
            # Obtener el número total de líneas del editor
            num_lines = int(self.editor.index('end-1c').split('.')[0])

            # Generar los números de línea
            line_numbers_content = '\n'.join(str(i) for i in range(1, num_lines + 1))

            # Actualizar el widget de números de línea
            self.line_numbers.config(state='normal')
            self.line_numbers.delete('1.0', 'end')
            self.line_numbers.insert('1.0', line_numbers_content)
            self.line_numbers.config(state='disabled')

            # Sincronizar el scroll del editor con los números de línea
            self.sincronizar_scroll()
        except Exception as e:
            print(f"Error actualizando números de línea: {e}")

    def sincronizar_scroll(self):
        """Sincronizar el scroll entre números de línea y editor"""
        try:
            # Obtener la posición de scroll del editor
            first_visible = self.editor.yview()[0]

            # Aplicar el mismo scroll a los números de línea
            self.line_numbers.yview_moveto(first_visible)
        except Exception as e:
            print(f"Error sincronizando scroll: {e}")
        
    def crear_panel_resultados(self, parent):
        """Crear el panel de resultados"""
        resultados_frame = tk.Frame(parent, bg='#2d2d44', width=650)
        resultados_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        resultados_frame.pack_propagate(False)
        
        # Header del panel
        header = tk.Frame(resultados_frame, bg='#3d3d5c', height=50)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Campo nombre del tester
        nombre_frame = tk.Frame(header, bg='#3d3d5c')
        nombre_frame.pack(side='left', padx=15, pady=8)
        
        tk.Label(
            nombre_frame,
            text="Nombre del Tester:",
            font=('Segoe UI', 10),
            bg='#3d3d5c',
            fg='#ffffff'
        ).pack(side='left', padx=(0, 10))
        
        self.nombre_entry = tk.Entry(
            nombre_frame,
            font=('Segoe UI', 10),
            bg='#44475a',
            fg='#f8f8f2',
            relief='flat',
            width=15,
            insertbackground='#50fa7b'
        )
        self.nombre_entry.pack(side='left')
        self.nombre_entry.insert(0, "Angelo")
        
        # Notebook para pestañas
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#2d2d44', borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background='#3d3d5c',
                       foreground='#ffffff',
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', '#282a36')],
                 foreground=[('selected', '#50fa7b')])
        
        self.notebook = ttk.Notebook(resultados_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.crear_tab_resumen()
        self.crear_tab_lexico()
        self.crear_tab_sintactico()
        self.crear_tab_semantico()
        self.crear_tab_tabla_simbolos()
        
    def crear_tab_resumen(self):
        """Crear la pestaña de resumen"""
        tab = tk.Frame(self.notebook, bg='#2d2d44')
        self.notebook.add(tab, text='📊 Resumen')
        
        # Grid para los contadores
        contadores_frame = tk.Frame(tab, bg='#2d2d44')
        contadores_frame.pack(expand=True, pady=20)
        
        # Léxico
        self.card_lexico = self.crear_card(
            contadores_frame, "Léxico", "#ff5555", row=0, col=0)
        
        # Sintáctico
        self.card_sintactico = self.crear_card(
            contadores_frame, "Sintáctico", "#ffb86c", row=0, col=1)
        
        # Semántico
        self.card_semantico = self.crear_card(
            contadores_frame, "Semántico", "#f1fa8c", row=1, col=0)
        
        # Éxito
        self.card_exito = self.crear_card(
            contadores_frame, "Éxito", "#50fa7b", row=1, col=1)
        
    def crear_card(self, parent, titulo, color, row, col):
        """Crear una tarjeta de contador"""
        card = tk.Frame(parent, bg='#3d3d5c', relief='flat', bd=0)
        card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        
        # Configurar grid
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1, minsize=250)
        
        # Título
        tk.Label(
            card,
            text=titulo,
            font=('Segoe UI', 12, 'bold'),
            bg='#3d3d5c',
            fg='#ffffff'
        ).pack(pady=(20, 10))
        
        # Contador
        label = tk.Label(
            card,
            text="0",
            font=('Segoe UI', 48, 'bold'),
            bg='#3d3d5c',
            fg=color
        )
        label.pack(pady=(0, 20))
        
        # Configurar tamaño mínimo
        card.configure(width=250, height=150)
        card.pack_propagate(False)
        
        return label
        
    def crear_tab_lexico(self):
        """Crear la pestaña de análisis léxico"""
        tab = tk.Frame(self.notebook, bg='#2d2d44')
        self.notebook.add(tab, text='🔤 Léxico')
        
        self.texto_lexico = scrolledtext.ScrolledText(
            tab,
            wrap='word',
            font=('Consolas', 9),
            bg='#282a36',
            fg='#f8f8f2',
            relief='flat',
            padx=10,
            pady=10
        )
        self.texto_lexico.pack(fill='both', expand=True, padx=10, pady=10)
        
    def crear_tab_sintactico(self):
        """Crear la pestaña de análisis sintáctico"""
        tab = tk.Frame(self.notebook, bg='#2d2d44')
        self.notebook.add(tab, text='🔧 Sintáctico')
        
        self.texto_sintactico = scrolledtext.ScrolledText(
            tab,
            wrap='word',
            font=('Consolas', 9),
            bg='#282a36',
            fg='#f8f8f2',
            relief='flat',
            padx=10,
            pady=10
        )
        self.texto_sintactico.pack(fill='both', expand=True, padx=10, pady=10)
        
    def crear_tab_semantico(self):
        """Crear la pestaña de análisis semántico"""
        tab = tk.Frame(self.notebook, bg='#2d2d44')
        self.notebook.add(tab, text='🧠 Semántico')
        
        self.texto_semantico = scrolledtext.ScrolledText(
            tab,
            wrap='word',
            font=('Consolas', 9),
            bg='#282a36',
            fg='#f8f8f2',
            relief='flat',
            padx=10,
            pady=10
        )
        self.texto_semantico.pack(fill='both', expand=True, padx=10, pady=10)
        
    def crear_tab_tabla_simbolos(self):
        """Crear la pestaña de tabla de símbolos"""
        tab = tk.Frame(self.notebook, bg='#2d2d44')
        self.notebook.add(tab, text='📋 Tabla de Símbolos')
        
        self.texto_tabla = scrolledtext.ScrolledText(
            tab,
            wrap='word',
            font=('Consolas', 9),
            bg='#282a36',
            fg='#f8f8f2',
            relief='flat',
            padx=10,
            pady=10
        )
        self.texto_tabla.pack(fill='both', expand=True, padx=10, pady=10)
        
    def crear_footer(self):
        """Crear el pie de página con estado"""
        footer = tk.Frame(self.root, bg='#2d2d44', height=40)
        footer.pack(fill='x', padx=10, pady=(0, 10))
        footer.pack_propagate(False)
        
        self.estado_label = tk.Label(
            footer,
            text="⏳ Esperando análisis...",
            font=('Segoe UI', 10),
            bg='#2d2d44',
            fg='#6272a4',
            anchor='w'
        )
        self.estado_label.pack(side='left', padx=20, pady=10)
        
        self.info_label = tk.Label(
            footer,
            text="Grupo 12 - Lenguajes de Programación",
            font=('Segoe UI', 9),
            bg='#2d2d44',
            fg='#6272a4',
            anchor='e'
        )
        self.info_label.pack(side='right', padx=20, pady=10)
        
    def analizar_codigo(self):
        """Ejecutar el análisis completo"""
        # Limpiar resultados anteriores
        self.limpiar_resultados()
        
        # Obtener código y nombre
        codigo = self.editor.get('1.0', 'end-1c')
        nombre_tester = self.nombre_entry.get().strip()
        
        if not nombre_tester:
            messagebox.showwarning("Advertencia", "Por favor ingrese el nombre del tester")
            return
        
        if not codigo.strip():
            messagebox.showwarning("Advertencia", "Por favor ingrese código Ruby para analizar")
            return
        
        # Actualizar estado
        self.estado_label.config(text="⚙️ Analizando código...", fg='#ffb86c')
        self.btn_analizar.config(state='disabled')
        self.root.update()
        
        try:
            # Guardar código temporalmente
            temp_file = 'temp_codigo.rb'
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(codigo)
            
            # 1. ANÁLISIS LÉXICO
            self.texto_lexico.insert('1.0', "Ejecutando análisis léxico...\n\n")
            self.root.update()
            
            tokens_lex, errores_lex = analizar_lexico(temp_file, nombre_tester)
            self.errores_lexico = len(errores_lex) if errores_lex else 0
            
            if errores_lex:
                resultado_lex = "❌ ERRORES LÉXICOS ENCONTRADOS:\n\n"
                for i, error in enumerate(errores_lex, 1):
                    resultado_lex += f"{i}. {error}\n"
            else:
                resultado_lex = "✅ ANÁLISIS LÉXICO COMPLETADO SIN ERRORES\n\n"
                resultado_lex += f"Total de tokens reconocidos: {len(tokens_lex) if tokens_lex else 0}"
            
            self.texto_lexico.delete('1.0', 'end')
            self.texto_lexico.insert('1.0', resultado_lex)
            
            # 2. ANÁLISIS SINTÁCTICO
            self.texto_sintactico.insert('1.0', "Ejecutando análisis sintáctico...\n\n")
            self.root.update()
            
            resultado_sint, errores_sint = analizar_sintaxis(temp_file, nombre_tester)
            self.errores_sintactico = len(errores_sint) if errores_sint else 0
            
            if errores_sint:
                resultado_sintactico = "❌ ERRORES SINTÁCTICOS ENCONTRADOS:\n\n"
                for i, error in enumerate(errores_sint, 1):
                    resultado_sintactico += f"{i}. {error}\n"
            else:
                resultado_sintactico = "✅ ANÁLISIS SINTÁCTICO COMPLETADO SIN ERRORES\n\n"
                resultado_sintactico += "Todas las construcciones sintácticas son válidas."
            
            self.texto_sintactico.delete('1.0', 'end')
            self.texto_sintactico.insert('1.0', resultado_sintactico)
            
            # 3. ANÁLISIS SEMÁNTICO
            self.texto_semantico.insert('1.0', "Ejecutando análisis semántico...\n\n")
            self.root.update()
            
            semantico.reiniciar_analisis()
            resultado_sem, errores_sem = semantico.analizar_semantica(temp_file, nombre_tester, mostrar_sintactico=False)
            self.errores_semantico = len(errores_sem) if errores_sem else 0
            
            if errores_sem:
                resultado_semantico = "❌ ERRORES SEMÁNTICOS ENCONTRADOS:\n\n"
                for i, error in enumerate(errores_sem, 1):
                    resultado_semantico += f"{i}. {error}\n"
            else:
                resultado_semantico = "✅ ANÁLISIS SEMÁNTICO COMPLETADO SIN ERRORES\n\n"
                resultado_semantico += "El código es semánticamente correcto."
            
            if semantico.warnings_semanticos:
                resultado_semantico += "\n\n⚠️ ADVERTENCIAS:\n\n"
                for i, warning in enumerate(semantico.warnings_semanticos, 1):
                    resultado_semantico += f"{i}. {warning}\n"
            
            self.texto_semantico.delete('1.0', 'end')
            self.texto_semantico.insert('1.0', resultado_semantico)
            
            # 4. TABLA DE SÍMBOLOS
            tabla_texto = self.generar_tabla_simbolos(semantico.tabla_simbolos)
            self.texto_tabla.delete('1.0', 'end')
            self.texto_tabla.insert('1.0', tabla_texto)
            
            # Actualizar contadores
            self.actualizar_contadores()
            
            # Limpiar archivo temporal
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Estado final
            if self.exito:
                self.estado_label.config(
                    text="✅ Análisis completado - Sin errores", 
                    fg='#50fa7b'
                )
            else:
                total_errores = self.errores_lexico + self.errores_sintactico + self.errores_semantico
                self.estado_label.config(
                    text=f"❌ Análisis completado - {total_errores} error(es) encontrado(s)",
                    fg='#ff5555'
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el análisis:\n{str(e)}")
            self.estado_label.config(text="❌ Error en el análisis", fg='#ff5555')
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            self.btn_analizar.config(state='normal')
            
    def generar_tabla_simbolos(self, tabla):
        """Generar texto de la tabla de símbolos"""
        texto = "TABLA DE SÍMBOLOS\n"
        texto += "=" * 80 + "\n\n"
        
        if tabla and tabla.get("variables"):
            texto += "VARIABLES:\n"
            texto += "-" * 80 + "\n"
            texto += f"{'Nombre':<30} {'Tipo':<20} {'Línea':<15}\n"
            texto += "-" * 80 + "\n"
            for nombre, info in tabla["variables"].items():
                texto += f"{nombre:<30} {info['tipo']:<20} {info['linea']:<15}\n"
            texto += f"\nTotal: {len(tabla['variables'])}\n\n"
        
        if tabla and tabla.get("constantes"):
            texto += "CONSTANTES:\n"
            texto += "-" * 80 + "\n"
            texto += f"{'Nombre':<30} {'Tipo':<20} {'Línea':<15}\n"
            texto += "-" * 80 + "\n"
            for nombre, info in tabla["constantes"].items():
                texto += f"{nombre:<30} {info['tipo']:<20} {info['linea']:<15}\n"
            texto += f"\nTotal: {len(tabla['constantes'])}\n\n"
        
        if tabla and tabla.get("funciones"):
            texto += "FUNCIONES:\n"
            texto += "-" * 80 + "\n"
            texto += f"{'Nombre':<30} {'Parámetros':<35} {'Línea':<15}\n"
            texto += "-" * 80 + "\n"
            for nombre, info in tabla["funciones"].items():
                params = ", ".join(info['parametros']) if info['parametros'] else "sin parámetros"
                texto += f"{nombre:<30} {params:<35} {info['linea']:<15}\n"
            texto += f"\nTotal: {len(tabla['funciones'])}\n"
        
        if not tabla or (not tabla.get("variables") and not tabla.get("constantes") and not tabla.get("funciones")):
            texto += "No se encontraron símbolos\n"
        
        return texto
            
    def actualizar_contadores(self):
        """Actualizar los contadores en el resumen"""
        self.card_lexico.config(text=str(self.errores_lexico))
        self.card_sintactico.config(text=str(self.errores_sintactico))
        self.card_semantico.config(text=str(self.errores_semantico))
        
        total_errores = self.errores_lexico + self.errores_sintactico + self.errores_semantico
        self.exito = (total_errores == 0)
        
        if self.exito:
            self.card_exito.config(text="✓", fg='#50fa7b')
        else:
            self.card_exito.config(text="✗", fg='#ff5555')
            
    def limpiar_resultados(self):
        """Limpiar todos los resultados anteriores"""
        self.errores_lexico = 0
        self.errores_sintactico = 0
        self.errores_semantico = 0
        self.exito = False
        
        self.card_lexico.config(text="0")
        self.card_sintactico.config(text="0")
        self.card_semantico.config(text="0")
        self.card_exito.config(text="0")
        
        self.texto_lexico.delete('1.0', 'end')
        self.texto_sintactico.delete('1.0', 'end')
        self.texto_semantico.delete('1.0', 'end')
        self.texto_tabla.delete('1.0', 'end')

def main():
    root = tk.Tk()
    app = AnalizadorRubyGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()