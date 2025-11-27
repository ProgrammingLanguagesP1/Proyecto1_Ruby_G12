def calcular_multa(dias_atraso)
  multa_total = dias_atraso * 0.50
  return multa_total
end

resultado = calcular_multa(5)
puts resultado
