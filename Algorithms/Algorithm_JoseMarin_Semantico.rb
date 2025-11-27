# ============================================================================
# ALGORITMO 3 - Sistema de Gestión de Calificaciones Estudiantiles
# Tester: José Marin (@JoseM0lina)
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
$aprobados_global = 0

# ERROR: Modificación de constante
NOTA_MAXIMA = 110

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
    if nota >= NOTA_MINIMA
      calificacion_nueva = nota
      @creditos_acumulados = @creditos_acumulados + creditos
      return true
    else
      return false
    end
  end
  
  def calcular_promedio_ponderado()
    suma_ponderada = 0
    suma_creditos = 0
    
    if suma_creditos > 0
      promedio = suma_ponderada / suma_creditos
      return promedio
    else
      return 0
    end
  end
end

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
  total = texto_cantidad + cantidad
  
  examenes_restantes = 1
  nota_requerida = nota_deseada * (cantidad + examenes_restantes) - suma_actual
  
  return nota_requerida
end

# Función para generar estadísticas del curso
def estadisticas_curso(lista_notas)
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
  
  # ERROR: División por cero
  promedio = suma / 0
  
  return promedio
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

# Procesamiento de calificaciones
total_estudiantes = 0
suma_promedios = 0

for i in 0..4
  nombre = nombres
  nota1 = notas_parcial1
  nota2 = notas_parcial2
  nota3 = notas_parcial3
  
  # ERROR: Operador incompatible
  texto_promedio = "promedio: "
  resultado_invalido = texto_promedio - 10
  
  promedio_estudiante = nota1 + nota2 + nota3
  suma_promedios = suma_promedios + promedio_estudiante
  
  if promedio_estudiante >= NOTA_APROBATORIA
    total_estudiantes = total_estudiantes + 1
  end
end

# ERROR: Modificación de constante
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

until progreso >= 10
  progreso = progreso + 1
  creditos_simulados = creditos_simulados + 4
  
  if creditos_simulados >= 40
    progreso = 10
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
  return indice
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

# Cálculo de porcentajes
total_evaluados = estudiantes_excelentes + estudiantes_buenos + estudiantes_regulares

if total_evaluados > 0
  porcentaje_excelentes = estudiantes_excelentes * 100 / total_evaluados
  porcentaje_buenos = estudiantes_buenos * 100 / total_evaluados
  porcentaje_regulares = estudiantes_regulares * 100 / total_evaluados
end

# Proyección de desempeño
notas_historicas = [75, 78, 80, 82, 85]
tendencia_positiva = true

for i in 0..3
  nota_actual = notas_historicas
  nota_siguiente = notas_historicas
  
  # ERROR: Operador incompatible
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
  promedio_est = notas_parcial1
  creditos_est = 35
  
  if promedio_est >= 85
    estudiantes_con_beca = estudiantes_con_beca + 1
    promedio_becarios = promedio_becarios + promedio_est
  end
  
  contador_beca = contador_beca + 1
end

# Análisis de asistencia
asistencias_totales = [45, 48, 50, 42, 47]
clases_totales = 50

# Cálculo de porcentaje de asistencia
porcentaje_asistencia = 0

for asistencia in asistencias_totales
  porcentaje_asistencia = asistencia * 100 / clases_totales
  
  if porcentaje_asistencia < 75
    puts "Asistencia insuficiente"
  end
end

# ERROR: Break fuera de loop
if porcentaje_asistencia < 80
  puts "Alerta de asistencia"
  break
end

# Generación de reportes finales
puts "==================================="
puts "REPORTE ACADÉMICO FINAL"
puts "==================================="

# ERROR: Variable no declarada
# ERROR: Variable global no declarada
porcentaje_aprobacion = $aprobados * 100 / total_estudiantes

print "Estudiantes evaluados: "
puts total_estudiantes

print "Estudiantes aprobados: "
puts $aprobados

print "Tasa de aprobación: "
puts porcentaje_aprobacion

# ERROR: Conversión implícita inválida (string + integer)
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

# ERROR: Variable no declarada en operación
diferencia = meta_aprobacion - tasa_actual

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

puts "==================================="
puts "Sistema de gestión académica finalizado"
puts "==================================="