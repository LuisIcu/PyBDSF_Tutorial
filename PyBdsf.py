# PyBdsf.py
# Realizado por Luis Fernando Icú
# Email: luisfer200010@gmail.com 
# GitHub: https://github.com/LuisIcu/PyBDSF_Tutorial
#
# Este script hace uso de la librería PyBDSF para analizar archivos .fits de mapas astronómicos y mediante ajustes gaussianos
# hallar fuentes en ellas.
# Al ejecutar el archivo será necesario ingresar el nombre del .fits (sin la extensión) y el nombre de salida.
# El script crea una carpeta con el nombre de salida donde guarda los siguientes archivos:
# -Un fits de 5 extensiones donde se encuentran:
#   -Mapa original.
#   -Mapa booleano: los pixeles pueden tomar valores 1 o 0, 1 para cuando ahí se encuentra una fuente y 0 cuando no la haya.
#   -Modelo gaussiano: Las fuentes gaussianas aisladas.
#   -Residuo gaussiano: el ruido de fondo, al omitir las fuentes.
#   -Mapa de RMS: Mapa cuantificado del ruido de confusión del fondo mediante la raiz cuadrática media (RMS por sus siglas en inglés).
# -Archivo .csv de 47 columnas con el nombre \textit{prov.csv}.
# -Archivo .csv con algunas columnas de interés:
#   -Isl_id: Número de isla.
#   -RA: Ascención recta.
#   -DEC: Declinación.
#   -Peak_Flux: Flujo en el pico.
#   -E\_Peak_Flux: Error del flujo en el pico.
#   -Maj: Eje mayor del beam.
#   -Min: Eje menor del beam.
#   -S_Code: Código que indica si la fuente es única en su isla.
# NOTA: para ejecutar el script el archivo .fits debe estar en la misma carpeta que el script. Si ya existe una carpeta con el nombre 
# de salida se genera un error y no ejecuta nada.
#
# Al ejecutar en la terminal se ve así:
# python3 PyBdsf.py
# Ingresar nombre del fits: NombreEntrada
# Ingresar nombre de salida: NombreSalida

import bdsf
import pandas as pd
import os 
from astropy.io import fits

def PyBdsf(FitsName:str,OutName:str):
    os.mkdir('./'+OutName)
    filename = FitsName + '.fits' 

    #Procesamos la imagen
    img = bdsf.process_image(
        filename,
        frequency=2.72e11,
        beam=(0.0016,0.0016,0),
        adaptive_rms_box=True    
    )

    #img.show_fit()

    #Creamos cada uno de los archivos fits y los juntamos en uno solo
    Images = ['ch0','island_mask','gaus_model','gaus_resid','rms']
    for image in Images:
        img.export_image(
            img_format = 'fits',
            img_type = image,
            outfile = image + '.fits',
            clobber = True
        )
    
    ch0 = fits.open('ch0.fits')
    island_mask = fits.open('island_mask.fits')
    gaus_model = fits.open('gaus_model.fits')
    gaus_resid = fits.open('gaus_resid.fits')
    rms = fits.open('rms.fits')

    hdul = fits.HDUList()
    hdul.append(ch0[0])
    hdul.append(island_mask[0])
    hdul.append(gaus_model[0])
    hdul.append(gaus_resid[0])
    hdul.append(rms[0])
    for i in range(1,len(Images)):
        hdul[i].name = Images[i]

    #Escribimos el catálogo
    img.write_catalog(
        outfile = 'prov.csv',
        format = 'csv',
        clobber = True
    )

    #Esto escribe el archivo prov.csv, de ahí seleccionamos las columnas que nos interesan
    #y las escribimos en otro archivo. Luego eliminamos el archivo prov y luego movemos todo
    #lo que creamos a una carpeta que se crea con el mismo nombre
    usecols = [' Isl_id',' RA',' DEC',' Peak_flux',' E_Peak_flux',' Maj',' Min', ' S_Code']
    map_data = pd.read_csv('./prov.csv',usecols=usecols,skiprows=5)
    map_data.to_csv(OutName+'.csv')

    #os.remove('prov.csv')
    for image in Images:
        os.remove(image + '.fits')

    hdul.writeto('./' + OutName + '/' + OutName + '.fits')
    os.rename('./'+OutName+'.csv','./'+OutName+'/'+OutName+'.csv')
    os.rename('./'+FitsName+'.fits.pybdsf.log','./'+OutName+'/'+FitsName+'.fits.pybdsf.log')
    os.rename('./prov.csv','./'+ OutName + '/prov.csv')



FitsName = input('Ingresar nombre del fits: ')
OutName = input('Ingresar nombre de salida: ')

#PyBdsf('MultDist1','Multi1')
PyBdsf(FitsName,OutName)

