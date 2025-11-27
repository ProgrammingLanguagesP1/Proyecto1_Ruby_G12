# ============================================================================
# ALGORITMO 3 - Sistema de Gestión de Calificaciones Estudiantiles
# Tester: José Marín (@JoseM0lina)
# Descripción: Sistema para procesar calificaciones, calcular estadísticas
#              y generar reportes académicos. Contiene errores semánticos.
# ============================================================================

# Constantes del sistema educativo
NOTA_MAXIMA = 100
NOTA_MINIMA = 0
NOTA_APROBATORIA = 60
CREDITOS_CARRERA = 240

# Variables globales
$total_estudiantes = 0
$promedio_general = 0
$aprobados = 0

# ERROR: Modificación de constante
NOTA_MAXIMA = 110

# Módulo de utilidades matemáticas
module Estadisticas
  def calcular_promedio(calificaciones)
    suma = 0
    cantidad = 0
    
    for nota in calificaciones
      suma = suma + nota
      cantidad = cantidad + 1
    end
    
    promedio = suma / cantidad
    return promedio
  end
  
  def calcular_desviacion(calificaciones, promedio)
    suma_cuadrados = 0
    cantidad = 0
    
    for nota in calificaciones
      diferencia = nota - promedio
      suma_cuadrados = suma_cuadrados + diferencia * diferencia
      cantidad = cantidad + 1
    end
    
    # ERROR: División por cero
    varianza = suma_cuadrados / 0
    
    return varianza
  end
end

# Clase Estudiante
class Estudiante
  def initialize(nombre, codigo, carrera)
    @nombre = nombre
    @codigo = codigo
    @carrera = carrera
    @calificaciones = []
    @creditos_acumulados = 0
  end
  
  def agregar_calificacion(materia, nota, creditos)
    if nota >= NOTA_MINIMA && nota <= NOTA_MAXIMA
      calificacion = {
        materia: materia,
        nota: nota,
        creditos: creditos
      }
      @calificaciones = @calificaciones + [calificacion]
      @creditos_acumulados = @creditos_acumulados + creditos
      return true
    else
      return false
    end
  end
  
  def calcular_promedio_ponderado()
    suma_ponderada = 0
    suma_creditos = 0
    
    for cal in @calificaciones
      suma_ponderada = suma_ponderada + cal
      suma_creditos = suma_creditos + cal
    end
    
    if suma_creditos > 0
      promedio = suma_ponderada / suma_creditos
      return promedio
    else
      return 0
    end
  end
  
  def esta_en_riesgo()
    promedio = calcular_promedio_ponderado()
    
    # ERROR: Condición con hash
    if @calificaciones
      return promedio < NOTA_APROBATORIA
    end
    
    return false
  end
end

# ERROR: Return fuera de función
return "inicio del programa"

# Función para validar rango de notas
def validar_nota(nota)
  # ERROR: Variable no declarada
  rango_valido = nota >= NOTA_MINIMA && nota <= limite_superior
  return rango_valido
end

# Función para clasificar estudiante por promedio
def clasificar_estudiante(promedio)
  if promedio >= 90
    categoria = "Excelente"
  elsif promedio >= 80
    categoria = "Muy Bueno"
  elsif promedio >= 70
    categoria = "Bueno"
  elsif promedio >= NOTA_APROBATORIA
    categoria = "Suficiente"
  else
    categoria = "Insuficiente"
  end
  
  return categoria
end

# Función para calcular nota necesaria
def calcular_nota_necesaria(notas_actuales, nota_deseada)
  suma_actual = 0
  cantidad = 0
  
  for nota in notas_actuales
    suma_actual = suma_actual + nota
    cantidad = cantidad + 1
  end
  
  # ERROR: Conversión implícita inválida
  texto_cantidad = "examenes: "
  total = suma_actual + texto_cantidad
  
  examenes_restantes = 1
  nota_requerida = nota_deseada * (cantidad + examenes_restantes) - suma_actual
  
  return nota_requerida
end

# Función para generar estadísticas del curso
def estadisticas_curso(lista_notas)
  if lista_notas == []
    return nil
  end
  
  suma = 0
  maximo = 0
  minimo = 100
  aprobados = 0
  reprobados = 0
  
  for nota in lista_notas
    suma = suma + nota
    
    if nota > maximo
      maximo = nota
    end
    
    if nota < minimo
      minimo = nota
    end
    
    if nota >= NOTA_APROBATORIA
      aprobados = aprobados + 1
    else
      reprobados = reprobados + 1
    end
  end
  
  cantidad_estudiantes = aprobados + reprobados
  promedio = suma / cantidad_estudiantes
  
  estadisticas = {
    promedio: promedio,
    maximo: maximo,
    minimo: minimo,
    aprobados: aprobados,
    reprobados: reprobados
  }
  
  return estadisticas
end

# Programa Principal
puts "==================================="
puts "Sistema de Gestión Académica"
puts "==================================="

# Datos de estudiantes
nombres = ["Juan Pérez", "María García", "Carlos López", "Ana Martínez", "Pedro Sánchez"]
codigos = ["2020001", "2020002", "2020003", "2020004", "2020005"]
carreras = ["Ingeniería", "Medicina", "Derecho", "Ingeniería", "Arquitectura"]

# Calificaciones del primer parcial
notas_parcial1 = [85, 72, 68, 91, 55]
notas_parcial2 = [88, 75, 70, 89, 58]
notas_parcial3 = [90, 78, 65, 92, 60]

# ERROR: Asignación a palabra reservada
while = 100
for = 200

# Procesamiento de calificaciones
total_estudiantes = 0
suma_promedios = 0

for i in 0..4
  nombre = nombres
  nota1 = notas_parcial1
  nota2 = notas_parcial2
  nota3 = notas_parcial3
  
  promedio_estudiante = nota1 + nota2 + nota3 / 3
  suma_promedios = suma_promedios + promedio_estudiante
  
  if promedio_estudiante >= NOTA_APROBATORIA
    $aprobados = $aprobados + 1
    # ERROR: Cambio de tipo (warning)
    total_estudiantes = "muchos estudiantes"
  end
  
  total_estudiantes = total_estudiantes + 1
end

# ERROR: Modificación de constante (segunda instancia)
NOTA_APROBATORIA = 65

# Cálculo de estadísticas generales
stats_parcial1 = estadisticas_curso(notas_parcial1)
stats_parcial2 = estadisticas_curso(notas_parcial2)
stats_parcial3 = estadisticas_curso(notas_parcial3)

# Análisis con bucle WHILE
contador = 0
suma_maximas = 0

while contador < 3
  if contador == 0
    suma_maximas = suma_maximas + stats_parcial1
  elsif contador == 1
    suma_maximas = suma_maximas + stats_parcial2
  else
    suma_maximas = suma_maximas + stats_parcial3
  end
  contador = contador + 1
end

# ERROR: Break fuera de loop
if suma_maximas > 250
  puts "Excelente rendimiento grupal"
  break
end

# Verificación de progreso con UNTIL
progreso = 0
creditos_simulados = 0

# ERROR: Condición con string
until "condicion"
  progreso = progreso + 1
  creditos_simulados = creditos_simulados + 4
  
  if creditos_simulados >= 40
    # ERROR: Next dentro de UNTIL (correcto en loop)
    # Pero agregamos un break fuera después
    next
  end
end

# Función para calcular índice académico
def calcular_indice(notas, creditos_por_materia)
  suma_producto = 0
  suma_creditos = 0
  contador = 0
  
  for nota in notas
    credito = creditos_por_materia
    suma_producto = suma_producto + nota * credito
    suma_creditos = suma_creditos + credito
    contador = contador + 1
  end
  
  # ERROR: Next fuera de loop
  if suma_creditos == 0
    next
  end
  
  indice = suma_producto / suma_creditos
  
  # ERROR: Return con tipo incompatible
  return "indice calculado"
end

# Procesamiento de materias
creditos_materias = [4, 3, 4, 3, 5]
materias = ["Cálculo", "Física", "Programación", "Química", "Inglés"]

# Rangos de notas con FOR
contador_rango = 0
estudiantes_excelentes = 0
estudiantes_buenos = 0
estudiantes_regulares = 0

for nota in notas_parcial1
  if nota >= 90
    estudiantes_excelentes = estudiantes_excelentes + 1
  elsif nota >= 70
    estudiantes_buenos = estudiantes_buenos + 1
  else
    estudiantes_regulares = estudiantes_regulares + 1
  end
  
  contador_rango = contador_rango + 1
end

# ERROR: Operador incompatible (string - integer)
texto_nota = "Nota: "
resultado_erroneo = texto_nota - 50

# Cálculo de porcentajes
total_evaluados = estudiantes_excelentes + estudiantes_buenos + estudiantes_regulares

if total_evaluados > 0
  porcentaje_excelentes = estudiantes_excelentes * 100 / total_evaluados
  porcentaje_buenos = estudiantes_buenos * 100 / total_evaluados
  porcentaje_regulares = estudiantes_regulares * 100 / total_evaluados
end

# ERROR: Asignación a palabra reservada (otra instancia)
def = 500
end = 600

# Proyección de desempeño
notas_historicas = [75, 78, 80, 82, 85]
tendencia_positiva = true

for i in 0..3
  nota_actual = notas_historicas
  nota_siguiente = notas_historicas
  
  # ERROR: Operador incompatible (string * float)
  mensaje = "Tendencia" * 2.5
  
  if nota_siguiente < nota_actual
    tendencia_positiva = false
  end
end

# Función para determinar beca
def elegible_beca(promedio, creditos, situacion_economica)
  requisito_promedio = promedio >= 85
  requisito_creditos = creditos >= 30
  
  # ERROR: Variable no declarada en expresión
  requisito_completo = requisito_promedio && requisito_creditos && ingreso_familiar
  
  if requisito_completo
    return true
  else
    return false
  end
end

# Simulación de sistema de becas
estudiantes_con_beca = 0
promedio_becarios = 0

contador_beca = 0
while contador_beca < 5
  promedio_est = notas_parcial1 + notas_parcial2 + notas_parcial3 / 3
  creditos_est = 35
  
  if promedio_est >= 85
    estudiantes_con_beca = estudiantes_con_beca + 1
    promedio_becarios = promedio_becarios + promedio_est
  end
  
  contador_beca = contador_beca + 1
end

# ERROR: División por cero en expresión
if estudiantes_con_beca > 0
  promedio_final_becarios = promedio_becarios / (10 - 10)
end

# Análisis de asistencia
asistencias_totales = [45, 48, 50, 42, 47]
clases_totales = 50

# Cálculo de porcentaje de asistencia
for asistencia in asistencias_totales
  porcentaje_asistencia = asistencia * 100 / clases_totales
  porcentaje_float = porcentaje_asistencia * 1.0
  porcentaje_int = porcentaje_float.to_i
  
  if porcentaje_asistencia < 75
    puts "Asistencia insuficiente"
  end
end

# ERROR: Break fuera de loop (segunda instancia)
if porcentaje_asistencia < 80
  puts "Alerta de asistencia"
  break
end

# Generación de reportes finales
puts "==================================="
puts "REPORTE ACADÉMICO FINAL"
puts "==================================="

print "Estudiantes evaluados: "
puts total_estudiantes

print "Estudiantes aprobados: "
puts $aprobados

print "Tasa de aprobación: "
porcentaje_aprobacion = $aprobados * 100 / total_estudiantes
puts porcentaje_aprobacion

# ERROR: Conversión implícita inválida (otra instancia)
reporte_texto = "Resumen del período " + 2024

puts "==================================="
puts "Distribución de calificaciones:"
print "Excelentes: "
puts estudiantes_excelentes
print "Buenos: "
puts estudiantes_buenos
print "Regulares: "
puts estudiantes_regulares
puts "==================================="

# Proyección para siguiente período
meta_aprobacion = 85
diferencia = meta_aprobacion - porcentaje_aprobacion

if diferencia > 0
  puts "Se requiere mejorar el rendimiento"
  accion_requerida = true
elsif diferencia == 0
  puts "Meta alcanzada exactamente"
  accion_requerida = false
else
  puts "Meta superada"
  accion_requerida = false
end