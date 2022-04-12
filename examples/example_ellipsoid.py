# Imports
import numpy as np
from model import Model
from cylinder import Cylinder
from slab import Slab
from sphere import Sphere
from ellipsoid import Ellipsoid
from injector import Injector


# Model dimensions
x = np.array([0, 150000])
y = np.array([0, 50000])
z = np.array([0, 80000])

# Model parameters
freq = 2        # [Hz]
min_vel = 3000  # [m/s]
epw = 3         # 3 elements per wavelength - pretty high res.


m = Model(x, y, z, epw, freq, min_vel, oversaturation=1)
inj = Injector(m)

#SLAB:
slab_inc = Slab(m, vp=-0.2, vs=-0.2, rho=-0.2, dim=[115000, 50000, 4000,  np.pi/4, 0, 1])
inj.addObj(slab_inc, location=[60000, 25000, 40000], overwrite=False)

flat_slab = Slab(m, vp=-0.2, vs=-0.2, rho=-0.2, dim=[24000, 50000, 4000,  0, 0, 1])
inj.addObj(flat_slab, location=[10000, 25000, 2000], overwrite=False)


# PLUME
plume_head = Sphere(m, vp=0.3, vs=0.3, rho=0.3, dim=[20000])
plume_tail = Cylinder(m, vp=0.3, vs=0.3, rho=0.3, dim=[60000, 3000, 0, 0, 1], major_axis="Z")
inj.addObj(plume_head, location=[140000, 40000, 15000], overwrite=False)
inj.addObj(plume_tail, location=[140000, 40000, 50000], overwrite=True)


# Ellipsoids
di = 15000
dJ = 7000

for j in range(6):
    j1 = (j+1)
    strain_ellipsoids = Ellipsoid(m, vp=0.2/j1, vs=0.2/j1, rho=0.2/j1, dim=[8000 -j1*1000, 1500 - j1*200, 1500 - 200*j1, np.pi/4, 0, 4])

    dj = dJ - 500*j
    for i in range(5):
        inj.spaced_obj(obj=strain_ellipsoids, mfl=[30000, 5000, 10000], x_lim=[40000 + i*di +j*dj, 60000 + i*di +j*dj], z_lim=[20000 + i*di, 27000 + i*di], overwrite=False)

m.writeNetCDF(f"trial1.nc")