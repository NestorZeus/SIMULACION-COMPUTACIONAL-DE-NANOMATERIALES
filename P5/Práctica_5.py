from math import exp, pi
import pylab
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.options.display.float_format = "{:,.18f}".format

wolfram = 0.048834111126049311
desde = 2
hasta = 5
pedazo = 50000
cuantos = [500, 5000, 50000]
puntos = []
ae = []
se = []
dec = []

def g(x):
    return (2  / (pi * (exp(x) + exp(-x))))

vg = np.vectorize(g)
X = np.arange(-8, 8, 0.05)
Y = vg(X)
 
from GeneralRandom import GeneralRandom
generador = GeneralRandom(np.asarray(X), np.asarray(Y))

def parte(replica):
    V = generador.random(pedazo)[0]
    return ((V >= desde) & (V <= hasta)).sum()

def compare_strings(a, b):
    a = str(a)
    b = str(b)
    
    if a is None or b is None:
        return 0
    
    size = min(len(a), len(b))
    count = 0

    for i in range(size):
        if a[i] == b[i]:
            count += 1
        else:
            break
    return count
 
import multiprocessing
if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        for c in cuantos:
            p = c * pedazo
            puntos.append('{:.1e}'.format(p))
            montecarlo = pool.map(parte, range(c))
            integral = sum(montecarlo) / p
            valor = (pi / 2) * integral
            ae.append(abs(valor - wolfram))
            se.append(((valor - wolfram)**2))
            dec.append(compare_strings(wolfram, valor) - 2)
        resultados = {'Iteraciones': puntos,
                      'Error Absoluto': ae,
                      'Error Cuadrado': se,
                      'Decimales Correctos': dec}
        df = pd.DataFrame(resultados)
        sns.barplot(data=df, x='Iteraciones',
                    y='Error Absoluto',
                    dodge=False)
        plt.savefig('AbsErr.png')

        plt.show()
        sns.barplot(data=df, x='Iteraciones',
                    y='Error Cuadrado',
                    dodge=False)
        plt.savefig('SqErr.png')
        plt.show()
        sns.barplot(data=df, x='Iteraciones',
                    y='Decimales Correctos',
                    dodge=False)
        plt.savefig('Decimals.png')
        plt.show()
        print(df)
