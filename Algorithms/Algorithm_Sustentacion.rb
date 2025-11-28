# ============================================
# ALGORITMO DE PRUEBA COMPLETO
# Sistema de Gestión de Estudiantes
# Grupo 12 - Lenguajes de Programación
# ============================================

# CONSTANTES DEL SISTEMA
MAX_ESTUDIANTES = 100
NOTA_MINIMA = 0
NOTA_MAXIMA = 20
APROBACION = 14

# Variables globales
$total_estudiantes = 0
$promedio_general = 0

# ============================================
# CLASE ESTUDIANTE
# ============================================
class Estudiante
  
  def inicializar(nombre, edad, carrera)
    @nombre = nombre
    @edad = edad
    @carrera = carrera
    @nota1 = 0
    @nota2 = 0
    @nota3 = 0
    @promedio = 0
  end
  
  def asignar_notas(n1, n2, n3)
    @nota1 = n1
    @nota2 = n2
    @nota3 = n3
    
    suma = @nota1 + @nota2 + @nota3
    @promedio = suma / 3
    
    return @promedio
  end
  
  def obtener_estado()
    if @promedio >= APROBACION
      return true
    else
      return false
    end
  end
  
  def mostrar_info()
    puts "Nombre: "
    puts @nombre
    puts "Edad: "
    puts @edad
    puts "Carrera: "
    puts @carrera
    puts "Promedio: "
    puts @promedio
  end
  
end

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def validar_edad(edad)
  if edad >= 16 and edad <= 100
    return true
  else
    return false
  end
end

def validar_nota(nota)
  if nota >= NOTA_MINIMA and nota <= NOTA_MAXIMA
    return true
  else
    puts "Error: Nota fuera de rango"
    return false
  end
end

def calcular_promedio(n1, n2, n3)
  suma = n1 + n2 + n3
  promedio = suma / 3
  return promedio
end

def clasificar_promedio(promedio)
  if promedio >= 18
    return "EXCELENTE"
  elsif promedio >= 16
    return "MUY BUENO"
  elsif promedio >= 14
    return "BUENO"
  elsif promedio >= 10
    return "REGULAR"
  else
    return "INSUFICIENTE"
  end
end

def factorial(n)
  if n <= 1
    return 1
  else
    return n * factorial(n - 1)
  end
end

def suma_rango(inicio, fin)
  suma = 0
  for i in inicio..fin
    suma = suma + i
  end
  return suma
end

def buscar_aprobados(notas)
  aprobados = 0
  contador = 0
  
  while contador < 10
    if notas[contador] >= APROBACION
      aprobados = aprobados + 1
    end
    contador = contador + 1
  end
  
  return aprobados
end

def procesar_notas(notas)
  suma = 0
  mayor = 0
  menor = 20
  
  i = 0
  until i >= 10
    nota_actual = notas[i]
    suma = suma + nota_actual
    
    if nota_actual > mayor
      mayor = nota_actual
    end
    
    if nota_actual < menor
      menor = nota_actual
    end
    
    i = i + 1
  end
  
  promedio = suma / 10
  
  return promedio
end

# ============================================
# PROGRAMA PRINCIPAL
# ============================================

puts "============================================"
puts "SISTEMA DE GESTION DE ESTUDIANTES"
puts "============================================"

# Crear estudiantes
estudiante1 = Estudiante
estudiante2 = Estudiante
estudiante3 = Estudiante
estudiante4 = Estudiante
estudiante5 = Estudiante

# Datos del estudiante 1
nombre1 = "Juan Perez"
edad1 = 20
carrera1 = "Computacion"

if validar_edad(edad1)
  puts "Registrando estudiante 1..."
  $total_estudiantes = $total_estudiantes + 1
end

# Asignar notas al estudiante 1
nota1_est1 = 18
nota2_est1 = 17
nota3_est1 = 19

if validar_nota(nota1_est1) and validar_nota(nota2_est1)
  if validar_nota(nota3_est1)
    promedio1 = calcular_promedio(nota1_est1, nota2_est1, nota3_est1)
    clasificacion1 = clasificar_promedio(promedio1)
    
    puts "Promedio: "
    puts promedio1
    puts "Clasificacion: "
    puts clasificacion1
  end
end

# Datos del estudiante 2
nombre2 = "Maria Garcia"
edad2 = 21
carrera2 = "Electronica"

if validar_edad(edad2)
  puts "Registrando estudiante 2..."
  $total_estudiantes = $total_estudiantes + 1
end

# Asignar notas al estudiante 2
nota1_est2 = 16
nota2_est2 = 15
nota3_est2 = 17

if validar_nota(nota1_est2) and validar_nota(nota2_est2)
  if validar_nota(nota3_est2)
    promedio2 = calcular_promedio(nota1_est2, nota2_est2, nota3_est2)
    clasificacion2 = clasificar_promedio(promedio2)
    
    puts "Promedio: "
    puts promedio2
    puts "Clasificacion: "
    puts clasificacion2
  end
end

# Datos del estudiante 3
nombre3 = "Carlos Lopez"
edad3 = 19
carrera3 = "Mecanica"

if validar_edad(edad3)
  puts "Registrando estudiante 3..."
  $total_estudiantes = $total_estudiantes + 1
end

# Asignar notas al estudiante 3
nota1_est3 = 14
nota2_est3 = 13
nota3_est3 = 15

if validar_nota(nota1_est3) and validar_nota(nota2_est3)
  if validar_nota(nota3_est3)
    promedio3 = calcular_promedio(nota1_est3, nota2_est3, nota3_est3)
    clasificacion3 = clasificar_promedio(promedio3)
    
    puts "Promedio: "
    puts promedio3
    puts "Clasificacion: "
    puts clasificacion3
  end
end

# Datos del estudiante 4
nombre4 = "Ana Martinez"
edad4 = 22
carrera4 = "Civil"

if validar_edad(edad4)
  puts "Registrando estudiante 4..."
  $total_estudiantes = $total_estudiantes + 1
end

# Asignar notas al estudiante 4
nota1_est4 = 12
nota2_est4 = 11
nota3_est4 = 13

if validar_nota(nota1_est4) and validar_nota(nota2_est4)
  if validar_nota(nota3_est4)
    promedio4 = calcular_promedio(nota1_est4, nota2_est4, nota3_est4)
    clasificacion4 = clasificar_promedio(promedio4)
    
    puts "Promedio: "
    puts promedio4
    puts "Clasificacion: "
    puts clasificacion4
  end
end

# Datos del estudiante 5
nombre5 = "Luis Rodriguez"
edad5 = 20
carrera5 = "Industrial"

if validar_edad(edad5)
  puts "Registrando estudiante 5..."
  $total_estudiantes = $total_estudiantes + 1
end

# Asignar notas al estudiante 5
nota1_est5 = 15
nota2_est5 = 14
nota3_est5 = 16

if validar_nota(nota1_est5) and validar_nota(nota2_est5)
  if validar_nota(nota3_est5)
    promedio5 = calcular_promedio(nota1_est5, nota2_est5, nota3_est5)
    clasificacion5 = clasificar_promedio(promedio5)
    
    puts "Promedio: "
    puts promedio5
    puts "Clasificacion: "
    puts clasificacion5
  end
end

# ============================================
# ESTADISTICAS GENERALES
# ============================================

puts "============================================"
puts "ESTADISTICAS GENERALES"
puts "============================================"

# Calcular promedio general
suma_promedios = promedio1 + promedio2 + promedio3
suma_promedios = suma_promedios + promedio4 + promedio5
$promedio_general = suma_promedios / $total_estudiantes

puts "Total de estudiantes: "
puts $total_estudiantes
puts "Promedio general: "
puts $promedio_general

# Contar aprobados
aprobados = 0

if promedio1 >= APROBACION
  aprobados = aprobados + 1
end

if promedio2 >= APROBACION
  aprobados = aprobados + 1
end

if promedio3 >= APROBACION
  aprobados = aprobados + 1
end

if promedio4 >= APROBACION
  aprobados = aprobados + 1
end

if promedio5 >= APROBACION
  aprobados = aprobados + 1
end

puts "Estudiantes aprobados: "
puts aprobados

reprobados = $total_estudiantes - aprobados
puts "Estudiantes reprobados: "
puts reprobados

# ============================================
# PRUEBAS DE BUCLES
# ============================================

puts "============================================"
puts "PRUEBAS DE BUCLES"
puts "============================================"

# Bucle while
puts "Conteo con WHILE:"
contador = 1
while contador <= 5
  puts contador
  contador = contador + 1
end

# Bucle for
puts "Conteo con FOR:"
for i in 1..10
  puts i
end

# Bucle until
puts "Conteo descendente con UNTIL:"
numero = 5
until numero <= 0
  puts numero
  numero = numero - 1
end

# ============================================
# OPERACIONES MATEMATICAS
# ============================================

puts "============================================"
puts "OPERACIONES MATEMATICAS"
puts "============================================"

# Variables para operaciones
a = 100
b = 25
c = 5

# Suma
resultado_suma = a + b
puts "Suma: "
puts resultado_suma

# Resta
resultado_resta = a - b
puts "Resta: "
puts resultado_resta

# Multiplicación
resultado_mult = b * c
puts "Multiplicacion: "
puts resultado_mult

# División
resultado_div = a / c
puts "Division: "
puts resultado_div

# Módulo
resultado_mod = a % 30
puts "Modulo: "
puts resultado_mod

# Operaciones combinadas
resultado_combinado = a + b * c - 10
puts "Operacion combinada: "
puts resultado_combinado

# ============================================
# PRUEBAS CON ARREGLOS
# ============================================

puts "============================================"
puts "PRUEBAS CON ARREGLOS"
puts "============================================"

# Crear arreglo de notas
notas_parcial = [18, 16, 14, 12, 15, 17, 13, 19, 11, 16]

puts "Arreglo de notas creado"

# Procesar notas
promedio_parcial = procesar_notas(notas_parcial)
puts "Promedio del parcial: "
puts promedio_parcial

# Contar aprobados
total_aprobados = buscar_aprobados(notas_parcial)
puts "Aprobados en parcial: "
puts total_aprobados

# ============================================
# OPERACIONES LOGICAS
# ============================================

puts "============================================"
puts "OPERACIONES LOGICAS"
puts "============================================"

# Variables booleanas
tiene_beca = true
asistencia_completa = true
promedio_alto = false

# AND
if tiene_beca and asistencia_completa
  puts "Estudiante cumple requisitos"
end

# OR
if promedio_alto or tiene_beca
  puts "Estudiante tiene beneficio"
end

# NOT
suspenso = false
if not suspenso
  puts "Estudiante en buen estado"
end

# Combinaciones
if tiene_beca and asistencia_completa and not suspenso
  puts "Estudiante destacado"
end

# ============================================
# FUNCIONES RECURSIVAS
# ============================================

puts "============================================"
puts "FUNCIONES RECURSIVAS"
puts "============================================"

# Factorial de 5
numero_fact = 5
resultado_fact = factorial(numero_fact)
puts "Factorial de 5: "
puts resultado_fact

# Factorial de 7
numero_fact2 = 7
resultado_fact2 = factorial(numero_fact2)
puts "Factorial de 7: "
puts resultado_fact2

# ============================================
# PRUEBAS CON RANGOS
# ============================================

puts "============================================"
puts "PRUEBAS CON RANGOS"
puts "============================================"

# Suma de 1 a 10
suma_1_10 = suma_rango(1, 10)
puts "Suma de 1 a 10: "
puts suma_1_10

# Suma de 1 a 100
suma_1_100 = suma_rango(1, 100)
puts "Suma de 1 a 100: "
puts suma_1_100

# ============================================
# COMPARACIONES
# ============================================

puts "============================================"
puts "COMPARACIONES"
puts "============================================"

nota_test = 15
limite_bajo = 14
limite_alto = 18

# Mayor que
if nota_test > limite_bajo
  puts "Nota superior al limite bajo"
end

# Menor que
if nota_test < limite_alto
  puts "Nota inferior al limite alto"
end

# Igual
if nota_test == 15
  puts "Nota igual a 15"
end

# Diferente
if nota_test != 20
  puts "Nota diferente de 20"
end

# Mayor o igual
if nota_test >= 14
  puts "Nota mayor o igual a 14"
end

# Menor o igual
if nota_test <= 16
  puts "Nota menor o igual a 16"
end

# ============================================
# FINALIZACION
# ============================================

puts "============================================"
puts "SISTEMA FINALIZADO EXITOSAMENTE"
puts "============================================"
puts "Total de estudiantes procesados: "
puts $total_estudiantes
puts "Promedio general del curso: "
puts $promedio_general
puts "Estado del sistema: ACTIVO"
puts "============================================"