import numpy
import scipy

from numpy.polynomial import Chebyshev as T

import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor
import plotTools

def figrange(figname, xlim=None, ylim=None):
    fig = plt.figure(figname)

    for i, ax in enumerate(fig.axes):
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)

def plotOneSpec(waves, specs, specIdx, pca, ncomp=None, pullCoeffs=[], figname='onesky', doClear=True):
    skyfig = plt.figure(figname)
    if doClear:
        skyfig.clf()
    
    wave = waves[specIdx,:]
    rawSpec = specs[specIdx,:]
    fitCoeffs = pca.transform(rawSpec)
    fitSpec = pca.inverse_transform(fitCoeffs)

    print "coeffs: ", fitCoeffs
    allFits = pca.transform(specs)
    if ncomp == None:
        ncomp = pca.n_components
    npcomp = min(ncomp, pca.n_components)
    needExtraComp = npcomp < pca.n_components
        
    nrows = npcomp+1
    ncols = 2
    nplots = nrows*ncols
    skyplot0 = skyfig.add_subplot(nrows,ncols,nplots-1)
    skyplot0.locator_params(axis='y', nbins=4)
    skyplot0.plot(wave, rawSpec)
    
    fitplot = skyfig.add_subplot(nrows,ncols,nplots, sharex=skyplot0, sharey=skyplot0)
    fitplot.locator_params(axis='y', nbins=4)
    fitplot.plot(wave, fitSpec-rawSpec)
        
    allplots = [skyplot0, fitplot]
    for i in range(npcomp):
        
        skyplot = skyfig.add_subplot(nrows, ncols, i*ncols+1, sharex=skyplot0, sharey=skyplot0)
        allplots.append(skyplot)
        skyplot.get_xaxis().set_visible(False)
        skyplot.locator_params(axis='y',nbins=4)

        pCoeffs = fitCoeffs * 0
        if i == npcomp-1 and needExtraComp:
            pCoeffs[i:] = fitCoeffs[i:]
        else:
            pCoeffs[i] = fitCoeffs[i]
        #coeffFit = numpy.dot(pCoeffs, pca.components_)
        #print "pCoeffs %d: %s" % (i, pCoeffs)
        coeffFit = pca.inverse_transform(pCoeffs)

        if pullCoeffs in (None, []):
            subCoeffs = fitCoeffs * 0
            subCoeffs[numpy.arange(i+1)] = fitCoeffs[numpy.arange(i+1)]
        else:
            subCoeffs = pCoeffs.copy()
            for c in pullCoeffs:
                subCoeffs[c] = fitCoeffs[c]
        subFit = pca.inverse_transform(subCoeffs)
        
        skyplot.plot(wave, coeffFit-pca.mean_)

        if doClear:
            pcaplot = skyfig.add_subplot(nrows, ncols, i*ncols+2, sharex=skyplot0, sharey=skyplot0)
            allplots.append(pcaplot)
            pcaplot.get_xaxis().set_visible(False)
            pcaplot.locator_params(axis='y',nbins=4)
            
            sort_i = allFits[:,i].argsort()
            sort_picks = sort_i[((len(sort_i)-1) * numpy.array([0.1, 0.9, 0.5])).astype('i4')]
            colors = 'b', 'r', 'k'
            #alpha = 0.5, 0.5, 1.0
            for ii, limIdx in enumerate(sort_picks):
                limCoeffs = fitCoeffs * 0
                limCoeffs[i] = allFits[limIdx, i]
                limSpec = pca.inverse_transform(limCoeffs)
                pcaplot.plot(wave, limSpec-pca.mean_, colors[ii])

    if doClear:
        skyplot0.plot(wave, pca.mean_, 'm')
        c = MultiCursor(skyfig.canvas, allplots, useblit=True, color='red', alpha=0.5)

    skyplot0.plot(wave, fitSpec, alpha=0.75)
    

    return fitCoeffs


def plotPCA1(pca, maxComponents=10):
    fig = plotTools.chooseFig('pca')

    ncomp = min(pca.n_components, maxComponents)
    print ncomp

    comps = pca.components_

    allplots = []
    pcaplot1 = None
    for i in range(ncomp):
        pcaplot = fig.add_subplot(ncomp, 1, i+1, sharex=pcaplot1, sharey=pcaplot1)

        if pcaplot1 == None:
            pcaplot.set_title('PCA components')
            pcaplot1 = pcaplot
        if i != ncomp-1:
            pcaplot.get_xaxis().set_visible(False)
        allplots.append(pcaplot)
        pcaplot.locator_params(axis='y', nbins=2)
        pcaplot.hlines(0, *pcaplot0.get_xlim(), color='r', alpha=0.5)
        cmean = comps[i].mean()
        sign = 1 if cmean > 0 else -1
        pcaplot.plot(twave, sign*comps[i])
        pcaplot.set_ylim(-0.1, 0.1)
        pcaplot.get_yaxis().set_visible(False)
        print "minmax(%d): %g, %g, %g" % (i, comps[i].min(), comps[i].max(), cmean)

    c = MultiCursor(fig.canvas, allplots, useblit=True,color='red', alpha=0.5)
    plotTools.scaleFigureText(fig, [2.0, 2.0, 2.0])
    fig.axes[0].set_xlim(9000,12500)
    #fig.axes[0].set_ylim(-1e-15, 5e-15)
    #fig.axes[1].set_ylim(-0.1, 0.1)

def plotPCA2(pca, wave, maxComponents=10):
    fig = plotTools.chooseFig('pca')

    ncomp = pca.n_components
    print ncomp

    comps = pca.components_

    pcaplot0 = fig.add_subplot(ncomp+1,1,1)
    pcaplot0.xaxis.set_visible(False)
    pcaplot0.plot(wave, pca.mean_, 'g')
    pcaplot0.locator_params(axis='y', nbins=4)
    pcaplot0.set_title('PCA components (with mean on top)')

    allplots = [pcaplot0]

    pcaplot1 = None
    for i in range(ncomp):
        pcaplot = fig.add_subplot(ncomp+1,1,i+2, sharex=pcaplot0, sharey=pcaplot1)
        allplots.append(pcaplot)
        if pcaplot1 == None:
            pcaplot1 = pcaplot
        pcaplot.locator_params(axis='y', nbins=2)
        if i != ncomp-1:
            pcaplot.get_xaxis().set_visible(False)
        pcaplot.hlines(0, *pcaplot0.get_xlim(), color='r', alpha=0.5)
        pcaplot.plot(wave, comps[i])
        print "minmax(%d): %g, %g" % (i, comps[i].min(), comps[i].max())

    MultiCursor(fig.canvas, allplots, useblit=True,color='red', alpha=0.5)
    #fig.axes[0].set_xlim(10000,12000)
    #fig.axes[0].set_ylim(-1e-15, 5e-15)
    #fig.axes[1].set_ylim(-0.1, 0.1)

def plotResidSpec(waves, specs, specIdx, pca, ncomp=None, pullCoeffs=[], figname='residuals', doClear=True):
    fig = plt.figure(figname)
    if doClear:
        fig.clf()
    
    wave = waves[specIdx,:]
    rawSpec = specs[specIdx,:]
    fitCoeffs = pca.transform(rawSpec)
    fitSpec = pca.inverse_transform(fitCoeffs).flatten()

    print("shapes: ", wave.shape, rawSpec.shape, fitSpec.shape)
    print("coeffs: ", fitCoeffs)

    nrows = 2
    ncols = 1
    nplots = nrows*ncols
    skyplot0 = fig.add_subplot(nrows,ncols,nplots-1)
    skyplot0.locator_params(axis='y', nbins=5)
    skyplot0.plot(wave, rawSpec)
    skyplot0.set_title('background-subtracted, airmass-corrected spectra')
    skyplot0.set_ylabel('erg/(s cm$^2$ arcsec$^2$ $\AA$)', size=16.0)
    
    residplot = fig.add_subplot(nrows,ncols,nplots, sharex=skyplot0)
    residplot.locator_params(axis='y', nbins=5)
    residplot.plot(wave, fitSpec-rawSpec)
    residplot.set_title('residuals from best fits to %d term PCA (10x scale)' % (pca.n_components))
    residplot.set_ylabel('erg/(s cm$^2$ arcsec$^2$ $\AA$)', size=16.0)
        
    allplots = [skyplot0, residplot]
 
    if doClear:
        skyplot0.plot(wave, pca.mean_, 'm')

    skyplot0.plot(wave, fitSpec, alpha=0.75)
    MultiCursor(fig.canvas, allplots, useblit=True, color='red', alpha=0.5)

    return fitCoeffs

def moonFrac(expInfo):
    moonAlt = expInfo[:,1] > 0
    moonIll = expInfo[:,2]
    moonAng = expInfo[:,0]
    moonRad = moonAng * numpy.pi / 180
    moonFrac = numpy.cos(moonRad/2)
    
    return moonAlt * moonIll * moonFrac

def clipsky(inArray, sigma=3, niter=3):
    a = inArray.copy()
    mask = numpy.zeros(shape=a.shape, dtype='bool')
    
    for i in range(niter):
        amed = numpy.median(a,axis=0)
        asig = a.std(axis=0)
        duds = numpy.where(numpy.abs(a - amed) > sigma*asig)

        mask[duds] = True
        a[duds] = amed[duds[1]]

        print "clip iter=%d sigma=%0.2f : %d/%d (%g), tot=%d (%g)" % (i+1, sigma, 
                                                         len(duds[0]), len(a.flat), 
                                                         1.0*len(duds[0])/len(a.flat),
                                                         mask.sum(), 1.0*mask.sum()/len(mask.flat))
    return a, mask

def filterSky(inArray, width=101):
    bgArray = inArray.copy()
    for i in range(inArray.shape[0]):
        bg = scipy.signal.medfilt(inArray[i,:], width)
        bgArray[i,:] = bg
        
    return bgArray

def ssmooth(skies, g=None, sigma=2.0):
    if not g:
        g = scipy.signal.gaussian(21,sigma)
        g /= sum(g)
    ret = scipy.ndimage.filters.convolve1d(skies, g, axis=1, mode='constant')
    return ret

def test_ssmooth(skies):
    oskies = ssmooth(skies, sigma=3.0)
    fig = plotTools.chooseFig('testing123')
    ax = fig.add_subplot(111)
    ax.plot(skies[0,:])
    ax.plot(oskies[0,:])

def varPlot(fig, pca, x, bestFit):
    lim_w = numpy.argmax(numpy.abs(bestFit), axis=0)
    min_w = numpy.argmin(bestFit, axis=0)
    max_w = numpy.argmax(bestFit, axis=0)
    print "min: %s" % (min_w)
    print "max: %s" % (max_w)
    print "lim: %s" % (lim_w)

    if x == None:
        x = numpy.arange(bestFit.shape[0])
    ii = numpy.argsort(x)

    for i in range(pca.n_components):
        if i == 0:
            pRef = p = fig.add_subplot(pca.n_components,1,i+1)
        else:
            p = fig.add_subplot(pca.n_components,1,i+1, sharex=pRef)
        p.locator_params(axis='y', nbins=4)
        p.plot(x[ii], bestFit[ii,i], '+')

        p.hlines(0, *p.get_xlim(), color='r', alpha=0.5)
        t = T.fit(x[ii], bestFit[ii,i], 1)
        pt = t(x[ii])
        p.plot(x[ii], pt)

        p.plot(x[min_w[i]], bestFit[min_w[i],i], 'r*')
        p.plot(x[max_w[i]], bestFit[max_w[i],i], 'r*')
        
    return min_w, max_w, lim_w
    
