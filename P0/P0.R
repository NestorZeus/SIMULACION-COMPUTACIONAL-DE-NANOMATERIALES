library(dplyr) 
library(ggplot2) #libreria para graficar boxplot agrupado
library(scales) #libreria para hacer modificaciones a la grafica
datos = data.frame() #para almacenar los datos obtenidos
niveles = c(20, 200, 2000, 20000) #caminatas: Nivel 1, Nivel 2, Nivel 3 y Nivel 4

for (dimension in c(2**1, 2**2, 2**3, 2**4, 2**5, 2**6, 2**7)) { #seleccionar dimension
  for (duracion in niveles) { #seleccionar la caminata
    for (replica in 1:12) { #repetir el experimento
      pos = rep(0, dimension)
      mayor = 0
      for (t in 1:duracion) {
        cambiar = sample(1:dimension, 1)
        cambio = 1
        if (runif(1) < 0.5) {
          cambio = -1
        }
        pos[cambiar] = pos[cambiar] + cambio
        d <- sum(abs(pos))
        if (d > mayor) {
          mayor = d
        }
      }
      resultado <- c(dimension, duracion, replica, mayor) #vector para agrupar resultados
      datos <- rbind(datos, resultado) #para llenar en ese orden el dataframe vacio
    }
  }
}
names(datos) <- c("dim", "Caminata", "rep", "dist") #nombre a las columnas del dataframe 

datos$dim = as.factor(datos$dim) #crear vector a partir del dataframe
datos$Caminata = as.factor(datos$Caminata) #crear vector a partir del dataframe
ggplot(datos, aes(x= dim, y= dist, fill= Caminata)) + 
  geom_boxplot(width=1)+
  labs(x = "Dimensión", y = "Distancia", title = 'Distancia Manhattan')+ #nombres
  scale_y_log10() #cambiar la escala del eje "y" a logaritmo
