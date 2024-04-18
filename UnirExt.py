import bdsf
import pandas as pd
import os 
from astropy.io import fits

Images = ['ch0','island_mask','gaus_model','gaus_resid','rms']

ch0 = fits.open(Images[0] + '.fits')
island_mask = fits.open(Images[1] + '.fits')
gaus_model = fits.open(Images[2] + '.fits')
gaus_resid = fits.open(Images[3] + '.fits')
rms = fits.open(Images[4] + '.fits')

hdul = fits.HDUList()
fits.PrimaryHDU()
hdul.append(ch0[0])
hdul.append(island_mask[0])
hdul.append(gaus_model[0])
hdul.append(gaus_resid[0])
hdul.append(rms[0])
hdul[1].name = 'island_mask'
hdul[2].name = 'gaus_model'
hdul[3].name = 'gaus_resid'
hdul[4].name = 'rms'
hdul.writeto('./ResConst.fits',overwrite=True)



