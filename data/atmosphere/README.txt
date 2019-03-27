We requested the following grid from Nick Mondrik:

* Wavelength: 350-1300 nm, at the agreed constant resolution of 1cm^-1 (https://pfs.ipmu.jp/research/parameters.html)
* PWV: 1, 2, 3 mm (http://www.gemini.edu/sciops/telescopes-and-sites/observing-condition-constraints)
* Aerosol: tau=0.0075; a=0, 1, 2.5 (arXiv:1210.2619 Fig 13, Fig 19)
* Zenith angle: 0, 30, 60, 70 deg
* O3: 260 DU (arXiv:1210.2619 Fig 13, 7.4, Fig 18)
* Pressure: 616 mbar (arXiv:1210.2619 Fig 13, 4.1.1)

Nicholas Mondrik <nmondrik@gmail.com> replied:

> I've attached a tarball with the generated files.  There is a metadata file that gives the parameters used for each atmosphere file.  Within the atmosphere files themselves, column 0 is wavelength in nm, and column 1 is the transparency.
>
> An important point for this future: is that due to how libradtran does it's modeling, even if you model an empty atmosphere, it will still have a COS(zenith_angle) shape (as I understand it, libradtran assumes a flat sensor whose normal points at zenith).  This is purely geometric and I have already removed this term from the transparencies I've given to you.  If you use more libradtran modeling in the future (whether from me or others), you'll want to keep this in mind.
>
> Let me know if there's anything else I can do to help with this!
> Nick
