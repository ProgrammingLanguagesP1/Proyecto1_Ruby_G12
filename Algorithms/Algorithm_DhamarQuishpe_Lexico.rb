# Algoritmo 2
# Tester: Dhamar Quishpe (@dquishpe)

# ===============================================
# Ejemplo de comentarios
# ===============================================

# Esto es un comentario de una sola línea

=begin
Este es un comentario
multilínea en Ruby.
Debe ser reconocido por el lexer
como COMENTARIO_MULTILINEA.
=end

# ===============================================
# Ejemplo de operadores lógicos
# ===============================================

activo = true
autorizado = false

# Operadores lógicos
resultado1 = activo && autorizado
resultado2 = activo || autorizado
resultado3 = !activo

# Combinación de expresiones lógicas
if (activo && !autorizado) || (autorizado && !activo)
  puts "Condición lógica compuesta evaluada"
end

# ===============================================
# Ejemplo de delimitadores
# ===============================================

# Paréntesis, llaves y corchetes
numeros = [1, 2, 3, 4]
persona = { nombre: "Ana", edad: 22 }
suma = (10 + 5) * (3 - 1)

# Uso de coma, punto y punto y coma
puts "Números:", numeros
puts "Nombre: #{persona[:nombre]}", "Edad: #{persona[:edad]}";

# Flecha (=>) en hash estilo antiguo
datos = { "pais" => "Ecuador", "ciudad" => "Guayaquil" }

# Dos puntos en símbolos y pares clave-valor
coordenadas = { x: 10, y: 20 }

# ===============================================
# Ejemplo de operadores aritméticos y de comparación
# ===============================================

a = 15
b = 4
PI = 3.1416
resultado_arit = (a + b) * 2 - (a / b) % 2

mayor = a > b
igual = a == b
diferente = a != b
menor_igual = b <= a

# Operadores combinados
a += 1
b *= 2
a -= 3
b /= 2

# ===============================================
# Ejemplo de variables globales, de clase e instancia
# ===============================================

$contador_global = 10
@@total = 5
@usuario = "Dhamar"

# ===============================================
# Ejemplo de cadenas, constantes y símbolos
# ===============================================

MENSAJE_BIENVENIDA = "Bienvenida al sistema Ruby"
saludo = "Hola #{persona[:nombre]}, tu edad es #{persona[:edad]}"
simbolo = :identificador
puts MENSAJE_BIENVENIDA
puts saludo

# ===============================================
# Ejemplo de estructuras de control
# ===============================================

if a > b then
  puts "a es mayor que b"
elsif a == b
  puts "a es igual a b"
else
  puts "a es menor que b"
end

# Bucle while
i = 0
while i < 3 do
  puts "Iteración #{i}"
  i += 1
end

# Bucle for con rango
for j in 1..5 do
  print j, " "
end
puts "\nFin del bucle"

# ===============================================
# Resultado final
# ===============================================
puts "Prueba completada con éxito"
