from math import ceil, sqrt
from random import shuffle
import multiprocessing
from time import time
from scipy.stats import f_oneway
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

d = 1000
h = 7919 
replicas = 30
original = [x for x in range(d, h + 1)]
invertido = original[::-1]
aleatorio = original.copy()
shuffle(aleatorio)
cores = multiprocessing.cpu_count()

def primo_1(n):
    if n < 3:
        return True
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def primo_2(n):
    if n < 4:
        return True
    if n % 2 == 0:
       return False
    for i in range(3, n - 1, 2):
        if n % i == 0:
            return False
    return True

def primo_3(n):
    if n < 4:
        return True
    if n % 2 == 0:
       return False
    for i in range(3, int(ceil(sqrt(n))), 2):
        if n % i == 0:
            return False
    return True

def primo_4(n):
    if n < 4:
        return True
    if n % 2 == 0:
       return False
    for i in range(4, int(ceil(sqrt(n))), 3):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    resultados_1 = {'Prueba 1': [], 'Prueba 2': [], 'Prueba 3': [], 'Prueba 4': []}              
    resultados_2 = {'Resultado 1': [], 'Resultado 2': [], 'Resultado 3': [], 'Resultado 4': []}
    with multiprocessing.Pool(processes = cores-1) as pool:
        pool.map(primo_1, original)
        for r in range(replicas):
            t = (time()*1000)
            pool.map(primo_1, original)
            resultados_1['Prueba 1'].append((time()*1000)-t)
            t = (time()*1000)
            pool.map(primo_2, original)
            resultados_1['Prueba 2'].append((time()*1000)-t)
            t = (time()*1000)
            pool.map(primo_3, original)
            resultados_1['Prueba 3'].append((time()*1000)-t)
            t = (time()*1000)
            pool.map(primo_4, original)
            resultados_1['Prueba 4'].append((time()*1000)-t)
            t = (time()*1000)
            pool.map(primo_3, original)
            resultados_2['Resultado 1'].append((time()*1000) - t)
            t = (time()*1000)
            pool.map(primo_3, invertido)
            resultados_2['Resultado 2'].append((time()*1000) - t)
            t = (time()*1000)
            pool.map(primo_3, aleatorio)
            resultados_2['Resultado 3'].append((time()*1000) - t)
            t = (time()*1000)
            pool.map(primo_3, aleatorio)
            resultados_2['Resultado 4'].append((time()*1000) - t)
    df1 = pd.DataFrame(data = resultados_1)
    df2 = pd.DataFrame(data = resultados_2)
    print(df1, '\n', df2)
    stat1, p1 = f_oneway(resultados_1['Prueba 1'],
                         resultados_1['Prueba 2'],
                         resultados_1['Prueba 3'],
                         resultados_1['Prueba 4'])
    print('Variando algoritmo\n', 'stat=%.3f, p=%.3f' % (stat1, p1))
    if p1 > 0.05:
        print('Estadísticamente no significativa\n')
    else:
        print('Estadísticamente significativa\n')
    stat2, p2 = f_oneway(resultados_2['Resultado 1'],
                         resultados_2['Resultado 2'],
                         resultados_2['Resultado 3'],
                         resultados_2['Resultado 4'])
    print('Variando orden de numeros\n', 'stat=%.3f, p=%.3f' % (stat2, p2))
    if p2 > 0.05:
        print('Estadísticamente no significativa\n')
    else:
        print('Estadísticamente significativa\n')
    
    sns.violinplot(data = df1, scale='count')
    plt.savefig('Prueba.png')
    plt.show()
    sns.violinplot(data = df2, scale='count')
    plt.savefig('Resultado.png')
    plt.show()


    
