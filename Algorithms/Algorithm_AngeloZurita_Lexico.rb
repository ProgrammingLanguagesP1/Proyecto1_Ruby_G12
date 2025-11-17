# Algoritmo 1 - Sistema de Gestión de Calificaciones
# Tester: Angelo Zurita (@aszurita)

# Variables globales y constantes
MAX_ESTUDIANTES = 50
MIN_NOTA = 0
MAX_NOTA = 100
$total_aprobados = 0
$promedio_general = 0.0

# Clase Estudiante
class Estudiante
  def initialize(nombre, edad)
    @nombre = nombre
    @edad = edad
    @notas = []
  end

  def agregar_nota(nota)
    if nota >= MIN_NOTA && nota <= MAX_NOTA
      @notas += [nota]
      return true
    else
      return false
    end
  end

  def calcular_promedio()
    suma = 0
    contador = 0
    for nota in @notas
      suma += nota
      contador += 1
    end
    if contador > 0
      return suma / contador
    else
      return 0
    end
  end

  def obtener_estado()
    prom = calcular_promedio()
    if prom >= 90
      estado = "Excelente"
    elsif prom >= 70
      estado = "Bueno"
    elsif prom >= 60
      estado = "Aprobado"
    else
      estado = "Reprobado"
    end
    return estado
  end
end

# Funciones auxiliares
def validar_edad(edad)
  valida = edad >= 16 && edad <= 100
  return valida
end

def calcular_estadisticas(numeros)
  suma = 0
  maximo = 0
  minimo = 100
  contador = 0
  for num in numeros
    suma += num
    contador += 1
    if num > maximo
      maximo = num
    end
    if num < minimo
      minimo = num
    end
  end
  promedio = suma / contador
  estadisticas = {
    suma: suma,
    promedio: promedio,
    maximo: maximo,
    minimo: minimo
  }
  return estadisticas
end

# Programa principal
nombres = ["Ana", "Luis", "Maria", "Pedro", "Sofia"]
edades = [20, 22, 19, 21, 23]
estudiantes = []
total_estudiantes = 0

puts "Sistema de Gestión de Calificaciones"
puts "===================================="

# Registro de estudiantes
for i in 0..4
  nombre = nombres
  edad = edades
  if validar_edad(edad)
    total_estudiantes += 1
    puts nombre
  end
end

# Notas por materia
matematicas = [85, 90, 78, 92, 88]
fisica = [80, 85, 82, 88, 90]
quimica = [90, 95, 88, 93, 91]

# Análisis estadístico
stats_mat = calcular_estadisticas(matematicas)
stats_fis = calcular_estadisticas(fisica)
stats_qui = calcular_estadisticas(quimica)

# Cálculo de promedio general con WHILE
contador = 0
suma_promedios = 0
while contador < 3
  if contador == 0
    suma_promedios += stats_mat
  elsif contador == 1
    suma_promedios += stats_fis
  else
    suma_promedios += stats_qui
  end
  contador += 1
end

$promedio_general = suma_promedios / 3

# Verificación con UNTIL
verificacion = 0
until verificacion >= total_estudiantes
  verificacion += 1
  $total_aprobados += 1
end

# Análisis de resultados
edad_promedio = 105 / total_estudiantes
todos_aprobados = $promedio_general >= 60 && total_estudiantes > 0
necesita_mejora = !todos_aprobados || $promedio_general < 75

# Reporte final
puts "===================================="
puts "REPORTE FINAL"
puts "===================================="
print "Total estudiantes: "
puts total_estudiantes
print "Promedio general: "
puts $promedio_general

if todos_aprobados && !necesita_mejora
  puts "Estado: Excelente"
else
  puts "Estado: Requiere mejoras"
end

puts "Sistema finalizado"
