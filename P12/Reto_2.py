from random import randint
import random
from math import floor, log
import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt

resultados=[]
for pr in (0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1):
    print('##############',pr,'###############')
    ciclos=20
    Rpl=[]
    for rpt in range(ciclos):
        modelos = pd.read_csv('digits.txt', sep=' ', header = None)
        modelos = modelos.replace({'n': 1, 'g': 0, 'b': 0})
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
            if (random.uniform(0, 1)) < pr:
                pixeles= random.randint(0, 1)* np.random.rand(dim)
            
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
            if (random.uniform(0, 1)) < pr:
                pixeles= random.randint(0, 1)* np.random.rand(dim)
                
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
plt.xlabel('Probabilidad de sal y pimienta')
ax.set_xticks([1,2,3,4,5,6,7,8,9,10])
ax.set_xticklabels(['0.1','0.2','0.3','0.4','0.5','0.6','0.7',
                    '0.8','0.9','1.0'])
plt.savefig('img_3.png', bbox_inches = 'tight')
plt.close()
