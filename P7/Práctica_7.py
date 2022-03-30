import numpy as np
import math as ma
from matplotlib import cm
import matplotlib.pyplot as plt
from random import uniform
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt, fabs 
from cv2 import cv2
from matplotlib.ticker import LinearLocator, FormatStrFormatter

def g(x, y):
    return (1 - x/2 + x**5 + y**3) * np.exp(-x**2 - y**2)

low = -2.7
high = -low
step = 0.10

x = np.arange(low, high, step)
y = np.arange(low, high, step)
x, y = np.meshgrid(x, y)
z =(1 - x/2 + x**5 + y**3) * np.exp(-x**2 - y**2)

fig = plt.figure()
ax = fig.gca(projection='3d')
s = ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.01f'))
fig.colorbar(s, shrink=0.5, aspect=5)
plt.savefig("p7_3dinicial.png")
plt.show()
#[(xi,yd),(cx,yd),(xd,yd)]
#[(xi,cy),(cx,cy),(xd,cy)]
#[(xi,yi),(cx,yi),(xd,yi)]
def vecinos(vecindad):
    pos=[]
    for a in vecindad:
        pos.append((g(a[0],a[1]),a[0],a[1]))
    return(pos)

def movimientos(x, y, bx, by):
    pasos=[]
    listax,listay=[],[]
    listamxy=[]
    for s in range(puntos):
        mejorx,mejory=bx[0],by[0]
        cx, cy= x[s], y[s]
        Dx=uniform(0, step/3)
        Dy=uniform(0, step/3)
        xi, xd= (cx-Dx), (cx+Dx)
        yi, yd= (cy-Dy), (cy+Dy)
        xi = low if xi < low else xi
        xd = high if xd > high else xd
        yi = low if yi < low else yi
        yd = high if yd > high else yd
        vecindad=[(xi,yd),(cx,yd),(xd,yd),(xi,cy),(xd,cy),(xi,yi),(cx,yi),(xd,yi)]
        datos=vecinos(vecindad)
        pos,cx,cy= (max(datos))
        if pos > g(mejorx,mejory):
            mejorx, mejory=cx,cy
        else:
            mejorx, mejory= bx[0], by[0]
        pasos.append(((cx// step- low // step),(cy// step- low // step)))
        listax.append(cx)
        listay.append(cy)
        listamxy.append((g(mejorx, mejory),(mejorx// step- low // step),(mejory// step- low // step)))
    return(pasos,listax,listay,listamxy)
puntos= 5
ciclos= 500

posx = [uniform(low, high) for s in range(puntos)]
posy = [uniform(low, high)for s in range(puntos)]
bestx = posx
besty = posy

p = np.arange(low, high, step)
n = len(p)
z = np.zeros((n, n), dtype=float)
for i in range(n):
    x = p[i]
    for j in range(n):
        y = p[n - j - 1]  
        z[i, j] = g(x, y)
t = range(0, n, 5)
l = ['{:.1f}'.format(low + s * step) for s in t]
for img in range(ciclos):
    ps,posx,posy,best = movimientos(posx, posy, bestx,besty)


    ####### grafico
    best=(max(best))
    mejorx, mejory=best[1], best[2]
    fig, ax = plt.subplots(figsize=(-low, high), ncols=1)
    pos = ax.imshow(z)
    plt.xticks(t, l)
    plt.yticks(t, l)
    ax.scatter(ps[0][0],ps[0][1], marker='o', color='red', s=5)
    ax.scatter(ps[1][0],ps[1][1], marker='o', color='red', s=5)
    ax.scatter(ps[2][0],ps[2][1], marker='o', color='red', s=5)
    ax.scatter(ps[3][0],ps[3][1], marker='o', color='red', s=5)
    ax.scatter(ps[4][0],ps[4][1], marker='o', color='red', s=5)
    ax.scatter(mejorx, mejory, marker='x', color='black', s=15)
    fig.colorbar(pos, ax=ax)
    plt.title('{:d} paso'.format(img+1))
    if img in [50,100,200,350,450]:
        fig.savefig('p7p_{:d}.png'.format(img), bbox_inches='tight')
    plt.close()
