import random
import matplotlib.pyplot as plt
from astropy.convolution import convolve, AiryDisk2DKernel, Gaussian2DKernel
import numpy as np
from math import sqrt, log
from scipy.optimize import curve_fit

#----------Parámetros que vamos a usar-----------#
#1. Dimension de las matrices
B=150
p=12
gaussPSF = Gaussian2DKernel(5/(2*sqrt(2*log(2))))
#Matriz de ruido
Noise = np.random.normal(0,1,size=(B,B))
ConvNoise = p*Noise

def AjustarGaussiana(M,titulo:str,output:str):
    h = M[0]
    for i in range(1,len(M)):
        h = np.concatenate((h,M[i]),axis=None)

    count, bins, ignored =  plt.hist(h,50,density=True,label='Histo ruido')
    #Ajuste de la función
    bin2 = np.delete(bins,len(bins)-1,0) + (bins[1]-bins[0])/2
    def model(x,a,b):
        return (1/np.sqrt(2*np.pi*a**2))*np.exp(-(x-b)**2/(2*a**2))
    parinc = [0.5,0.5]
    popt, pconv = curve_fit(model,bin2,count,p0=parinc)

    sigma = round(popt[0],4)
    mu = round(popt[1],4)

    x_modelo  = np.linspace(bins[0], bins[len(bins)-1], 200)
    plt.plot(x_modelo, model(x_modelo, *popt), 'r-')
    #plt.plot(x_modelo, model(x_modelo, k,0), 'r-')

    plt.text(bin2[int(len(bin2)*0.85)],0.9*np.amax(count),
             r'Parámetros:' +'\n' +'$\sigma$ = ' + str(sigma) + '\n'+ r'$\mu$ = ' + str(mu) )
    #plt.text(-6,0.1,r'$\mu$ = ' + str(popt[1]))

    #Guardar figura y ajuste
    plt.xlabel('Valor del ruido')
    plt.ylabel('Conteo')
    plt.title(titulo)
    plt.savefig(f'./Imagenes/{output}.pdf',dpi=600,bbox_inches='tight')
    #plt.show()
    plt.close()
    return sigma, mu


s, m = AjustarGaussiana(Noise,'Histograma de ruido','historuido')
sc, mc = AjustarGaussiana(ConvNoise,'Histograma de ruido multiplicado','histoconv')

file = open('./Imagenes/data.txt','w')
file.write(
    'Parámetros para el ruido:' + '\n' +
    r'$\sigma$ = ' + f'{s}' + '\n' +
    r'$\mu$ = ' + f'{m}' + '\n' +
    'Parámetros para el ruido de la matriz convolucionada:' + '\n' +
    r'$\sigma$ = ' + f'{sc}' + '\n' +
    r'$\mu$ = ' + f'{mc}' + '\n' +
    f'La variación entre la desviación antes y después de la multiplicación es: {sc/s}'
)

