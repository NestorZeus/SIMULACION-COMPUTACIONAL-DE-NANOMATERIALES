import numpy as np
import pandas as pd
from random import uniform 
import matplotlib.pyplot as plt
import matplotlib.colorbar as colorbar
from matplotlib.colors import LinearSegmentedColormap
import math


paso = 256 // 10
niveles = [i/256 for i in range(0, 256, paso)]
colores = [(niveles[i], 0, niveles[-(i + 1)]) for i in range(len(niveles))]
palette = LinearSegmentedColormap.from_list('tonos', colores, N = len(colores))
 
from math import fabs, sqrt, floor, log
eps = 0.001
def fuerza(i, shared):
    p = shared.data
    n = shared.count
    pi = p.iloc[i]
    xi = pi.x
    yi = pi.y
    ci = pi.c
    mi = pi.masa
    fx, fy = 0, 0
    for k in range(n):
        pk = p.iloc[k]

        ck = pk.c
        mk = pk.masa

        dire_c = (-1)**(1 + (ci * ck < 0))
        dire_m = (-1)**(1 + (mi * mk > 0))

        dx = xi - pk.x
        dy = yi - pk.y

        factor_c = dire_c * fabs(ci - ck) / (sqrt(dx**2 + dy**2) + eps)
        factor_m = dire_m * fabs(mi - mk) / (sqrt(dx**2 + dy**2) + eps)

        fx -= dx * factor_m * factor_c
        fy -= dy * factor_m * factor_c
    return (fx, fy)
 
from os import popen
 
def actualiza(pos, fuerza, de):
    return max(min(pos + de * fuerza, 1), 0)

import multiprocessing
from itertools import repeat
import itertools
if __name__ == "__main__":
    inicial=[]
    popen('rm -f p9p_t*.png') # borramos anteriores en el caso que lo hayamos corrido
    n = 25
    x = np.random.normal(size = n)
    y = np.random.normal(size = n)
    masa = [uniform(0,50)for i in range(n)]
    c = np.random.normal(size = n)
    #masa=[s * (-1) for s in masa]
    
    xmax = max(x)
    xmin = min(x)
    x = (x - xmin) / (xmax - xmin) # de 0 a 1

    ymax = max(y)
    ymin = min(y)
    y = (y - ymin) / (ymax - ymin) 

    cmax = max(c)
    cmin = min(c)
    c = 2 * (c - cmin) / (cmax - cmin) - 1 # entre -1 y 1

    g = np.round(5 * c).astype(int)
    p = pd.DataFrame({'x': x, 'y': y, 'c': c, 'g': g, 'masa': masa})
    mgr = multiprocessing.Manager() # https://stackoverflow.com/questions/22487296/multiprocessing-in-python-sharing-large-object-e-g-pandas-dataframe-between
    ns = mgr.Namespace()
    ns.data = p # compartido entre el pool
    ns.count = n 
    tmax = 20
    digitos = floor(log(tmax, 10)) + 1
    fig, ax = plt.subplots(figsize=(6, 5), ncols=1)
    pos = plt.scatter(p.x, p.y, c = p.g, s = p.masa*10, marker = 'o', cmap = palette)
    fig.colorbar(pos, ax=ax)
    plt.title('Estado inicial')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)
    fig.savefig('p9p_t0.png')
    plt.close()
    for s in range(n):
        inicial.append((p.x[s],p.y[s]))
    velocidad=[]
    for t in range(tmax):
        with multiprocessing.Pool() as pool: # rehacer para que vea cambios en p
            f = pool.starmap(fuerza, [(i, ns) for i in range(n)])
            delta = 0.02 / max([max(fabs(fx), fabs(fy)) for (fx, fy) in f])
            p['x'] = pool.starmap(actualiza, zip(p.x, [v[0] for v in f], repeat(delta)))
            p['y'] = pool.starmap(actualiza, zip(p.y, [v[1] for v in f], repeat(delta)))
            movimiento=[]
            for s in range(n):
                movimiento.append((p.x[s],p.y[s]))
            part_mov=[]
            for vel in range(n):
                ini, mov= inicial[vel], movimiento[vel]
                Dx = ini[0] - mov[0]
                Dy = ini[1] - mov[1]
                part_mov.append(sqrt(Dx**2 + Dy**2))
            velocidad.append(part_mov)
            inicial= movimiento 
            fig, ax = plt.subplots(figsize=(6, 5), ncols=1)
            pos = plt.scatter(p.x, p.y, c = p.g, s = p.masa*10, marker = 'o', cmap = palette)
            fig.colorbar(pos, ax=ax)
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.xlim(-0.1, 1.1)
            plt.ylim(-0.1, 1.1)            
            plt.title('Paso {:d}'.format(t + 1))
            fig.savefig('p9p_t' + format(t + 1, '0{:d}'.format(digitos)) + '.png')
            plt.close()

#########################
    datos={
       'carga': c,
       'masa': masa,
       'velocidad':velocidad[0]}
    df = pd.DataFrame(datos)
    df = df.sort_values(by='velocidad', ascending=True)
    print(df)
    x= df.loc[:,"carga"] 
    y= df.loc[:,"masa"] 
    z= df.loc[:,"velocidad"] 
    plt.figure()
    ax=plt.axes(projection ='3d')
    ax.scatter3D(x, y, z, s=15, color="red")
    ax.set_xlabel('Carga', fontweight ='bold')
    ax.set_ylabel('Masa', fontweight ='bold')
    ax.set_zlabel('Velocidad', fontweight ='bold')
    plt.show()

    t = x
    data1 = y
    data2 = z
       
    fig, ax1 = plt.subplots()
   
    color = 'tab:blue'
    ax1.set_xlabel('CARGA')
    ax1.set_ylabel('MASA', color = color)
    ax1.scatter(t, data1, color = color)
    ax1.tick_params(axis ='y', labelcolor = color)
   
    ax2 = ax1.twinx()
       
    color = 'tab:green'
    ax2.set_ylabel('VELOCIDAD', color = color)
    ax2.scatter(t, data2, color = color)
    ax2.tick_params(axis ='y', labelcolor = color)

    plt.show()
### Correlación entre variables
    cor = df.corr()
    xi = 'carga'
    yi = 'masa'
    zi = 'velocidad'

    xz = cor.loc[ xi, zi ]
    yz = cor.loc[ yi, zi ]
    xy = cor.loc[ xi, yi ]

    Rxyz = math.sqrt((abs(xz**2) + abs(yz**2) - 2*xz*yz*xy) / (1-abs(xy**2)) )
    R2 = Rxyz**2
    
    n = len(df) # Number of rows
    k = 2       # Number of independent variables
    R2_adj = 1 - ( ((1-R2)*(n-1)) / (n-k-1) )
    print("relacion entre la velocidad con carga y velocidad con masa",R2_adj)
### Correlación de rango de Spearman
    from scipy.stats import spearmanr
    stat, p = spearmanr(x, z)
    print("correlacion carga con velocidad")
    print('stat=%.3f, p=%.3f' % (stat, p))
    if p > 0.05:
        print('Probablemente dependiente')
    else:
        print('Probablemente independiente')

    print("correlacion masa con velocidad")
    stat2, p2 = spearmanr(y, z)
    print('stat=%.3f, p=%.3f' % (stat2, p2))
    if p2 > 0.05:
        print('Probablemente dependiente')
    else:
        print('Probablemente independiente')
