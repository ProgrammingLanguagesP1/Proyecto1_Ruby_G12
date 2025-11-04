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

### Ejemplos:

```bash
# Analizar Algorithm1 con usuario aszurita
python src/lexico.py Algorithms/Algorithm1_AngeloZurita.rb aszurita

# Analizar Algorithm2 con usuario dquishpe
python src/lexico.py Algorithms/Algorithm2_DhamarQuishpe.rb dquishpe

# Analizar Algorithm3 con usuario JoseM0lina
python src/lexico.py Algorithms/Algorithm3_JoseMarin.rb JoseM0lina
```

## 📂 Estructura del Proyecto

```
Proyecto1_Ruby_G12/
├── src/
│   └── lexico.py           # Analizador léxico principal
├── Algorithms/
│   ├── Algorithm1_AngeloZurita.rb
│   ├── Algorithm2_DhamarQuishpe.rb
│   └── Algorithm3_JoseMarin.rb
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
2. **Archivo log**: Guardado en `logs/` con formato `lexico-{usuario}-{fecha}.txt`

Cada log contiene:
- Información del análisis (usuario, fecha, archivo)
- Lista completa de tokens con tipo, valor, línea y posición
- Resumen de errores (si los hay)
- Total de tokens reconocidos

## 📝 Ejemplo de Salida

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
