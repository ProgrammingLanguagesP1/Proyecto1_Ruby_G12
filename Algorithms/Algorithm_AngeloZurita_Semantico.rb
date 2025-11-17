# ============================================================================
# ALGORITMO - Sistema de Gestión de Inventario de Librería
# Tester: Angelo Zurita (@aszurita)
# Descripción: Sistema para gestionar inventario, ventas y estadísticas
#              de una librería. Contiene errores semánticos intencionales.
# ============================================================================

# Variables globales y constantes
MAX_LIBROS = 100
MIN_PRECIO = 5
DESCUENTO_ESTUDIANTE = 0.15
$total_ventas = 0
$libros_vendidos = 0

# ERROR SEMÁNTICO: Modificación de constante
MAX_LIBROS = 150

# Clase Libro
class Libro
  def initialize(titulo, autor, precio, cantidad)
    @titulo = titulo
    @autor = autor
    @precio = precio
    @cantidad = cantidad
    @ventas = 0
  end

  def calcular_valor_inventario()
    valor = @precio * @cantidad
    return valor
  end

  def aplicar_descuento(porcentaje)
    # ERROR SEMÁNTICO: Operación incompatible (string - float)
    descuento = "precio" - porcentaje
    precio_nuevo = @precio * descuento
    return precio_nuevo
  end

  def vender(cantidad_venta)
    if cantidad_venta <= @cantidad
      @cantidad -= cantidad_venta
      @ventas += cantidad_venta
      return true
    else
      return false
    end
  end

  def necesita_reabastecimiento()
    # ERROR SEMÁNTICO: Condición con string (warning)
    if @titulo
      limite = 10
      return @cantidad < limite
    end
  end
end

# Funciones auxiliares
def validar_precio(precio)
  # ERROR SEMÁNTICO: Variable no declarada
  valido = precio >= MIN_PRECIO && precio <= precio_maximo
  return valido
end

def calcular_total_inventario(libros)
  total = 0
  contador = 0

  for libro in libros
    total += libro
    contador += 1
  end

  # ERROR SEMÁNTICO: División por cero
  promedio = total / 0

  return total
end

def generar_reporte_ventas(ventas_mes)
  suma = 0
  maximo = 0
  minimo = 1000

  # ERROR SEMÁNTICO: Conversión implícita inválida
  mes_texto = "Enero"
  total_con_mes = suma + mes_texto

  for venta in ventas_mes
    suma += venta
    if venta > maximo
      maximo = venta
    end
    if venta < minimo
      minimo = venta
    end
  end

  reporte = {
    total: suma,
    maximo: maximo,
    minimo: minimo
  }

  return reporte
end

# ERROR SEMÁNTICO: Return fuera de función
return "inicializacion"

# Programa principal
puts "Sistema de Gestión de Inventario"
puts "=================================="

# Inicialización de inventario
titulos = ["Cien años de soledad", "Don Quijote", "El Principito", "1984", "Rayuela"]
autores = ["García Márquez", "Cervantes", "Saint-Exupéry", "Orwell", "Cortázar"]
precios = [25.99, 30.50, 15.75, 22.00, 28.50]
cantidades = [50, 30, 45, 25, 35]

libros_inventario = []
total_libros = 0

# ERROR SEMÁNTICO: Asignación a palabra reservada
puts = "Mensaje del sistema"

# Registro de libros
for i in 0..4
  titulo = titulos
  autor = autores
  precio = precios
  cantidad = cantidades

  if validar_precio(precio)
    total_libros += 1
    # ERROR SEMÁNTICO: Cambio de tipo (warning)
    total_libros = "muchos libros"
  end
end

# Simulación de ventas
ventas_enero = [120, 95, 150, 80, 110]
ventas_febrero = [100, 105, 130, 90, 115]
ventas_marzo = [140, 120, 160, 100, 125]

# Cálculo de estadísticas
stats_enero = generar_reporte_ventas(ventas_enero)
stats_febrero = generar_reporte_ventas(ventas_febrero)
stats_marzo = generar_reporte_ventas(ventas_marzo)

# ERROR SEMÁNTICO: Modificación de constante
DESCUENTO_ESTUDIANTE = 0.20

# Aplicación de descuentos
descuento_aplicado = DESCUENTO_ESTUDIANTE * 100
precio_con_descuento = precios - descuento_aplicado

# Cálculo de ventas totales con WHILE
contador_mes = 0
suma_ventas = 0
while contador_mes < 3
  if contador_mes == 0
    suma_ventas += stats_enero
  elsif contador_mes == 1
    suma_ventas += stats_febrero
  else
    suma_ventas += stats_marzo
  end
  contador_mes += 1
end

$total_ventas = suma_ventas

# ERROR SEMÁNTICO: Break fuera de loop
if $total_ventas > 500
  break
end

# Verificación con UNTIL
verificacion = 0
# ERROR SEMÁNTICO: Condición con array (warning)
until cantidades
  verificacion += 1
  $libros_vendidos += 5
end

# Análisis de resultados
promedio_ventas = $total_ventas / 3
meta_cumplida = promedio_ventas >= 100 && total_libros > 0
necesita_promocion = !meta_cumplida || promedio_ventas < 120

# Función para calcular ganancia
def calcular_ganancia(precio_venta, precio_costo, cantidad)
  # ERROR SEMÁNTICO: Variable no declarada usada en operación
  ganancia_unitaria = precio_venta - costo_base
  ganancia_total = ganancia_unitaria * cantidad

  # ERROR SEMÁNTICO: Next fuera de loop
  if ganancia_total < 0
    next
  end

  # ERROR SEMÁNTICO: Return con tipo incompatible (warning)
  return "ganancia positiva"
end

# Procesamiento de reabastecimiento
cantidad_reabastecer = 0
for i in 0..4
  stock_actual = cantidades

  # ERROR SEMÁNTICO: Conversión con pérdida de datos (warning)
  precio_decimal = precios
  precio_entero = precio_decimal.to_i

  if stock_actual < 20
    cantidad_reabastecer += 1
  end
end

# ERROR SEMÁNTICO: Asignación a palabra reservada
if = 100
else = 200

# Categorización de libros
categoria_ficcion = 0
categoria_no_ficcion = 0

contador = 0
while contador < 5
  # ERROR SEMÁNTICO: Operación incompatible (string * integer)
  categoria = "Ficcion" * contador

  if contador % 2 == 0
    categoria_ficcion += 1
  else
    categoria_no_ficcion += 1
  end
  contador += 1
end

# Función para generar recomendaciones
def generar_recomendaciones(ventas_historial)
  recomendaciones = []
  total = 0

  for venta in ventas_historial
    total += venta
  end

  promedio = total / ventas_historial.length

  # ERROR SEMÁNTICO: División por cero en expresión
  factor = promedio / (5 - 5)

  if promedio > 100
    recomendaciones = ["Aumentar stock", "Promocionar"]
  else
    recomendaciones = ["Mantener", "Descuento"]
  end

  return recomendaciones
end

# Cálculo de impuestos
TASA_IMPUESTO = 0.12
# ERROR SEMÁNTICO: Modificación de constante recién creada
TASA_IMPUESTO = 0.15

impuesto_total = $total_ventas * TASA_IMPUESTO

# Análisis de rentabilidad
costo_operativo = 200
ingresos = $total_ventas
utilidad = ingresos - costo_operativo

# ERROR SEMÁNTICO: Variable no declarada en expresión compleja
margen_ganancia = (utilidad / ventas_proyectadas) * 100

# Bucle para verificar stock crítico
libros_criticos = 0
for cantidad in cantidades
  if cantidad < 15
    libros_criticos += 1
    # ERROR SEMÁNTICO: Break dentro de if (correcto), pero agregamos otro caso
  end
end

# ERROR SEMÁNTICO: Break fuera de loop (segunda instancia)
if libros_criticos > 0
  puts "Alerta de stock bajo"
  break
end

# Generación de proyecciones
proyeccion_trimestre = $total_ventas * 3
# ERROR SEMÁNTICO: Conversión implícita inválida
meta_anual = "12 meses" + proyeccion_trimestre

# Reporte final
puts "=================================="
puts "REPORTE FINAL DE INVENTARIO"
puts "=================================="
print "Total de libros en sistema: "
puts total_libros
print "Total de ventas: "
puts $total_ventas
print "Promedio mensual: "
puts promedio_ventas
print "Libros vendidos: "
puts $libros_vendidos

if meta_cumplida && !necesita_promocion
  puts "Estado: Excelente desempeño"
elsif meta_cumplida
  puts "Estado: Buen desempeño"
else
  puts "Estado: Requiere estrategias de mejora"
end

if libros_criticos > 0
  print "Libros con stock crítico: "
  puts libros_criticos
  puts "Acción requerida: Reabastecer inventario"
end

puts "=================================="
puts "Sistema de inventario finalizado"
puts "=================================="
