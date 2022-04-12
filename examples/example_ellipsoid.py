# Imports
import numpy as np
from model_class import model
from ellipsoid import Ellipsoid
from cylinder import Cylinder
from injector import Injector


# Model dimensions
x = np.array([0, 50000])
y = np.array([0, 50000])
z = np.array([0, 50000])

# Model parameters
freq = 2        # [Hz]
min_vel = 3000  # [m/s]
epw = 3         # 3 elements per wavelength - pretty high res.


m = model(x,y, z, epw, freq, min_vel, oversaturation=1)

#ell = Ellipsoid(m, vp=-0.2, vs=-0.2, rho=-0.2, dim=[10000, 5000, 5000, np.pi/3, np.pi/4, 2])
cyl = Cylinder(m, vp=-0.2, vs=-0.2, rho=-0.2, dim=[10000, 5000, np.pi/3, np.pi/4, 2])


inj = Injector(m)
inj.addObj(cyl, location=[25000, 25000, 25000], overwrite=False)
#inj.spaced_obj(obj=ell, mfl=10000, overwrite=False)


m.writeNetCDF("cyl.nc")