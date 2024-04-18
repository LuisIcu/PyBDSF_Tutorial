from astropy.io import fits
from astropy.convolution import convolve, Gaussian2DKernel
import numpy as np
import matplotlib.pyplot as plt

#Creamos el mapa
map = np.zeros((101,101))
map[27][32] = 1
map[51][78] = 2
Ruido=np.random.normal(0,0.001,(101,101))

map1 = convolve(map,Gaussian2DKernel(5/2.355))+Ruido
map2 = (1/0.03531086478853188)*(convolve(map,Gaussian2DKernel(5/2.355))+Ruido)

'''plt.imshow(map1, interpolation='none', origin='lower')
plt.show()
plt.close()
plt.imshow(map2, interpolation='none', origin='lower')
plt.show()
plt.close()'''

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


fits.writeto('NoConst.fits',map1,hdr,overwrite=True)
fits.writeto('Const.fits',map2,hdr,overwrite=True)