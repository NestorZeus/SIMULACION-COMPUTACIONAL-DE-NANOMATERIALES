from random import randint
import matplotlib.pyplot as plt
import numpy as np
import itertools
from math import floor, log
import pandas as pd


factorial= itertools.product((1,0.5,0),(1,0.5,0),(1,0.5,0))
resultados=[]
for d1, d2, d3 in factorial:
    print('##############',d1,d2,d3,'###############')
    ciclos=10
    Rpl=[]
    for rpt in range(ciclos):
        modelos = pd.read_csv('digits.txt', sep=' ', header = None)
        modelos = modelos.replace({'n': d1, 'g': d2, 'b': d3})
        r, c = 5, 3
        dim = r * c
        tasa = 0.15
        tranqui = 0.99
        tope = 9
        k = tope + 1 # incl. cero
        contadores = np.zeros((k, k + 1), dtype = int)
        n = floor(log(k-1, 2)) + 1
        neuronas = np.random.rand(n, dim) # perceptrones
  
        for t in range(5000): # entrenamiento
            d = randint(0, tope)
            pixeles = 1 * (np.random.rand(dim) < modelos.iloc[d])
            correcto = '{0:04b}'.format(d)
            for i in range(n):
                w = neuronas[i, :]
                deseada = int(correcto[i]) # 0 o 1
                resultado = sum(w * pixeles) >= 0
                if deseada != resultado: 
                    ajuste = tasa * (1 * deseada - 1 * resultado)
                    tasa = tranqui * tasa 
                    neuronas[i, :] = w + ajuste * pixeles
 
        for t in range(300): # prueba
            d = randint(0, tope)
            pixeles = 1 * (np.random.rand(dim) < modelos.iloc[d])
            correcto = '{0:04b}'.format(d)
            salida = ''
            for i in range(n):
                salida += '1' if sum(neuronas[i, :] * pixeles) >= 0 else '0'
            r = min(int(salida, 2), k)
            contadores[d, r] += 1
        c = pd.DataFrame(contadores)
        c.columns = [str(i) for i in range(k)] + ['NA']
        c.index = [str(i) for i in range(k)]

        arr=c.to_numpy()
        TP=sum(arr.diagonal())
        FP=(sum(sum(arr[:,:tope])))-TP
        FN= sum(sum(arr[:,-1:]))
        Precision= TP/(TP+FP)
        Recuperacion= TP/(TP+FN)
        puntajeF= 2*(Precision*Recuperacion)/(Precision+Recuperacion)
        Rpl.append(puntajeF)
    resultados.append(Rpl)

factorial2= itertools.product((1,0.5,0),(1,0.5,0),(1,0.5,0))
ejex=[]
for i in factorial2:
    ejex.append(str(i)) 
print(ejex)
fig, ax = plt.subplots(nrows = 1, ncols = 1)
plt.ylabel('F-score')
parts = ax.violinplot(resultados, showmeans=False, showmedians=False, showextrema=False)

for p in parts['bodies']:
    p.set_facecolor('orange')
    p.set_edgecolor('red')
    p.set_alpha(1)
c='blue'
plt.boxplot(resultados,
            capprops=dict(color=c),
            whiskerprops=dict(color=c),
            flierprops=dict(color=c, markeredgecolor=c),
            medianprops=dict(color='lime'),widths=([0.15]*len(resultados)))
plt.subplots_adjust(bottom = 0.5, wspace = 0.02)
plt.xlabel('Probabilidades (n,g,b)')
ax.set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
            21,22,23,24,25,26])
ax.set_xticklabels(ejex, rotation=65)
plt.savefig('img_1.png', bbox_inches = 'tight')
plt.close()
