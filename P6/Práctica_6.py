import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from math import floor, log, sqrt
from random import random, uniform
 
l = 2
n = 40
pi = 0.09
pr = 0.05
v = l / 30
r = 0.1
tmax = 45
runs = 45
maximos = {'Pico más alto': [],
           'Caso sospechosos': []}

def contagiados():
    for i in range(n):
        a1 = agentes.iloc[i]
        if a1.estado == 'I':
            for j in range(n):
                a2 = agentes.iloc[j]
                if a2.estado == 'S':
                    d = sqrt((a1.x - a2.x)**2 + (a1.y - a2.y)**2)
                    if d < r:
                        if random() < (r - d) / r:
                            contagios[j] = True
    return contagios

for k in range(runs):
    agentes =  pd.DataFrame()
    agentes['x'] = [uniform(0, l) for i in range(n)]
    agentes['y'] = [uniform(0, l) for i in range(n)]
    agentes['estado'] = ['S' if random() > pi else 'I' for i in range(n)]
    agentes['dx'] = [uniform(-v/2, v/2) if  agentes.at[i, 'estado'] == 'I'\
                     else uniform(-v, v) for i in range(n)]
    agentes['dy'] = [uniform(-v/2, v/2) if  agentes.at[i, 'estado'] == 'I'\
                     else uniform(-v, v) for i in range(n)]
    epidemia = []
    for tiempo in range(tmax):
        conteos = agentes.estado.value_counts()
        infectados = conteos.get('I', 0)
        epidemia.append(infectados)
        contagios = [False for i in range(n)]
        if infectados == 0:
            break
        contagios = contagiados()
        for i in range(n):
            a = agentes.iloc[i]
            if contagios[i]:
                agentes.at[i, 'dx'] /= 2
                agentes.at[1, 'dy'] /= 2
                agentes.at[i, 'estado'] = 'I'
            elif a.estado == 'I':
                if random() < pr:
                    agentes.at[i, 'estado'] = 'R'
            x = a.x + a.dx
            y = a.y + a.dy
            x = x if x < l else x - l
            y = y if y < l else y - l
            x = x if x > 0 else x + l
            y = y if y > 0 else y + l
            agentes.at[i, 'x'] = x
            agentes.at[i, 'y'] = y
    maximos['Pico más alto'].append(max(epidemia))
    maximos['Caso sospechosos'].append(epidemia.index(max(epidemia)) + 1)
df = pd.DataFrame(maximos)
sns.violinplot(data=df, scale='width', cut=0)
plt.savefig('Slow_Epidemic.png')
plt.show()
