from astropy.io import fits
from astropy.convolution import convolve, Gaussian2DKernel
import numpy as np
import matplotlib.pyplot as plt

#-------------------Constantes-------------------------
px_beam = 1/0.03530547356165598     #Constante para convertir las unidades de mJy/px a mJy/beam
sig_conv = 0.1325                   #Factor de conversión de ruido al ser convolucionado (si era 1 después de la conv. será 0.1325)


GaussPSF = Gaussian2DKernel(5/(2*np.sqrt(2*np.log(2))))

fluxes = np.arange(1,1+15)
map = np.zeros((25,25*len(fluxes)))

for i in range(len(fluxes)):
    map[12][12+24*i] = fluxes[i]

Ruido=np.random.normal(0,1,(25,25*len(fluxes)))
map = px_beam*(convolve(map,GaussPSF))+Ruido

#Ruido=np.random.normal(0,1/px_beam,(25,25*len(fluxes)))
#map = px_beam*(convolve(map,GaussPSF)+Ruido)

#Ruido=np.random.normal(0,1/(px_beam*px_beam),(25,25*len(fluxes)))
#map = px_beam*(convolve(map+Ruido,GaussPSF))

plt.imshow(map,interpolation='none',origin='lower')
plt.show()

#Configuramos los fits
hdu = fits.PrimaryHDU()
hdr = hdu.header
hdr['CTYPE1'] = ('RA---TAN','WCS Projection Type 1')
hdr['CUNIT1'] = ('deg     ','WCS Axis Unit 1')
hdr['CRVAL1'] = (109.3789,'WCS Ref Pixel Value 1')
hdr['CDELT1'] = (-0.0002777778,'WCS Pixel Scale 1')
hdr['CRPIX1'] = (379.5,'WCS Ref Pixel 1')
hdr['CTYPE2'] = ('DEC--TAN','WCS Projection Type 2')
hdr['CUNIT2'] = ('deg     ','WCS Axis Unit 2')
hdr['CRVAL2'] = (37.75826,'WCS Ref Pixel Value 2')
hdr['CDELT2'] = (0.0002777778,'WCS Pixel Scale 2')
hdr['CRPIX2'] = (387.5,'WCS Ref Pixel 2')
hdr['CTYPE3'] = ('FREQ    ','WCS Projection Type 3')
hdr['CUNIT3'] = ('Hz      ','WCS Axis Unit 3')
hdr['CRVAL3'] = (1.,'WCS Ref Pixel Value 3')
hdr['CDELT3'] = (1.,'WCS Pixel Scale 3')
hdr['CRPIX3'] = (1.,'WCS Ref Pixel 3')
hdr['CTYPE4'] = ('STOKES  ','WCS Projection Type 4')
hdr['CUNIT4'] = ('        ','WCS Axis Unit 4')
hdr['CRVAL4'] = (1.,'WCS Ref Pixel Value 4')
hdr['CDELT4'] = (1.,'WCS Pixel Scale 4')
hdr['CRPIX4'] = (1.,'WCS Ref Pixel 4')
hdr['UNIT'] = ('mJy/beam','Unit of map')


fits.writeto('MultSNR.fits',map,hdr,overwrite=True)