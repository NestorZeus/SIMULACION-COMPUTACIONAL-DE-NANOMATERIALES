import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from math import floor, log, sqrt
import statistics
##muestras=100,1000,5000#electrones
muestras=100,500,1000
F = (2, 5, 8, 12, 15, 20)
Pd=.5
pasomax=1
rep=25
digitos = floor(log(50, 10)) + 1
N_data=[]
for n in muestras:
    CV=[]
    for Fuerza in F:
        PORC=[]
        for replicas in range(rep):
            electronX=[random.uniform(0,180) for i in range(n)]
            electronY=[115 for i in range(n)]
            planoX= [i for i in range(5,170,40)]
            planoY= [80 for i in range(len(planoX))]
            atomoP= [25 for i in range(len(planoX))]
            C=[]
            paso=0
            for t in range(100):
                electrones= list(zip(electronX,electronY))
                atomos=list(zip(planoX, planoY))
                cambioE=0
                E=[]
                for xi, yi in electrones:
                    A=[]
                    electronY[cambioE]=electronY[cambioE]-paso
                    if t<37:
                        for xf, yf in atomos: 
                            distancia =sqrt(((xf-xi)**2)+((yf-yi)**2))
                            if distancia <= Fuerza and yi>=yf:# si entra a un rango cerca al atomo
                                desvio=(pasomax/Fuerza)*(Fuerza-distancia)
                                if (random.uniform(0,1))<Pd:# si la probabilidad es menor dispersa
                                    if xi >= xf:
                                        electronX[cambioE]=electronX[cambioE]-desvio
                                        A.append('I')
                                    if xi < xf:
                                        electronX[cambioE]=electronX[cambioE]+desvio
                                        A.append('D')
                                else:
                                    A.append(0)
                            else:
                                A.append(0)
                        E.append(A)
                    cambioE=cambioE+1
                C.append(E)
                if t >= 36: # fue el ultimo paso donde sufrio efecto de dispersion
                    if t>36:
                        electronX=electronX2
                        E=E2
                    dispersion=0
                    for e in E:
                        if 'I' in e:
                            electronX[dispersion]=electronX[dispersion]-1
                            I=1
                        if 'D' in e:
                            electronX[dispersion]=electronX[dispersion]+1
                            D=1
                
                        dispersion=dispersion+1
                    electronX2=electronX
                    E2=E
##    plt.scatter(electronX, electronY, s=1, color='blue')
##    plt.scatter(planoX, planoY, s=atomoP, color='red')
##    plt.title('Paso {:d}'.format(t + 1))
##    plt.savefig('p9p_t' + format(t + 1, '0{:d}'.format(digitos)) + '.png')
                paso=1
            guarda=[]
            for i in electronX:
                if i < 5 or i > 170:
                    guarda.append(i)
            porcentaje= (len(guarda)*100)/n
            PORC.append(porcentaje)
        CV.append(statistics.mean(PORC))
    N_data.append(CV)
print(N_data)

## para graficos
F1,F2,F3,F4,F5,F6=[],[],[],[],[],[]
for i in N_data:
    cnt=0
    for j in i:
        if cnt==0:
            F1.append(j)
        if cnt==1:
            F2.append(j)
        if cnt==2:
            F3.append(j)
        if cnt==3:
            F4.append(j)
        if cnt==4:
            F5.append(j)
        if cnt==5:
            F6.append(j)
        cnt=cnt+1

barWidth = 0.15
fig = plt.subplots(figsize =(12, 8))

br1 = np.arange(len(F1))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
br5 = [x + barWidth for x in br4]
br6 = [x + barWidth for x in br5]
 
plt.bar(br1, F1, color ='r', width = barWidth,
        edgecolor ='grey', label ='2')
plt.bar(br2, F2, color ='g', width = barWidth,
        edgecolor ='grey', label ='5')
plt.bar(br3, F3, color ='b', width = barWidth,
        edgecolor ='grey', label ='8')
plt.bar(br4, F4, color ='y', width = barWidth,
        edgecolor ='grey', label ='12')
plt.bar(br5, F5, color ='purple', width = barWidth,
        edgecolor ='grey', label ='15')
plt.bar(br6, F6, color ='brown', width = barWidth,
        edgecolor ='grey', label ='20')
plt.xlabel('Cantidad de electrones', fontweight ='bold', fontsize = 15)
plt.ylabel('Promedio de dispersiones (%)', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(F1))],
        ['100', '500', '700'])
plt.legend(title='Tamaño de atomo')
plt.show()
