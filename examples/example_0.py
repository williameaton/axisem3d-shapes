# Imports
import numpy as np
from model_class import model
from sphere_class import Sphere
from injector import Injector


# Model dimensions
x = np.array([0, 300000])
y = np.array([0, 300000])
z = np.array([0, 200000])

# Model parameters
freq = 2        # [Hz]
min_vel = 3000  # [m/s]
epw = 3         # 3 elements per wavelength - pretty high res.

vs_ptb = -0.2
vp_ptb = -0.2
rho_ptb = -0.2

sphere_rad_wavelengths = 6
mfp = 41.5


m = model(x,y, z, epw, freq, min_vel, oversaturation=1)
sph = Sphere(model=m, rho=rho_ptb, vp=vp_ptb, vs=vs_ptb, dim=sphere_rad_wavelengths*m.min_wavelength)
inj = Injector(m)

inj.spaced_obj(obj=sph, mfl=50000, overwrite=False)

sph.set_radius(35000)
sph.update_vp(-0.4)
inj.addObj(sph, location=[150000, 150000, 100000], overwrite=False)


m.writeNetCDF("test0.nc")