import numpy as np 
from random import random
import matplotlib.cm as cm
import matplotlib.pyplot as plt

def mapeo(pos):
    fila = pos // dim
    columna = pos % dim
    return actual[fila, columna]

def paso(pos):
    fila = pos // dim
    columna = pos % dim
    vecindad = actual[max(0, fila - 1):min(dim, fila + 2),
                      max(0, columna - 1):min(dim, columna + 2)]
    return 1 * (np.sum(vecindad) - actual[fila, columna] == 3)

dimension = (10, 15, 20)
probabilidad = (0.2, 0.4, 0.6, 0.8)
grafico=[]
bp=[]
for dim in dimension:
    print("################ Dimensión:",dim,"#########################")
    num = dim**2
    vpp=[]#vivos por probabilidad
    mpp=[]#muertos por probabilidad
    for p in probabilidad:
        print("######### probabilidad:",p,"################")
        rep = 200
        vivieron=[]
        murieron=[]
        for replicas in range(rep):# ciclo de las 30 réplicas
            valores = [1 * (random() < p) for i in range(num)]
            actual = np.reshape(valores, (dim, dim))
            assert all([mapeo(x) == valores[x]  for x in range(num)])  
            dur = 50
            historial = []
            for iteracion in range(dur):
                valores = [paso(x) for x in range(num)]
                vivos = sum(valores)
                historial.append(vivos)
                historial[-4:]
                cuantos = 4
                actual = np.reshape(valores, (dim, dim))  
                if vivos == 0:
                    murieron.append(iteracion)#guarda las iteraciones en que murieron todos
                    break; # nadie vivo
                if len(historial) > cuantos and len(set(historial[-cuantos:])) == 1:
                    vivieron.append(iteracion)# guarda las iteraciones llegaron a 50 
                    break;
        vpp.append(((len(vivieron))*100)/rep)#guarda el porcentaje que vivieron
        mpp.append(((len(murieron))*100)/rep)
        print("muertes en 30 réplicas:",len(murieron))
        print("vivos en 30 réplicas:",len(vivieron))
    print("vpp:",vpp)
    grafico.append(vpp)
print(grafico)

linedim10=[grafico[0][0],grafico[0][1],grafico[0][2],grafico[0][3]]
linedim15=[grafico[1][0],grafico[1][1],grafico[1][2],grafico[1][3]]
linedim20=[grafico[2][0],grafico[2][1],grafico[2][2],grafico[2][3]]
plt.plot([0,1,2,3],linedim10,label='dimensión 10')
plt.scatter([0,1,2,3],linedim10)
plt.plot([0,1,2,3],linedim15,label='dimensión 15')
plt.scatter([0,1,2,3],linedim15)
plt.plot([0,1,2,3],linedim20,label='dimensión 20')
plt.scatter([0,1,2,3],linedim20)
plt.xticks([0,1,2,3], ('0.2', '0.4', '0.6', '0.8'))
plt.ylabel('Probabilidad que no muera toda la población (%)')
plt.xlabel('Probabilidad')
plt.title('Gráfico de porcentaje de supervivencia de poblacion')
plt.legend()
plt.show()
