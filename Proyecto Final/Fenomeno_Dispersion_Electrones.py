import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from math import floor, log, sqrt

planos=1
n=8
electronX=[random.randint(0,35) for i in range(n)]
electronY=[150 for i in range(n)]
electronC=[4 for i in range(n)]
planoX= [i for i in range(5,35,5)]*planos
planoY= [90 for i in range(6)]* planos
atomoP= [25 for i in range(6)]*planos
atomoN= [10 for i in range(6)]*planos

paso=0
cambio=0
digitos = floor(log(50, 10)) + 1
for t in range(50):
    electrones= list(zip(electronX,electronY))
    atomos=list(zip(planoX, planoY))
    EC=0
    cntmas=.05
    for xi, yi in electrones:
        for xf, yf in atomos:
            distancia =sqrt(((xf-xi)**2)+((yf-yi)**2))
            if distancia < 10:
                if xi > xf:
                    electronX[EC] = electronX[EC]+cntmas
                    cambio=cambio+1
                else:
                    electronX[EC] = electronX[EC]-cntmas
                    cambio=cambio+1
            else:
                if cambio > 0:
                    if xi > xf:
                        electronX[EC] = electronX[EC]+cntmas
                    else:
                        electronX[EC] = electronX[EC]-cntmas
                
        electronY[EC]=electronY[EC]-paso
        EC=EC+1
    plt.xlim(-15, 55)
    plt.ylim(0, 160)
    plt.scatter(electronX, electronY, s=electronC, color='blue')
    plt.scatter(planoX, planoY, s=atomoP, color='red')
    plt.title('Paso {:d}'.format(t + 1))
    plt.savefig('p9p_t' + format(t + 1, '0{:d}'.format(digitos)) + '.png')
    paso=3



    
