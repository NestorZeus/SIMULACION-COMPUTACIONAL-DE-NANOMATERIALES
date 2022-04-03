from random import random
from numpy.random import shuffle
import matplotlib.pyplot as plt
from math import exp, floor, log
import numpy as np
from random import randint

def rotura(x, c, d):
    return 1 / (1 + exp((c - x) / d))
 
def union(x, c):
    return exp(-x / c)
    
def romperse(tam, cuantos):
    if tam == 1: # no se puede romper
        return [tam] * cuantos
    res = []
    for cumulo in range(cuantos):
        if random() < rotura(tam, c, d):
            primera = randint(1, tam - 1)
            segunda = tam - primera
            assert primera > 0
            assert segunda > 0
            assert primera + segunda == tam
            res += [primera, segunda]
        else:
            res.append(tam) # no rompió
    assert sum(res) == tam * cuantos
    return res
 
def unirse(tam, cuantos):
    res = []
    for cumulo in range(cuantos):
        if random() < union(tam, c):
            res.append(-tam) # marcamos con negativo los que quieren unirse
        else:
            res.append(tam)
    return res
CB=[]


k = 5000
n = 1000000
repeticiones=40

contador=0
metodos=3 
for met in range(metodos):
    promedio=[]
    for rep in range(repeticiones):
        orig = np.random.normal(size = k)
        cumulos = orig - min(orig)
        cumulos += 1 # ahora el menor vale uno
        cumulos = cumulos / sum(cumulos) # ahora suman a uno
        cumulos *= n # ahora suman a n, pero son valores decimales
        cumulos = np.round(cumulos).astype(int) # ahora son enteros
        diferencia = n - sum(cumulos) # por cuanto le hemos fallado
        cambio = 1 if diferencia > 0 else -1

        while diferencia != 0:
            p = randint(0, k - 1)
            if cambio > 0 or (cambio < 0 and cumulos[p] > 0): # sin vaciar
                cumulos[p] += cambio
                diferencia -= cambio
        assert all(cumulos != 0)
        assert sum(cumulos) == n
 
        if contador == 0:
            c = np.median(cumulos) # tamaño crítico de cúmulos           
        elif contador==1:
            c = min(cumulos)# factor arbitrario para suavizar la curva
        elif contador==2:
            c = max(cumulos)
            
        d = np.std(cumulos) / 4
        
        duracion = 50
        digitos = floor(log(duracion, 10)) + 1
        part_porc=[]
        for paso in range(duracion):
            assert sum(cumulos) == n
            assert all([c > 0 for c in cumulos]) 
            (tams, freqs) = np.unique(cumulos, return_counts = True)
            cumulos = []
            assert len(tams) == len(freqs)
            for i in range(len(tams)):
                cumulos += romperse(tams[i], freqs[i]) 
            assert sum(cumulos) == n
            assert all([c > 0 for c in cumulos]) 
            (tams, freqs) = np.unique(cumulos, return_counts = True)
            cumulos = []
            assert len(tams) == len(freqs)
            for i in range(len(tams)):
                cumulos += unirse(tams[i], freqs[i])
            cumulos = np.asarray(cumulos)
            neg = cumulos < 0
            a = len(cumulos)
            juntarse = -1 * np.extract(neg, cumulos) # sacarlos y hacerlos positivos
            cumulos = np.extract(~neg, cumulos).tolist() # los demás van en una lista
            assert a == len(juntarse) + len(cumulos)
            nt = len(juntarse)
            if nt > 1:
                shuffle(juntarse) # orden aleatorio
            j = juntarse.tolist()
            while len(j) > 1: # agregamos los pares formados
                cumulos.append(j.pop(0) + j.pop(0))
            if len(j) > 0: # impar
                cumulos.append(j.pop(0)) # el ultimo no alcanzó pareja
            assert len(j) == 0
            assert sum(cumulos) == n
            assert all([c != 0 for c in cumulos])
            grandes=[]
            for s in cumulos:
                if s > c:
                    grandes.append(s)
            part_porc.append((len(grandes)/len(cumulos))*100)
        promedio.append((sum(part_porc)/len(part_porc)))
    CB.append(promedio)
    contador=contador+1
print(len(CB))
plt.boxplot(CB, [1,2,3])
plt.xlabel('Valor critico de cúmulos')
plt.ylabel('Promedios retenidos en filtro (%)')
plt.xticks([1,2,3], ['Mediana','mínimo','máximo'],rotation=10)
plt.show()

listax=[i for i in range(len(CB[0]))]

plt.scatter([np.arange(len(CB[0]))],sorted(CB[0]),color='blue')
plt.scatter([np.arange(len(CB[1]))],sorted(CB[1]),color='red')
plt.scatter([np.arange(len(CB[2]))],sorted(CB[2]),color='green')

plt.plot(listax,sorted(CB[0]),color='blue', label='Mediana')
plt.plot(listax,sorted(CB[1]),color='red',label='Mínimo')
plt.plot(listax,sorted(CB[2]),color='green',label='Máximo')
plt.xlabel('Réplicas')
plt.ylabel('Promedios retenidos en filtro (%)')
plt.legend(loc='best')
plt.show()
