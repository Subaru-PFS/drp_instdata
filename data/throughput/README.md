# PFS throughput information

This directory `throughput` contains the following files:

* README.md (this file) : some explanation
* pfs_thr_20201231_ext_all_blu.dat : transmission curve of blue arm
* pfs_thr_20201231_ext_all_red.dat : transmission curve of red arm
* pfs_thr_20201231_ext_all_nir.dat : transmission curve of NIR arm
* pfs_thr_20201231_ext_all_mid.dat : transmission curve of red arm in medium resolution (MR) mode

They are *roughly* consistent with the current throughput model in the `spt_ExposureTimeCalculator`.

Each file contains the following information:

* (Col 1) wavelength in nm
* (Col 2) telescope primary mirror reflectivity (taken from Subaru website)
* (Col 3) wide field corrector (WFC) and field element (based on measurement + requirement)
* (Col 4) fiber system (based on the requirement)
* (Col 5) spectrograph system optical components (based on measurement for red arm but the requirement for blue & NIR arms)
* (Col 6) spectrograph system dichroic mirror (based on requirement)
* (Col 7) spectrograph system VPH grating (based on requirement)
* (Col 8) spectrograph system detector (based on measurements but approximate values are here)
* (Col 9) atmospheric transmission (at zenith)
    * Continuum opacity: Gemini Mauna Kea optical extinction model
    * Line opacity: KP measurements at <900nm and Gemini MK model with 3mm PWV at >900nm
* (Col 10) total throughput without atmosphere
* (Col 11) total throughput with atmosphere
