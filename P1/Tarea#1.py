from random import random, randint, getrandbits
from math import fabs, sqrt
import matplotlib.pyplot as plt
import numpy as np
from time import time

runs = 30 #replicas
caminatas = [100, 1000, 10000] #pasos
results = [] #almacena las dimensiones

for i in range(3): #itera la cantidad de pasos
    dur = caminatas[i]
    for dim in range(1, 6): #de una a cinco dimensiones
        mayores = []
        for rep in range(runs):#corre el experimento 30 veces en cada dimension
            before = time()*1000
            pos = [0] * dim
            mayor = 0
            for paso in range(dur):
                eje = randint(0, dim - 1)
                if pos[eje] > -100 and pos[eje] < 100:
                    if random() < 0.5:
                        pos[eje] += 1
                    else:
                        pos[eje] -= 1
                else:
                    if pos[eje] == -100:
                        pos[eje] += 1
                    if pos[eje] == 100:
                        pos[eje] -= 1
                mayor = max(mayor, sqrt(sum([p**2 for p in pos])))
            mayores.append(mayor)
            after = time()*1000
        results.append(mayores)
tiempo = after - before
print(tiempo)

#separar los resultados en tres grupos de caminatas
walks_1 = results[0:4]
walks_2 = results[4:8]
walks_3 = results[8:12]

#empezar a graficar

ticks = ['1', '2', '3', '4', '5']

#funcion definir los colores de cajas y bigotes
def set_box_color(bp, color):
    plt.setp(bp['boxes'], color='green')
    plt.setp(bp['whiskers'], color='gray')
    plt.setp(bp['caps'], color='red')
    plt.setp(bp['medians'], color='purple')

def box_plot(data, edge_color, fill_color):
    bp = ax.boxplot(data, patch_artist=True)
    
    for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color=edge_color)

    for patch in bp['boxes']:
        patch.set(facecolor=fill_color)

    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

        
plt.figure()

bpl = plt.boxplot(walks_1, positions=np.array(range(len(walks_1)))*6.0-1.0, sym='-1', widths=1.2)
bpc = plt.boxplot(walks_2, positions=np.array(range(len(walks_2)))*6.0, sym='-1', widths=1.2)
bpr = plt.boxplot(walks_3, positions=np.array(range(len(walks_3)))*6.0+1.0, sym='-1', widths=1.2)
set_box_color(bpl, '#67001f')
set_box_color(bpc, '#1a1a1a')
set_box_color(bpr, '#d6604d')


plt.xticks(range(0, len(ticks)*5, 5), ticks)
plt.ylim(0, len(ticks)*40)
plt.xlim(-3, len(ticks)*5)
plt.title('Distancia Manhattan')
plt.tight_layout()
plt.savefig('DistanciaMan.png')
plt.show()
