# Algoritmo 3
# Tester: Jose Marín (@JoseM0lina)

# Variables de instancia
@nombre_instancia = "ObjetoDemo"
@valor_interno = 100
@estado_activo = true
@precio_base = 299.99

# Variables de clase
@@contador_clase = 0
@@total_instancias = 50
@@version_sistema = 2.5
@@limite_maximo = 1000

# Estructura until
contador_until = 0
until contador_until >= 5
  puts "Iteración: #{contador_until}"
  contador_until += 1
end

# Definición de funciones
def calcular_precio(base, cantidad)
  subtotal = base * cantidad
  return subtotal
end

# Definición de clases
class Producto
  def initialize(nombre, precio)
    @nombre = nombre
    @precio = precio
    @@contador_clase += 1
  end
  
  def calcular_total(cantidad)
    total = @precio * cantidad
    return total
  end
end

# Definición de módulos
module Matematicas
  PI = 3.14159
  
  def self.area_circulo(radio)
    area = PI * radio * radio
    return area
  end
end

# Valor nil
valor_nulo = nil
dato_vacio = nil

if valor_nulo == nil
  puts "Valor nulo detectado"
end

# Control de flujo: break
for i in 1..10
  if i == 6
    break
  end
  puts "Break: #{i}"
end

# Control de flujo: next
for i in 1..8
  if i == 4
    next
  end
  puts "Next: #{i}"
end

# Control de flujo: redo
contador_redo = 0
for i in 1..3
  contador_redo += 1
  if contador_redo < 2
    redo
  end
  puts "Redo: #{i}"
end

# Uso de then
edad_test = 25
if edad_test >= 18 then
  puts "Mayor de edad"
end

# Uso de do en for
for num in 1..3 do
  puts "Número: #{num}"
end

# Uso de do en while
indice = 0
while indice < 3 do
  puts "Índice: #{indice}"
  indice += 1
end

# Entrada con gets
puts "Ingrese su nombre:"
nombre_usuario = gets

# Importar módulos con require
require 'date'
require 'json'

# Strings con caracteres especiales
texto_escape = "Línea 1\nLínea 2"
texto_tab = "Columna1\tColumna2"
texto_comilla = "Él dijo: \"Hola\""
texto_apostrofe = 'It\'s working'

# Llamadas a funciones
precio = calcular_precio(100.0, 5)
descuento = aplicar_descuento(500.0, 0.10)
validacion = es_valido(42)

# Llamadas a módulos
area = Matematicas.area_circulo(10.0)
mayor_edad = Utilidades.validar_edad(20)

# Combinaciones con variables de instancia y clase
resultado = @valor_interno + @@contador_clase

puts "Prueba completada"