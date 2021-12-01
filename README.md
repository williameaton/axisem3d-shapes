# AxiSEM 3D repo

### Overview:

Author: Will Eaton, Princeton University 2021

Last modified: December 1st 2021

Contact: weaton@princeton.edu 

### Short description:
A small repo containing scripts to inject sphere's into 3D cartesian models for use in AxiSEM3D. I can write a better set of documentation if required, just email me! 

### Usage: 
This isn't a package or compiled executable, simply a series of Python3 functions that can be used. There are two classes accompanied by a number of functions: 

1) Model - the model class creates and stores 3D arrays for density, Vp and Vs. It is defined using a series of parameters like the minimum frequency and elements per wavelength 
2) Sphere - a sphere object essentially holds details like the radius of the sphere and the internal vp/vs/rho values of that sphere. Spheres may then be added to the model using the addSphere() function. 

Two examples are provided which demonstrate two cases of usage: 
1) The reason I developed this code was to produce 3D models which are filled with blobs that are separated by some distance (mean free path). This is example 1 and taken pretty much from the script I always used to generate these. Some of the functions supplied here like spaced_spheres() are written for this purpose only. 
2) Example two is a bit more general and demonstrates that you can have whatever 3D model that you want and inject a sphere (or as many as you want) into that model. I have written a Jupyter notebook for this one but not Example 1. 

#### Spheres: 
The function gen_sphere() does the actual bulk of the sphere generation. I note here that a second function called gen_sphere_gaussian() is also supplied. The difference between these is that gen_sphere() produces homogenous spheres of a certain vp, vs, rho, where as the gaussian version has its vp, vs and rho taper towards 0 in some outer region of the sphere. In this case the original radius of the sphere is all homogenous + some additional shell of tapered material from r_original to r. This was created in the hope that it might avoid some instabilities caused in AxiSEM3D when the perturbations of the sphere were strong. I could have written these in a single combined function but in all honestly I couldn't be bothered, especially as I don't use the gaussian version. However, note that the lines in which the gaussian values of Vp, Vs, Rho are implimented (lines 39-44) could be edited to make whatever kind of blob you want - i.e. one with some internal structure. 


## Current limitations: 
The major limitation is that presently the spheres are injected as follows: the 'sphere' is a 3D array with non-zero values in certain elements. On injection, the non-zero values of this array are set as the values of the relevant model elements. Hence, any elements inside the sphere that have a value of 0 (e.g. if Vs = 0 this would be a fluid section of the sphere) will not be injected and the model will retain its background value. If that becomes an issue for someone then I'll try and update it. 
