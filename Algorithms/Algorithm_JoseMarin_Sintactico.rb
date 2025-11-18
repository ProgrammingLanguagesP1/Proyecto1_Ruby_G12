# ============================================================================
# ALGORITMO 2 - TEST DE ERRORES SINTÁCTICOS
# Tester: Jose Marin (@JoseM0lina)
# Descripción: Algoritmo diseñado para probar reglas sintácticas adicionales 
#              complementando Algorithm1
# ============================================================================

# Error 1: Operador de asignación compuesta incompleto
x += 

# Error 2: Asignación múltiple sin valores
a, b, c = 

# Error 3: Asignación con operador compuesto mal formado
y =+ 10

# Error 4: División asignación sin operando
total /= 

# Error 5: Multiplicación asignación con operador adicional
contador *= * 2

# Error 6: UNTIL sin END
until contador > 100
  contador += 1

# Error 7: UNTIL sin condición
until
  puts "Loop infinito"
end

# Error 8: UNTIL con DO pero sin END
until x < 0 do
  x -= 1

# Error 9: Rango inclusivo incompleto (falta valor final)
for i in 1..
  puts i
end

# Error 10: Rango exclusivo mal formado
rango = 5...

# Error 11: Rango con operadores inválidos
numeros = 1....10

# Error 12: FOR con rango sin valor inicial
for x in ..100 do
  puts x
end

# Error 13: MODULE sin nombre
module
  def metodo_modulo
    puts "test"
  end
end

# Error 14: MODULE sin END
module MiModulo
  def utilidad
    return true
  end

# Error 15: MODULE con nombre en minúscula (variable local en vez de constante)
module mi_modulo
  def helper
    puts "ayuda"
  end
end

# Error 16: RETURN con expresión incompleta
def calcular
  return x +
end

# Error 17: NEXT con expresión inválida
for i in 1..10
  next if i >
end

# Error 18: REDO sin estar en un ciclo
redo

# Error 19: ELSIF sin condición
if x > 5
  puts "Mayor que 5"
elsif
  puts "Error"
end

# Error 20: ELSIF sin THEN ni sentencias
if x > 10
  puts "Diez"
elsif x > 5 then
end

# Error 21: Múltiples ELSIF con último sin condición
if x < 0
  puts "Negativo"
elsif x == 0
  puts "Cero"
elsif
  puts "Error"
end

# Error 22: Llamada a función con coma adicional al final
resultado = sumar(1, 2, 3,)

# Error 23: Llamada a función con operador en vez de argumento
valor = multiplicar(10, *, 5)

# Error 24: Método de clase sin el punto
resultado = MiClase metodo()

# Error 25: Arreglo con corchetes desbalanceados
matriz = [[1, 2, 3], [4, 5, 6]

# Error 26: Arreglo con coma doble
lista = [1, 2,, 3, 4]

# Error 27: Hash con flecha pero sin valor
config = { nombre: "Juan", edad => }

# Error 28: Hash con clave duplicada pero sintaxis rota
datos = { x: 1, y: 2, x: }

# Error 29: Hash con mezcla incorrecta de sintaxis
opciones = { "a" => 1, b:, "c" => 3 }

# Error 30: AND sin operando derecho
if x > 5 and
  puts "Error"
end

# Error 31: OR con paréntesis sin cerrar
if (a > b or c < d
  puts "Comparación"
end

# Error 32: NOT sin expresión
resultado = not

# Error 33: Operadores lógicos consecutivos
if x > 5 and or y < 10
  puts "Error"
end