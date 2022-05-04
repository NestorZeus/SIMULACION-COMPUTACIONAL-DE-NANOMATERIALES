import numpy as np
import pandas as pd
from random import random, randint, sample
import matplotlib.pyplot as plt
import math
from scipy.stats import expon
from time import time

def knapsack(peso_permitido, pesos, valores):
    assert len(pesos) == len(valores)
    peso_total = sum(pesos)
    valor_total = sum(valores)
    if peso_total < peso_permitido: 
        return valor_total
    else:
        V = dict()
        for w in range(peso_permitido + 1):
            V[(w, 0)] = 0
        for i in range(len(pesos)):
            peso = pesos[i]
            valor = valores[i]
            for w in range(peso_permitido + 1):
                cand = V.get((w - peso, i), -float('inf')) + valor
                V[(w, i + 1)] = max(V[(w, i)], cand)
        return max(V.values())
 
def factible(seleccion, pesos, capacidad):
    return np.inner(seleccion, pesos) <= capacidad
  
def objetivo(seleccion, valores):
    return np.inner(seleccion, valores)
 
def normalizar(data):
    menor = min(data)
    mayor = max(data)
    rango  = mayor - menor
    data = data - menor # > 0
    return data / rango # entre 0 y 1
  
def pesos1(cuantos, low, high):
    return np.round(normalizar(np.random.uniform(size = cuantos)) * (high - low) + low)
 
def valores1(pesos, low, high):
    n = len(pesos)
    valores = np.empty((n))
    for i in range(n):
        valores[i] = np.random.uniform(pesos[i], random(), 1)
    return normalizar(valores) * (high - low) + low

def pesos2(valores, low, high):
    cuantos=1/valores
    return np.round(normalizar(cuantos) * (high - low) + low)
 
def valores2(cuantos, low, high):
    valores = expon.rvs(size= cuantos)
    return normalizar(valores) * (high - low) + low

def pesos3(cuantos, low, high):
    return np.round(normalizar(np.random.normal(size = cuantos)) * (high - low) + low)
 
def valores3(pesos, low, high):
    n = len(pesos)
    valores = np.empty((n))
    magnitud=0.3
    ruido=np.random.normal(loc=5, size = n)
    ruido=ruido*magnitud
    for i in range(n):
        valores[i] = (pesos[i]**2)+ ruido[i]
    return normalizar(valores) * (high - low) + low
 
def poblacion_inicial(n, tam):
    pobl = np.zeros((tam, n))
    for i in range(tam):
        pobl[i] = (np.round(np.random.uniform(size = n))).astype(int)
    return pobl
 
def mutacion(sol, n):
    pos = randint(0, n - 1)
    mut = np.copy(sol)
    mut[pos] = 1 if sol[pos] == 0 else 0
    return mut
  
def reproduccion(x, y, n):
    pos = randint(2, n - 2)
    xy = np.concatenate([x[:pos], y[pos:]])
    yx = np.concatenate([y[:pos], x[pos:]])
    return (xy, yx)
 
n = 40
VP=[]
Tr=[]
for regla in range(3):
    print("############## regla:",regla,"#################")
    if regla == 0:
        pesos = pesos1(n, 23, 100)
        valores = valores1(pesos, 5, 700)
    if regla == 1:
        valores = valores2(n, 5, 700)
        pesos = pesos2(valores, 23, 80)
    if regla == 2:
        pesos = pesos3(n, 23, 100)
        valores = valores3(pesos, 10, 700)
    
    capacidad = int(round(sum(pesos) * 0.70))
    optimo = knapsack(capacidad, pesos, valores)
    PM=(0.09,0.20,1)
    INIT=(47,600,900)
    REP=(10,47,100)
    instancias=list(zip(PM, INIT, REP))
    CB=[]
    Ti=[]
    for pm, init, rep in instancias:
        antesi=time()
        print("#############",pm, init, rep,"#############")
        replicas=3
        best=[]
        porc_dif=[]
        for K in range(replicas):
            p = poblacion_inicial(n, init)
            tam = p.shape[0]
            assert tam == init
            tmax = 40
            mejor = None
            mejores = []
            for t in range(tmax):
                for i in range(tam): # mutarse con probabilidad pm
                    if random() < pm:
                        p = np.vstack([p, mutacion(p[i], n)])
                for i in range(rep):  # reproducciones
                    padres = sample(range(tam), 2)
                    hijos = reproduccion(p[padres[0]], p[padres[1]], n)
                    p = np.vstack([p, hijos[0], hijos[1]])
                tam = p.shape[0]
                d = []
                for i in range(tam):
                    d.append({'idx': i, 'obj': objetivo(p[i], valores),
                              'fact': factible(p[i], pesos, capacidad)})
                d = pd.DataFrame(d).sort_values(by = ['fact', 'obj'], ascending = False)
                mantener = np.array(d.idx[:init])
                p = p[mantener, :]
                tam = p.shape[0]
                assert tam == init
                factibles = d.loc[d.fact == True,]
                mejor = max(factibles.obj)
                mejores.append(mejor)
            best.append(mejor)
            porc_dif.append(((optimo - mejor) / optimo)*100)
        CB.append(porc_dif)
        Ti.append(time()-antesi)
    VP.append(CB)
    Tr.append(Ti)

print('------------ Instancia 1 -------------')
print(VP[0][0])
print(VP[0][1])
print(VP[0][2])
print('------------ Instancia 2 -------------')
print(VP[1][0])
print(VP[1][1])
print(VP[1][2])
print('------------ Instancia 3 -------------')
print(VP[2][0])
print(VP[2][1])
print(VP[2][2])
x= [1,4,7]
x2=[2,5,8]
x3=[3,6,9]

plt.bar(x,Tr[0], label="Instancia 1")
plt.bar(x2,Tr[1], label="Instancia 2")
plt.bar(x3,Tr[2], label="Instancia 3")
plt.xticks([2,5,8], ['(0.09, 0.20, 1.0)','(23, 100, 40)','(1.0, 900, 80)'])
plt.xlabel('Instancias')
plt.ylabel('Tiempo de ejecucion (s)')
plt.legend()
plt.show()
               
plt.violinplot(VP[0], positions=[1,4,7])
plt.violinplot(VP[1], positions=[2,5,8])
plt.violinplot(VP[2], positions=[3,6,9])
plt.plot((),(),color='blue',label='Regla 1')
plt.plot((),(),color='orange',label='Regla 2')
plt.plot((),(),color='green',label='Regla 3')
plt.xlabel('Instancias (Pm, Pi, Cz)')
plt.ylabel('Cantidad predeterminada de generaciones')
plt.xticks([2,5,8], ['(1, 23, 100)','(1, 700, 23)','(1, 10000, 700)'])
plt.legend(loc='upper right')
plt.show()

R1_i1=np.mean(VP[0][0])
R1_i2=np.mean(VP[0][1])
R1_i3=np.mean(VP[0][2])
R1=[R1_i1,R1_i2,R1_i3]

R2_i1=np.mean(VP[1][0])
R2_i2=np.mean(VP[1][1])
R2_i3=np.mean(VP[1][2])
R2=[R2_i1,R2_i2,R2_i3]

R3_i1=np.mean(VP[2][0])
R3_i2=np.mean(VP[2][1])
R3_i3=np.mean(VP[2][2])
R3=[R3_i1,R3_i2,R3_i3]

import plotly.graph_objects as go
categories = ['Pm, Pi, Cz \n(0.09, 0.20, 1.0)','Pm, Pi, Cz \n(23, 100, 40)','Pm, Pi, Cz \n(1.0, 900, 80)']
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
      r= R1,
      theta=categories,
      fill='toself',
      name='n= Instancia 1'
))
fig.add_trace(go.Scatterpolar(
      r= R2,
      theta=categories,
      fill='toself',
      name='n= Instancia 2'
))

fig.add_trace(go.Scatterpolar(
      r= R3,
      theta=categories,
      fill='toself',
      name='n= Instancia 3'
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 13]
    )),
  showlegend=True
)

fig.show()
