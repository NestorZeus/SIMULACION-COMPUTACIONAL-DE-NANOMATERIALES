library(dplyr) 
library(ggplot2) #libreria para graficar boxplot agrupado
library(scales) #libreria para hacer modificaciones a la grafica
datos = data.frame() #para almacenar los datos obtenidos
niveles = c(10, 100, 1000, 10000) #caminatas: Nivel 1, Nivel 2, Nivel 3 y Nivel 4

for (dimension in c(2**1, 2**2, 2**3, 2**4, 2**5, 2**6, 2**7)) { #seleccionar dimension
  for (duracion in niveles) { #seleccionar la caminata
    for (replica in 1:12) { #repetir el experimento
      pos = rep(0, dimension)
      mayor = 1
      for (t in 1:duracion) {
        cambiar = sample(1:dimension, 1)
        cambio = 1
        if (runif(1) < 0.5) {
          cambio = -1
        }
