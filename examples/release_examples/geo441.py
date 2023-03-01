# Plan is to compare a test in which there is a load of thin plumes vs one large plume coming up from an LLVP
import sys
sys.path.append('../../src')

import os
import numpy as np
from model import Model
from ellipsoid import Ellipsoid
from cylinder import Cylinder
from injector import Injector
import netCDF4 as nc

# We dont need to make a model that spans the whole domain, just the part we are interested in injecting a plume in:
radius = 6371000
perturb = 0.1
lat_lim = [-15 , 15]
long_lim = [-15, 15]
depth_lim = [0, 2891000]

# Set locations for shapes:
# Create our global model:
glob_m = Model("spherical", lat_lim, long_lim, depth_lim, elements_per_wavelength=1, dominant_freq=1, min_velocity=10000, oversaturation=1, a=radius)
i = Injector(glob_m)

plumes = [[0, 0, 1500000, 3200000, 100000],
          [3, 0, 2100000, 2200000, 100000],
          [6, 0, 2600000, 1200000, 100000],
          [-3, 0, 2100000, 2200000, 100000],
          [-6, 0, 2600000, 1200000, 100000],
          ]

for pl in range(5):
    p = plumes[pl]
    # Create cylinder:
    c = Cylinder(model=glob_m, vp=perturb, vs=perturb, rho=perturb, dim=[p[3], p[4], 0, 0, 1], loc=p[:3], major_axis='Z')
    i.addObj(c, location=p[:3], overwrite=True)


# Create ellipse:
print("Creating ellipse:")
ell_loc = [0,0, 200000]
ellipse = Ellipsoid(model=glob_m, vp=perturb, vs=perturb, rho=perturb, dim=[1000000, 100000, 400000, np.pi/2, 0, 1], loc=ell_loc)
i.addObj(ellipse, location=ell_loc, overwrite=True)


# Write to NetCDF file
glob_m.writeNetCDF("llvp.nc")
glob_m.writeNetCDF("llvp_visual.nc", paraview=True)


