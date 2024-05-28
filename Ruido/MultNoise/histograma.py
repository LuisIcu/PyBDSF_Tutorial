import random
import matplotlib.pyplot as plt
from astropy.convolution import convolve, AiryDisk2DKernel, Gaussian2DKernel
import numpy as np
from math import sqrt, log, fabs
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression

#----------Parámetros que vamos a usar-----------#
#1. Dimension de las matrices
B=150
gaussPSF = Gaussian2DKernel(5/(2*sqrt(2*log(2))))
#Matriz de ruido
#Noise = np.random.normal(0,2,size=(B,B))
#ConvNoise = convolve(Noise,gaussPSF)

def AjustarGaussiana(M):
    h = M[0]
    for i in range(1,len(M)):
        h = np.concatenate((h,M[i]),axis=None)

    count, bins, ignored =  plt.hist(h,50,density=True)
    #Ajuste de la función
    bin2 = np.delete(bins,len(bins)-1,0) + (bins[1]-bins[0])/2
    def model(x,a,b):
        return (1/np.sqrt(2*np.pi*a**2))*np.exp(-(x-b)**2/(2*a**2))
    parinc = [0.5,0.5]
    popt, pconv = curve_fit(model,bin2,count,p0=parinc)
    #x_modelo  = np.linspace(bins[0], bins[len(bins)-1], 200)
    #plt.plot(x_modelo, model(x_modelo, *popt), 'r-')

    sigma = round(popt[0],4)
    mu = round(popt[1],4)
    plt.close()
    return sigma, mu

'''sig, mu = AjustarGaussiana(Noise)
print(f'sigma = {sig}, mu = {mu}')
sig, mu = AjustarGaussiana(ConvNoise)
print(f'sigma = {sig}, mu = {mu}')'''

sigma = np.array([])

list_sig = np.arange(1,1+30)
Noise = np.random.normal(0,1,size=(B,B))
for s in list_sig:
    ConvNoise = s*Noise
    sig, mu = AjustarGaussiana(ConvNoise)
    sigma = np.append(sigma,fabs(sig))
print(sigma)

list_sig = list_sig.reshape((-1,1))
model = LinearRegression().fit(list_sig,sigma)
a = round(model.coef_[0],4)
b = round(model.intercept_,4)

plt.plot(list_sig,sigma,'r*',alpha=0.65,label = 'Pares de pixeles antes/después de la multiplicación')
x = np.linspace(0,30)
y = a*x+b 
plt.plot(x,y,'c--',label = f'Ajuste lineal\nm = {a}', linewidth = 1.5)
plt.legend()
plt.title('Cambio del ruido gaussiano después de la multiplicación')
plt.xlabel(r'Coeficiente de multiplicación')
plt.ylabel(r'$\sigma$ después de la multiplicación')
plt.savefig('./Imagenes/MultPlot.pdf',dpi=600,bbox_inches='tight')
#plt.show()
