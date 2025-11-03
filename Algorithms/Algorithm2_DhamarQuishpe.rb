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
# Resultado final
# ===============================================
puts "Prueba completada con éxito"
