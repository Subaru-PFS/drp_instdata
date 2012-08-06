import os
import re

import numpy
import scipy.signal
import scipy.ndimage

import pyfits

"""
OFFSETS :
    HEADER: 0
    DESIGN FILE: 2K
    X,Y,FOC (NIMAGE*3 floats): 8K
    DATA (NIMAGE*XSIZE*YSIZE u-shorts) 32K

"""

def makeFiberImage(fiberRadius=28, shape=(64,64), dtype='f4'):
    """ Return the image we convolve the spots with. """
    
    im = numpy.zeros(shape, dtype=dtype)
    spotRadius = shape[0]/2

    x,y = numpy.meshgrid(numpy.arange(-spotRadius,spotRadius+1),
                         numpy.arange(-spotRadius,spotRadius+1))
    d = numpy.sqrt(x**2 + y**2)

    im[numpy.where(d <= fiberRadius)] = 1

    return im
    
def convolveWithFiber(spot, fiberImage=None):
    if fiberImage == None:
        fiberImage = makeFiberImage()
    
    return scipy.ndimage.convolve(spot, fiberImage, mode='constant', cval=0.0)

def readAll(filename):
    """ Read slightly cleaned up versions of JEGs spots.

    The .imgstk file contains a few 1k-aligned sections:
    
    OFFSETS :
        HEADER: 0
        DESIGN FILE: 2K
        X,Y,FOC (NIMAGE*3 floats): 8K
        DATA (NIMAGE*XSIZE*YSIZE u-shorts) 32K
        
    """

    with open(filename, 'r') as f:
        rawHeader = f.read(2*1024)
        rawDesign = f.read((8-2)*1024)
        rawPositions = f.read((32-8)*1024)
        rawData = f.read()

    rawHeader = rawHeader.rstrip('\0\n')
    header = rawHeader.split('\n')

    headerDict = {'TITLE':header.pop(0)}
    for i, h in enumerate(header):
        m = re.match('(^[A-Z][-A-Z_ 0-9\[\]]*) = (.*)', h)
        if m:
            key, value = m.groups()
            headerDict[key] = value
        else:
            headerDict['LINE%03d'%(i)] = h
                       
    nimage = int(headerDict['NIMAGE'])
    xsize = int(headerDict['XSIZE'])
    ysize = int(headerDict['YSIZE'])
    positions = numpy.fromstring(rawPositions, dtype='3f4', count=nimage)
    
    wavelengths = []
    nlam = int(headerDict['NLAM'])
    for i in range(nlam):
        waveKey = "LAM[%d]" % (i)
        wavelength = float(headerDict[waveKey])
        wavelengths.append(wavelength)
        
    fiberIDs = []
    slitRadius = float(headerDict['SLIT RADIUS'])
    fiberSpacing = 27
    nang = int(headerDict['NANG'])
    for i in range(nang):
        #angKey = "SINANG[%d]" % (i)
        #sinang = float(headerDict[angKey])
        #fiberOffset = slitRadius * sinang
        #print "ang %d: %0.2f" % (i, fiberOffset)
        #fiberIDs.append(fiberOffset)
        fiberIDs.append(i * fiberSpacing)
        
    data = numpy.fromstring(rawData, dtype='(%d,%d)u2' % (xsize,ysize), count=nimage).astype('f4')
    fiberImage = makeFiberImage()

    spots = []
    for i in range(data.shape[0]):
        fiberIdx = fiberIDs[i / nlam]
        wavelength = wavelengths[i % nlam]
        xc = positions[i,0]
        yc = positions[i,1]
        sum = numpy.sum(data[i,:,:])
        spot = convolveWithFiber(data[i,:,:], fiberImage)
        spots.append((fiberIdx, wavelength, xc, yc, spot))
        print("fiber  %d (%d, %0.2f) sum=%f" % (i, fiberIdx, wavelength, sum))

        #spots[i,:,:] = convolveWithFiber(data[i,:,:], fiberImage)

    spotDtype = numpy.dtype([('fiberIdx','i2'),
                             ('wavelength','f4'),
                             ('spot_xc','f4'), ('spot_yc','f4'),
                             ('spot', '(256,256)f4')])

    tarr = numpy.array(spots, dtype=spotDtype)

    # Now clean up... later steps expect to have wavelengths in order
    sortfrom = numpy.argsort(tarr['wavelength'][:nlam])
    arr = numpy.zeros(shape=tarr.shape, dtype=tarr.dtype)
    for i in range(nlam):
        arr[i::nlam] = tarr[sortfrom[i]::nlam]
        
    return arr

def writeSpotFITS(spotDir, data):

    phdu = pyfits.PrimaryHDU()
    phdr = phdu.header
    phdr.update('pixscale', 0.001, 'mm/pixel')

    cols = []
    cols.append(pyfits.Column(name='fiberIdx',
                              format='I',
                              array=data['fiberIdx']))
    cols.append(pyfits.Column(name='wavelength',
                              format='D',
                              array=data['wavelength']))
    cols.append(pyfits.Column(name='spot_xc',
                              format='D',
                              array=data['spot_xc']))
    cols.append(pyfits.Column(name='spot_yc',
                              format='D',
                              array=data['spot_yc']))
    spots = data['spot'][:]
    spots.shape = (len(spots), 256*256)
    cols.append(pyfits.Column(name='spot',
                              format='%dE' % (256*256),
                              dim='(256,256)',
                              array=spots))
    colDefs = pyfits.ColDefs(cols)

    thdu = pyfits.new_table(colDefs)
    hdulist = pyfits.HDUList([phdu, thdu])

    hdulist.writeto(os.path.join(spotDir, 'spots.fits'), 
                    checksum=True, clobber=True)

def saveFITS(filename, positions, data):
    pass


