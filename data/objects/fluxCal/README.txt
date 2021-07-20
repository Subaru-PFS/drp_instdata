Stellar spectra intended for use as in-field flux standards
===========================================================

The AMBRE model templates whose wavelength was extrapolated
to 1300 nm with an exponential function. See PIPE2D-364 for
the details.

* Templates
Six templates with Teff = 6500, 7000, 7500K and Z = 0, -1. 

* File name
The file names follows ones of the previous version but they
have a suffix of "_Extp". The previous naming rule is as 
follows.
> > Spectrum files are named as follows:
> > p2500:g+3.5:m0.0:t01:z+0.00:a+0.00.AMBRE
> > where
> > 'p' (or 's') means that radiative transfer has been solved in plan-parallel (or spherical) geometry
> > '2500' : Teff in K
> > 'g+3.5': log of surface gravity (g in units of cm/s2)
> > 'm0.0' : mass of the corresponding MARCS model atmosphere (in Msun)
> > 't0.1' : microturbulence velocity adopted in the MARCS model atmosphere and the spectral synthesis (in km/s)
> > 'z+0.00' : mean stellar metallicity (equivalent to [Metal/H] or [Fe/H])
> > 'a+0.00' : [alpha/Fe] chemical index

* FITS
Only flux density (nJy) is stored. 
Use CRPIX1, CRVAL, CDELT in FITS header for wavelength solution.
Pixel scale is 0.01 nm/pix.