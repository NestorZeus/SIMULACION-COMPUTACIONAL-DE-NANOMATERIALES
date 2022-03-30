import numpy as np
import math as ma
from matplotlib import cm
import matplotlib.pyplot as plt
from random import uniform, choice, random
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt, fabs, exp
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
        mejorx,mejory=bx[s],by[s]
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
            mejorx, mejory= bx[s], by[s]
        pasos.append(((cx// step- low // step),(cy// step- low // step)))
        listax.append(cx)
        listay.append(cy)
        listamxy.append((g(mejorx, mejory),(mejorx// step- low // step),(mejory// step- low // step)))
    return(pasos,listax,listay,listamxy)

def mov_reto1(x, y, bx, by, temp):
    pasos=[]
    listax,listay=[],[]
    listamxy=[]
    for s in range(puntos):
        mejorx,mejory=bx[s],by[s]
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
        for k in range(len(vecindad)):
            xnew,ynew = choice(vecindad)
            vecindad.remove((xnew,ynew))
            delta= g(xnew,ynew) - g(cx,cy)
            probabilidad= exp(delta/temp)
            if delta > 0:
                cx, cy=xnew, ynew        
                break
            else:
                if random() < (probabilidad):
                    cx, cy=xnew, ynew        
                    temp=(temp*(0.995))
                    break
                else:
                    cx, cy = cx, cy
        if g(cx, cy) > g(mejorx,mejory):
            mejorx, mejory=cx,cy
        else:
            mejorx, mejory= bx[s], by[s]
        pasos.append(((cx// step- low // step),(cy// step- low // step)))
        listax.append(cx)
        listay.append(cy)
        listamxy.append((g(mejorx, mejory),(mejorx// step- low // step),(mejory// step- low // step)))
    return(pasos,listax,listay,listamxy,temp)


puntos= 5
iteraciones= (100,500,1000)
replicas=1000

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


CB_est=[]
for f in iteraciones:
    estimados=[]
    for r in range(replicas):
        posx = [uniform(low, high) for s in range(puntos)]
        posy = [uniform(low, high)for s in range(puntos)]
        bestx = posx
        besty = posy
        for img in range(f):
            ps,posx,posy,best = movimientos(posx, posy, bestx,besty)
            if img==(f-1):
                mejor=max(best)
                estimados.append(mejor[0])
    CB_est.append(estimados)
plt.boxplot([CB_est[0], CB_est[1], CB_est[2]])
plt.xlabel('iteraciones')
plt.ylabel('Posiciones finales maximizadas')
plt.xticks([1,2,3], ['50','100','500'])
plt.show()

prom_1=(sum(CB_est[0])/(len(CB_est[0])))
prom_2=(sum(CB_est[1])/(len(CB_est[1])))
prom_3=(sum(CB_est[2])/(len(CB_est[2])))

plt.axhline(1.04, 0, 4, color="black")
plt.text(1, 1.04, 'Óptimo')
plt.bar(0, prom_1, color='blue', label='n=50')
plt.bar(1, prom_2, color='red', label='n=100')
plt.bar(2, prom_3, color='green', label='n=500')
plt.xlabel('iteraciones')
plt.ylabel('Promedio posiciones finales maximizadas')
plt.xticks([0,1,2], ['50','100','500'])
plt.legend()
plt.show()


iteraciones= (100,500,1000)
CB_est2=[]
for f in iteraciones:
    estimados2=[]
    for r in range(replicas):
        posx = [uniform(low, high) for s in range(puntos)]
        posy = [uniform(low, high)for s in range(puntos)]
        bestx = posx
        besty = posy
        temperatura=1000
        for img in range(f):
            ps,posx,posy,best,temperatura = mov_reto1(posx, posy, bestx,besty, temperatura)
            if img==(f-1):
                mejor=max(best)
                estimados2.append(mejor[0])
    CB_est2.append(estimados2)
plt.boxplot([CB_est2[0], CB_est2[1], CB_est2[2]])
plt.xlabel('iteraciones')
plt.ylabel('Posiciones finales maximizadas')
plt.xticks([1,2,3], ['100','500','1000'])
plt.show()

prom_4=(sum(CB_est2[0])/(len(CB_est2[0])))
prom_5=(sum(CB_est2[1])/(len(CB_est2[1])))
prom_6=(sum(CB_est2[2])/(len(CB_est2[2])))

plt.axhline(1.04, 0, 4, color="black")
plt.text(1, 1.04, 'Óptimo')
plt.bar(0, prom_4, color='blue', label='n=100')
plt.bar(1, prom_5, color='red', label='n=500')
plt.bar(2, prom_6, color='green', label='n=1000')
plt.xlabel('iteraciones')
plt.ylabel('Promedio posiciones finales maximizadas')
plt.xticks([0,1,2], ['100','500','1000'])
plt.legend()
plt.show()

##### barras  
N = 3
ind = np.arange(N) 
width = 0.2
plt.axhline(1.04, 0, 4, color="black")
xvals = [prom_1, prom_2, prom_3]
bar1 = plt.bar(ind, xvals, width, color = 'r')
yvals = [prom_4, prom_5, prom_6]
bar2 = plt.bar(ind+width, yvals, width, color='g')
plt.text(1, 1.04, 'Óptimo')
plt.xlabel("Iteraciones")
plt.ylabel('Promedios de maximos alcanzados')
plt.xticks(ind+width,['100', '500', '1000'])
plt.legend( (bar1, bar2), ('Mejor vecino', 'Vecino azar'), title='Método analizado')
plt.show()
