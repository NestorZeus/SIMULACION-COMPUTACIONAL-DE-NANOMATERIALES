from random import randint, choice
from PIL import Image, ImageColor, ImageDraw
from matplotlib import pyplot as plt, patches
import numpy as np
import seaborn as sns
from math import sqrt
import random

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
                           #g[vx, vy]=(0,255,0)
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

def union(seeds,im,incr):
    for a in range(len(seeds)):
        x=seeds[a][0]
        y=seeds[a][1]
        r = incr[a]
        color=im.getpixel((x, y))
        img=im.copy()
        image = img
        draw = ImageDraw.Draw(image)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=color)
        for Y in range(n):
            for X in range(n):
                nueva=image.getpixel((X,Y))
                orig= im.getpixel((X, Y))
                if nueva == color:
                    if orig != (0,0,0) and orig != color:
                        image.putpixel((X,Y),orig)
                if nueva != (0,0,0):
                    if X > 0 and X < (n-1) and Y > 0 and Y < (n-1):
                        #print('Fue diferente',X,Y)
                        V= []
                        for dx in range(X-1, X+2):
                            for dy in range(Y-1, Y+2):
                                V.append(image.getpixel((dx,dy)))
                        V.pop(4)
                        if(all([u != nueva and u !=(0,0,0) for u in V]))== True:
                            #print(V)
                            image.putpixel((X,Y),(V[0]))
        im=image
    #plt.title('termina funcion')
    #plt.imshow(image)
    #plt.show()
    return(image)

prob = {"min_sem": [], "med_sem": [], "max_sem": []}
for n in 50, 60, 70, 80:
    print("################# dimension",n,"###################")
    ciclos=0
    for k in 5, 80, 250:
        semillas = []
        ciclos=ciclos+1
        print("########## semillas",k,"##############")
        voronoi = Image.new('RGB', (n, n))
        vor = voronoi.load()
        paleta = sns.color_palette("Set1", k)
        for s in range(k):
            while True:
                x, y = randint(0, n - 1), randint(0, n - 1)
                if (x, y) not in semillas:
                    semillas.append((x, y))
                    break
        col=[]
        for dato in paleta:
            col.append([(int(i * 255)) for i in dato])
########### ############
        for i in range(len(semillas)):
            voronoi.putpixel(semillas[i],(tuple(col[i])))
        #plt.imshow(voronoi)###### IMPRIMIR
        #plt.show()
        #vo=voronoi.copy()
        #visual = vo.resize((10 * n,10 * n))
        #visual.save("ciclo_0_ini.png")
        p=0.4
        aumento=[]
        semi=[]
        for s in range(n):
            #fondo=[]
            #print("######## ciclo:",s)
            if s == 0:
                semi.append(semillas[0])
                semillas.pop(s)
                aumento.append(0)
            if s != 0 and ((random.uniform(0, 1)) > p) and len(semillas)>0:
                rnd=random.choice(semillas)
                semi.append(rnd)
                semillas.remove(rnd)
                aumento.append(0)
            aumento=[s+1 for s in aumento]
            voronoi= union(semi,voronoi,aumento)
            #[[fondo.append(voronoi.getpixel((x,y))) for x in range(5)]for y in range(5)]
            #vis=voronoi.copy()
            #visual = vis.resize((10 * n,10 * n))
            #visual.save("ciclo_{:d}.png".format(s))
            #plt.imshow(voronoi)
            #plt.show()
        #plt.imshow(voronoi)####### IMPRIMIR
        #plt.show()###############
##################################################
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
linea3= [prob["min_sem"][2], prob["med_sem"][2], prob["max_sem"][2]]
linea4= [prob["min_sem"][3], prob["med_sem"][3], prob["max_sem"][3]]

plt.plot(np.arange(len(linea1)),linea1, color='red', label='n=50')
plt.scatter(np.arange(len(linea1)),linea1, color='black')
plt.plot(np.arange(len(linea2)),linea2, color='blue', label='n=60')
plt.scatter(np.arange(len(linea2)),linea2, color='black')
plt.plot(np.arange(len(linea3)),linea3, color='green', label='n=70')
plt.scatter(np.arange(len(linea3)),linea3, color='black')
plt.plot(np.arange(len(linea4)),linea4, color='yellow', label='n=80')
plt.scatter(np.arange(len(linea4)),linea4, color='black')

plt.xlabel('semillas')
plt.xticks([0,1,2],['5','80','250'])
plt.ylabel('Probabilidad de choque en grietas (%)')
plt.legend(title="Dimensiones")
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
      name='n= 60'
))
fig.add_trace(go.Scatterpolar(
      r=linea3,
      theta=categories,
      fill=None,
      name='n= 70'
))
fig.add_trace(go.Scatterpolar(
      r=linea4,
      theta=categories,
      fill=None,
      name='n= 80'
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
































