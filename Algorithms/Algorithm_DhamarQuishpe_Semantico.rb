# ==========================================
# ALGORITMO 2 - TEST DE ERRORES SEMÁNTICOS
# Tester: Dhamar Quishpe (@dquishpe)
# Descripción: Casos diseñados para que el analizador semántico detecte errores.
# ==========================================

# Constantes matemáticas (CORRECTO)
PI = 3.14159
E = 2.71828
GRAVEDAD = 9.8
VELOCIDAD_LUZ = 300000

# Variables globales de configuración (CORRECTO)
$debug_mode = true
$contador_operaciones = 0
$precision = 2

# ==========================================
# ERROR 1: Constante modificada 
# ==========================================
PI = 3.14

# Función para calcular área de círculo (CORRECTO)
def area_circulo(radio)
  area = PI * radio * radio
  return area
end

# Función para calcular volumen de esfera (CORRECTO)
def volumen_esfera(radio)
  volumen = 4 * PI * radio * radio * radio / 3
  return volumen
end

# Inicialización de variables (CORRECTO)
radio1 = 5
radio2 = 10
radio3 = 15

# Cálculos de áreas (CORRECTO)
area1 = area_circulo(radio1)
area2 = area_circulo(radio2)
area3 = area_circulo(radio3)

puts area1
puts area2
puts area3

# ==========================================
# ERROR 2: Variable no declarada 
# ==========================================
def mostrar_resultados
  puts variable_inexistente
  return 0
end

# Cálculos de volúmenes (CORRECTO)
vol1 = volumen_esfera(radio1)
vol2 = volumen_esfera(radio2)
vol3 = volumen_esfera(radio3)

# ==========================================
# ERROR 3: Operador incompatible 
# ==========================================
texto_area = "El área es: "
resultado_invalido = texto_area - 100

# Función para sumar arreglo (CORRECTO)
def sumar_elementos(arr)
  total = 0
  for elemento in arr do
    total = total + elemento
  end
  return total
end

# Crear arreglos de datos (CORRECTO)
numeros = [10, 20, 30, 40, 50]
temperaturas = [18, 22, 25, 19, 21]
distancias = [100, 250, 175, 300, 425]

# Procesar arreglos (CORRECTO)
suma_numeros = sumar_elementos(numeros)
suma_temperaturas = sumar_elementos(temperaturas)
suma_distancias = sumar_elementos(distancias)

puts suma_numeros
puts suma_temperaturas
puts suma_distancias

# ==========================================
# ERROR 4: Conversión implícita inválida 
# ==========================================
mensaje = "Total: " + suma_numeros

# Calcular promedios (CORRECTO)
promedio_numeros = suma_numeros / 5
promedio_temperaturas = suma_temperaturas / 5
promedio_distancias = suma_distancias / 5

# ==========================================
# ERROR 5: Cambio de tipo 
# ==========================================
promedio_numeros = "cincuenta"

# Función para encontrar máximo (CORRECTO)
def encontrar_maximo(a, b, c)
  max = a
  if b > max then
    max = b
  end
  if c > max then
    max = c
  end
  return max
end

# Buscar valores máximos (CORRECTO)
max_area = encontrar_maximo(area1, area2, area3)
max_volumen = encontrar_maximo(vol1, vol2, vol3)

puts max_area
puts max_volumen

# ==========================================
# ERROR 6: Break fuera de loop 
# ==========================================
def procesar_datos
  valor = 100
  break
  return valor
end

# Operaciones con potencias (CORRECTO)
base = 2
exponente = 3
resultado_potencia = 1

for i in 1..exponente do
  resultado_potencia = resultado_potencia * base
end

puts resultado_potencia

# Crear matriz de datos (CORRECTO)
matriz = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
]

# ==========================================
# ERROR 7: Condición no booleana 
# ==========================================
if numeros then
  puts "Arreglo existe"
end

# Procesar matriz (CORRECTO)
suma_matriz = 0
for fila in matriz do
  for elemento in fila do
    suma_matriz = suma_matriz + elemento
  end
end

puts suma_matriz

# ==========================================
# ERROR 8: Return fuera de función 
# ==========================================
return suma_matriz

# Función para calcular factorial (CORRECTO)
def factorial(n)
  if n <= 1 then
    return 1
  else
    resultado = 1
    contador = 2
    while contador <= n do
      resultado = resultado * contador
      contador = contador + 1
    end
    return resultado
  end
end

# Calcular factoriales (CORRECTO)
fact5 = factorial(5)
fact7 = factorial(7)
fact10 = factorial(10)

puts fact5
puts fact7
puts fact10

# ==========================================
# ERROR 9: Asignación a palabra reservada 
# ==========================================
if = 25

# Hash con configuraciones (CORRECTO)
configuracion = {
  modo: "activo",
  nivel: 5,
  habilitado: true
}

# Función de conversión de temperatura (CORRECTO)
def celsius_a_fahrenheit(celsius)
  fahrenheit = celsius * 9 / 5 + 32
  return fahrenheit
end

# Función de conversión inversa (CORRECTO)
def fahrenheit_a_celsius(fahrenheit)
  celsius = fahrenheit - 32 * 5 / 9
  return celsius
end

# Conversiones de temperatura (CORRECTO)
temp_celsius = 25
temp_fahrenheit = celsius_a_fahrenheit(temp_celsius)
temp_celsius_nuevamente = fahrenheit_a_celsius(temp_fahrenheit)

puts temp_fahrenheit
puts temp_celsius_nuevamente

# ==========================================
# ERROR 10: Operador incompatible string * float 
# ==========================================
cadena = "Hola"
repeticiones = cadena * 3.5

# Crear secuencia de Fibonacci (CORRECTO)
fibonacci = [0, 1]
for i in 2..10 do
  siguiente = fibonacci[0] + fibonacci[1]
  fibonacci = fibonacci + [siguiente]
end

# Cálculo de velocidad (CORRECTO)
distancia = 150
tiempo = 3
velocidad = distancia / tiempo

puts velocidad

# Cálculo de aceleración (CORRECTO)
velocidad_inicial = 0
velocidad_final = 50
tiempo_transcurrido = 10
aceleracion = velocidad_final - velocidad_inicial / tiempo_transcurrido

puts aceleracion

# Bucle until para contador (CORRECTO)
contador = 0
until contador >= 10 do
  contador = contador + 1
  if contador == 5 then
    puts "Mitad del proceso"
  end
end

# Función para verificar par o impar (CORRECTO)
def es_par(numero)
  resto = numero % 2
  if resto == 0 then
    return true
  else
    return false
  end
end

# Verificar números (CORRECTO)
numero1 = 42
numero2 = 37
numero3 = 100

resultado1 = es_par(numero1)
resultado2 = es_par(numero2)
resultado3 = es_par(numero3)

puts resultado1
puts resultado2
puts resultado3

# Operaciones con cadenas (CORRECTO)
texto1 = "Procesamiento"
texto2 = "de"
texto3 = "Datos"

# Concatenación correcta
texto_completo = texto1 + " " + texto2 + " " + texto3
puts texto_completo

# Cálculo de energía cinética (CORRECTO)
masa = 10
velocidad_objeto = 20
energia_cinetica = masa * velocidad_objeto * velocidad_objeto / 2

puts energia_cinetica

# Cálculo de energía potencial (CORRECTO)
altura = 50
energia_potencial = masa * GRAVEDAD * altura

puts energia_potencial

# Resumen final (CORRECTO)
puts "Total de operaciones realizadas"
puts "Areas calculadas: 3"
puts "Volumenes calculados: 3"
puts "Conversiones: 2"
puts "Factoriales: 3"

# Fin del programa