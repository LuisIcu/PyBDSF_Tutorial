from astropy.io import fits
from astropy.convolution import convolve, Gaussian2DKernel
import numpy as np
import matplotlib.pyplot as plt

GaussPSF = Gaussian2DKernel(6/(2*np.sqrt(2*np.log(2))))
Ruido=np.random.normal(0,0.001,(37,21*16))

map = np.zeros((37,21*16))
for i in range(16):
    map[11][11+20*i] = 1
    map[12+i][11+20*i] = 1
map = (1/0.024516717278706596)*(convolve(map,GaussPSF)+Ruido)

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


fits.writeto('MultDist1.fits',map,hdr,overwrite=True)