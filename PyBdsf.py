import bdsf
import pandas as pd
import os 
from astropy.io import fits

def PyBdsf(FitsName:str,OutName:str):
    filename = FitsName + '.fits' 

    #Procesamos la imagen
    img = bdsf.process_image(
        filename,
        frequency=2.72e11,
        beam=(0.0016,0.0016,0),
        adaptive_rms_box=True    
    )

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
    usecols = ['# Gaus_id',' RA',' DEC',' Peak_flux',' E_Peak_flux']
    map_data = pd.read_csv('./prov.csv',usecols=usecols,skiprows=5)
    map_data.to_csv(OutName+'.csv')

    #os.remove('prov.csv')
    for image in Images:
        os.remove(image + '.fits')

    os.mkdir('./'+OutName)
    hdul.writeto('./' + OutName + '/' + OutName + '.fits')
    os.rename('./'+OutName+'.csv','./'+OutName+'/'+OutName+'.csv')
    os.rename('./'+FitsName+'.fits.pybdsf.log','./'+OutName+'/'+FitsName+'.fits.pybdsf.log')
    os.rename('./prov.csv','./'+ OutName + '/prov.csv')

PyBdsf('Const','ResConst')


