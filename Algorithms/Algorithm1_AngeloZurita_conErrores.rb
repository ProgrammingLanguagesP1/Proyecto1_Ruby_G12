# ============================================================================
# ALGORITMO 1 - TEST DE ERRORES SINTÁCTICOS
# Tester: Angelo Zurita (@aszurita)
# Descripción: Algoritmo diseñado para probar el manejo de errores del
#              analizador sintáctico
# ============================================================================

# Error 1: IF sin END
if x > 10
  puts "Mayor que 10"

# Error 2: Paréntesis sin cerrar en llamada a función
resultado = calcular(5, 10

# Error 3: Operador inválido al inicio de línea
+ = 5

# Error 4: FOR con sintaxis incorrecta (falta IN)
for i 1..10
  puts i
end

# Error 5: Asignación con operador incorrecto
x =< 5

# Error 6: DEF sin END
def mi_funcion
  puts "Hola"

# Error 7: Expresión aritmética incompleta
y = 10 +

# Error 8: Hash con sintaxis incorrecta (falta clave)
hash = { a: 1, : 2 }

# Error 9: WHILE sin condición
while
  puts "Loop"
end

# Error 10: Arreglo sin cerrar corchete
numeros = [1, 2, 3, 4

# Error 11: Comparación incompleta en condicional
if x >
  puts "Error"
end

# Error 12: Clase sin nombre
class
  def metodo
    puts "test"
  end
end

# Error 13: Operadores consecutivos inválidos
z = 10 ++ 5

# Error 14: ELSIF sin IF previo
elsif x > 5
  puts "Mayor que 5"

# Error 15: END sin estructura correspondiente
puts "Hola Mundo"
end

# Error 16: Llamada a función con paréntesis sin cerrar
funcion(1, 2, 3

# Error 17: String sin cerrar comillas
mensaje = "Esto es un error

# Error 18: Operador lógico sin operando derecho
if x > 5 and
  puts "Error"
end

# Error 19: FOR sin palabra clave IN
for contador 1..100 do
  puts contador
end

# Error 20: Return con expresión inválida
def test
  return + 5
end
