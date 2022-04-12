# Imports
import numpy as np
from model import Model
from sphere_class import Sphere
from spaced_spheres import spaced_spheres


# Model dimensions
x = np.array([0, 300000]) # Model from -150,000 [m] to +150,000 [m] in x direction
y = np.array([0, 300000]) # Model from -150,000 [m] to +150,000 [m] in y direction
z = np.array([0, 200000]) # Model from -100,000 [m] to +100,000 [m] in z direction

# Model parameters
freq = 2        # [Hz]
min_vel = 3000  # [m/s]
epw = 3         # 3 elements per wavelength - pretty high res.


# Create model class - generates a 3D array of the correct size/epw
# Oversaturation can be used to increase the epw above what is necessary based on epw/freq/min velocity
# Obviously this makes a larger array and hence a greater netcdf file (which axisem sometimes struggles with)
m = Model(x, y, z, epw, freq, min_vel, oversaturation=1)


# Define perturbations:
# Here these will inject a value of 0.2 wherever a sphere is injected; note that axisem may either read this as an
# absolute perturbation or as a percentage perturbation dependent on your .yaml inputs - see manual for detail
vs_ptb = -0.2
vp_ptb = -0.2
rho_ptb = -0.2


# For this code I want to inject lots of spheres with a radius of a certain wavelength that are separatated by a certain
# distance (mfp)
sphere_rad_wavelengths = 6 # Sphere radius in wavelengths
mfp = 41.5 # In wavelengths


# Generate spheres:
# Sph is an object of the class sphere which holds some features like its radius/its rho, vp, vs perturbations etc
# This is the blob that is injected. It requires knowledge of the model that it is going into so that it knows the
# grid spacing etc
sph = Sphere(model=m, rho=rho_ptb, vp=vp_ptb, vs=vs_ptb, dim=sphere_rad_wavelengths*m.min_wavelength)

# Spaced spheres is a function which generates a set of coordinates that are equally spaced apart. A sphere is then
# injected, centred at each of these coordinates
# You may wish to inject spheres manually in different places by using:
# sph.set_centre() to set the location of the sphere and then the addSphere function to add the sphere to your model
out = spaced_spheres(sph, m, mfp*m.min_wavelength, print_time='n')

# Define some output filename string:
#scr = f'p{str(ptb)}_{str(freq)}hz_{str(mfp)}_mfp_{str(sphere_rad_wavelengths)}_rad.nc'
scr = "example1.nc"

out.writeNetCDF(scr)
