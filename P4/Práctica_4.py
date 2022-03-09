import seaborn as sns
from math import sqrt
from PIL import Image, ImageColor
from random import randint, choice
import matplotlib.pyplot as plt
import numpy as np

def celda(pos):
    if pos in semillas:
        return semillas.index(pos)
    x, y = pos % n, pos // n
    cercano = None
    menor = n * sqrt(2)
    for i in range(k):
        (xs, ys) = semillas[i]
        dx, dy = x - xs, y - ys
        dist = sqrt(dx**2 + dy**2)
        if dist < menor:
            cercano, menor = i, dist
    return cercano
 
def inicio():
    direccion = randint(0, 3)
    if direccion == 0: # vertical abajo -> arriba
        return (0, randint(0, n - 1))
    elif direccion == 1: # izq. -> der
        return (randint(0, n - 1), 0)
    elif direccion == 2: # der. -> izq.
        return (randint(0, n - 1), n - 1)
    else:
        return (n - 1, randint(0, n - 1))

 
def propaga(replica,rupturas):
    grieta = voronoi.copy()
    for f in range(rupturas):
        prob, dificil = 0.9, 0.8
        #grieta = voronoi.copy()
        g = grieta.load()
        (x, y) = inicio()
        largo = 0
        cnt=0
        if f == 0:
            color=(0,0,0)# grieta color negro
        if f == 1:
            color = (0, 0, 255)# color azul de grieta para el segundo ciclo
        while True:
            g[x, y] = color
            largo += 1
            frontera, interior = [], []
            for v in vecinos:
                (dx, dy) = v
                vx, vy = x + dx, y + dy
                if vx >= 0 and vx < n and vy >= 0 and vy < n: # existe
                   if g[vx, vy] != color: # no tiene grieta por el momento
                       if vor[vx, vy] == vor[x, y]: # misma celda
                           interior.append(v)
                       else:
                           frontera.append(v)
                   if f == 1:
                       if g[vx, vy]==(0,0,0):
                           cnt=1
                           g[vx, vy]=(0,255,0)
                           break      
            if cnt == 1:
                visual = grieta.resize((10 * n,10 * n))
                contacto.append([vx, vy])
                break
            elegido = None
            if len(frontera) > 0:
                elegido = choice(frontera)
                prob = 1
            elif len(interior) > 0:
                elegido = choice(interior)
                prob *= dificil
            if elegido is not None:
                (dx, dy) = elegido
                x, y = x + dx, y + dy
            else:
                break # ya no se propaga
        if largo >= limite:
            visual = grieta.resize((10 * n,10 * n))
    #plt.imshow(grieta)
    #plt.show()
    return (contacto)



prob = {"min_sem": [], "med_sem": [], "max_sem": []}
for n in 50, 150:
    semillas = []
    print("################# dimension",n,"###################")
    ciclos=0
    for k in 5, 80, 250:
        ciclos=ciclos+1
        print("########## semillas",k,"##############")
        for s in range(k):
            while True:
                x, y = randint(0, n - 1), randint(0, n - 1)
                if (x, y) not in semillas:
                    semillas.append((x, y))
                    break
 
        celdas = [celda(i) for i in range(n * n)]
        voronoi = Image.new('RGB', (n, n))
        vor = voronoi.load()
        c = sns.color_palette("Set3", k).as_hex()
        for i in range(n * n):
            vor[i % n, i // n] = ImageColor.getrgb(c[celdas.pop(0)])
        limite, vecinos = 1, []

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx != 0 or dy != 0:
                    vecinos.append((dx, dy))

        rupturas=2# cantidad de grietas
        contacto=[]
        for r in range(300): # replicas
            atraveso = propaga(r,rupturas)
            #print("Por replica:",r, "resultado:",atraveso)
        print("cuantos atravesaron",len(atraveso))
        if ciclos == 1:
            prob["min_sem"].append(((len(atraveso))/300)*100)
        if ciclos == 2:
            prob["med_sem"].append(((len(atraveso))/300)*100)
        if ciclos == 3:
            prob["max_sem"].append(((len(atraveso))/300)*100)
    print("final de probabilidades",prob)

linea1= [prob["min_sem"][0], prob["med_sem"][0], prob["max_sem"][0]]
linea2= [prob["min_sem"][1], prob["med_sem"][1], prob["max_sem"][1]]
plt.plot(np.arange(len(linea1)),linea1, color='red', label='n=50')
plt.scatter(np.arange(len(linea1)),linea1, color='black')
plt.plot(np.arange(len(linea2)),linea2, color='blue', label='n=150')
plt.scatter(np.arange(len(linea2)),linea2, color='black')
plt.xlabel('semillas')
plt.xticks([0,1,2],['5','80','250'])
plt.ylabel('Probabilidad de choque en grietas (%)')
plt.legend()
plt.show()

import plotly.graph_objects as go
categories = ['5 semillas','80 semillas','250 semillas']
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
      r=linea1,
      theta=categories,
      fill=None,
      name='n= 50'
))
fig.add_trace(go.Scatterpolar(
      r=linea2,
      theta=categories,
      fill=None,
      name='n= 150'
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 60]
    )),
  showlegend=True
)

fig.show()




    
