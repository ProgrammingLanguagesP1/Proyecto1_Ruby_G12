# ============================================================================
# ALGORITMO 2 - TEST DE ERRORES SINTÁCTICOS (adaptado a la gramática del parser)
# Tester: Dhamar Quishpe (@dquishpe)
# Descripción: Casos diseñados para que el parser detecte errores.
# ============================================================================

# --- ASIGNACIÓN Y EXPRESIONES ---
x = 10 +
y = (5 * 3
z = 2 ** 3   # operador no permitido en esta gramática
resultado = x + y *
valor = (10 + 5)) # paréntesis extra
numero = 7 / (2 - ) # expresión incompleta

# --- STRINGS Y CONCATENACIONES ---
mensaje = "Hola #{nombre"   # falta cierre de interpolación
texto = 'Hola #{nombre}'    # uso incorrecto de comillas simples
cadena = "Esto es un texto sin cerrar

# --- ESTRUCTURA IF ---
if x > 5
  puts "Mayor que cinco"
elsif x < 2
  puts "Menor que dos"
else
  puts "Otro valor"
# falta el END aquí para provocar error

# --- CONDICIONES LÓGICAS ---
if (x &&) || (y)
  puts "condición mal formada"
end

if x > 0 and or y < 5
  puts "doble operador lógico"
end

# --- WHILE ---
while x < 10 do
  x += 1
  puts x
endd   # palabra mal escrita (error leve)

while do
  puts "falta condición"
end

# --- UNTIL ---
until contador > 
  puts "error en condición"
end

# --- FUNCIONES ---
def suma(a, b,)
  return a + b
end

def sin_end(a)
  puts a + 2
# falta el END

def sin_nombre()
  puts "no tiene identificador"
end

# --- CLASES ---
class Persona
  def initialize(nombre)
    @nombre = nombre
  end
  def saludar()
    puts "Hola, #{@nombre}"
  end
# falta END de clase

class miClase
  puts "nombre inválido (no constante)"
end

# --- MÓDULO ---
module Herramientas
  def self.ayuda
    puts "módulo sin END"
# falta END del módulo

# --- HASHES Y ARREGLOS ---
datos = {nombre: "Ana", edad => 22}   # operador => mal ubicado
valores = [1, 2, 3, , 5]               # coma doble
pares = { :ok => 1, :fail: => 2 }      # símbolo mal formado
lista = [10, (20 + ), 30]              # expresión incompleta

# --- RANGOS Y FOR ---
for i in 1..
  puts i
end

for in 1..5
  puts "sin variable"
end

for x in (1 + 2)
  puts x
# falta END

# --- RETURN Y BLOQUES ---
return + 5  # fuera de función

items.each do |x
  puts x
end

# --- REQUIRES Y OTROS ---
require archivo_sin_comillas
include sin_nombre

# --- FIN EXTRA ---
puts "fin del test"
end  # END sobrante
