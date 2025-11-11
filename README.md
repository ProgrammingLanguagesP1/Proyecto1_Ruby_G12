# Proyecto1_Ruby_G12

Analizador Léxico, Sintáctico y Semántico para Ruby

## 👥 Integrantes - Grupo 12

- **Angelo Zurita** (@aszurita)
- **Dhamar Quishpe** (@dquishpe)  
- **José Marín** (@JoseM0lina)

## 📝 Descripción

Proyecto de análisis léxico para el lenguaje Ruby desarrollado con Python y PLY (Python Lex-Yacc). El analizador identifica y clasifica tokens del código Ruby, generando logs detallados del análisis.

## 🔧 Requisitos

- Python
- PLY (Python Lex-Yacc)

## 📦 Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd Proyecto1_Ruby_G12
```

2. Instalar dependencias:
```bash
pip install ply
```

## 🚀 Uso

Para ejecutar el analizador léxico:

```bash
python src/lexico.py <archivo_ruby> <usuario_git>
```
Para ejecutar el analizador sintáctico:

```bash
python src/sintactico.py <archivo_ruby> <usuario_git>
```

### Ejemplos:

```bash
# Analizar Algorithm1 con usuario aszurita
python src/lexico.py Algorithms/Algorithm1_AngeloZurita.rb aszurita

# Analizar Algorithm2 con usuario dquishpe
python src/lexico.py Algorithms/Algorithm2_DhamarQuishpe.rb dquishpe

# Analizar Algorithm3 con usuario JoseM0lina
python src/lexico.py Algorithms/Algorithm3_JoseMarin.rb JoseM0lina

# Analizar Algorithm1 con Errores con usuario dquishpe
python src/sintactico.py Algorithms/Algorithm3_DhamarQuishpe_conErrores.rb dquishpe
```

## 📂 Estructura del Proyecto

```
Proyecto1_Ruby_G12/
├── src/
│   └── lexico.py           # Analizador léxico principal
│   └── sintactico.py           # Analizador sintáctico principal
├── Algorithms/
│   ├── Algorithm1_AngeloZurita.rb
│   ├── Algorithm2_DhamarQuishpe.rb
│   └── Algorithm3_JoseMarin.rb
│   ├── Algorithm1_AngeloZurita_conErrores.rb
│   ├── Algorithm2_DhamarQuishpe_conErrores.rb
│   └── Algorithm3_JoseMarin_conErrores.rb
├── logs/                    # Logs generados automáticamente
└── README.md
```

## 🎯 Tokens Reconocidos

El analizador reconoce los siguientes tipos de tokens:

### Variables y Constantes
- Variables locales: `nombre`, `edad`, `contador`
- Variables globales: `$contador`, `$total`
- Variables de instancia: `@nombre`, `@valor`
- Variables de clase: `@@contador`, `@@total`
- Constantes: `PI`, `DESCUENTO`

### Tipos de Datos
- Enteros: `42`, `100`
- Flotantes: `3.14`, `0.5`
- Strings: `"texto"`, `'texto'`
- Booleanos: `true`, `false`
- Nil: `nil`

### Operadores
- Aritméticos: `+`, `-`, `*`, `/`, `%`
- Asignación: `=`, `+=`, `-=`, `*=`, `/=`
- Comparación: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Lógicos: `&&`, `||`, `!`

### Palabras Reservadas
`if`, `else`, `elsif`, `while`, `for`, `until`, `def`, `return`, `end`, `class`, `module`, `break`, `next`, `redo`, `puts`, `print`, `gets`, `require`, `then`, `do`, `in`

### Delimitadores
`(`, `)`, `{`, `}`, `[`, `]`, `,`, `;`, `:`, `.`, `=>`

### Comentarios
- Línea: `# comentario`
- Multilínea: `=begin ... =end`

## 📊 Salida

El programa genera:
1. **Salida en consola**: Tabla formateada con todos los tokens encontrados
2. **Archivo log**: Guardado en `logs/` con formato `lexico-{usuario}-{fecha}.txt` o `sintactico-{usuario}-{fecha}.txt`

Cada log contiene respectivamente:
- Información del análisis (usuario, fecha, archivo)
- Lista completa de tokens con tipo, valor, línea y posición
- Resumen de errores (si los hay)
- Total de tokens reconocidos
- Total de construcciones
- Total de errores sintácticos

## 📝 Ejemplo de Salida (Analizador léxico)

```
====================================================================================================
ANALIZADOR LÉXICO PARA RUBY
====================================================================================================

Usuario: aszurita
Fecha: 02/11/2025 23:12:39
Archivo analizado: Algorithms/Algorithm1_AngeloZurita.rb

TOKENS RECONOCIDOS:
----------------------------------------------------------------------------------------------------
Tipo                      Valor                          Línea      Posición  
----------------------------------------------------------------------------------------------------
VARIABLE_LOCAL            nombre                         5          71        
ASIGNACION                =                              5          78        
STRING                    Juan                           5          80        
...
----------------------------------------------------------------------------------------------------
Total de tokens: 131

 ANÁLISIS COMPLETADO SIN ERRORES
====================================================================================================
```
## 📝 Ejemplo de Salida (Analizador sintáctico)

```
====================================================================================================
ANALIZADOR SINTÁCTICO PARA RUBY
====================================================================================================

Usuario: dquishpe
Fecha: 10/11/2025 22:51:03
Archivo analizado: Algorithms/Algorithm3_DhamarQuishpe_conErrores.rb
====================================================================================================

[OK] ANÁLISIS SINTÁCTICO EXITOSO

ESTRUCTURA DEL PROGRAMA:
----------------------------------------------------------------------------------------------------
('programa', ['# END sobrante'])
----------------------------------------------------------------------------------------------------

CONSTRUCCIONES SINTÁCTICAS RECONOCIDAS:
----------------------------------------------------------------------------------------------------
1. Operación aritmética: *
2. Operación aritmética: +
...
----------------------------------------------------------------------------------------------------
Total de construcciones: 16

ERRORES SINTÁCTICOS ENCONTRADOS:
----------------------------------------------------------------------------------------------------
1. Error sintáctico en línea 73: Token inesperado '=' (tipo: ASIGNACION)
2. Error sintáctico en línea 74: Token inesperado 'z' (tipo: VARIABLE_LOCAL)
3. Error sintáctico en línea 76: Token inesperado '=' (tipo: ASIGNACION)
...
----------------------------------------------------------------------------------------------------
Total de errores: 15


[ERROR] ANÁLISIS COMPLETADO CON ERRORES SINTÁCTICOS

====================================================================================================

```
