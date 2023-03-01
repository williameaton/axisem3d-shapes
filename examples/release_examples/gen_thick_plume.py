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
perturb = -0.1
lat_lim = [-30 , 30]
long_lim = [-30, 30]
depth_lim = [0, 2891000]

# Set locations for shapes:
ell_loc = [0,0, 2891000]
c1_loc = [0,0, 1425000]

# Create our global model:
glob_m = Model("spherical", lat_lim, long_lim, depth_lim, elements_per_wavelength=1, dominant_freq=1, min_velocity=15000, oversaturation=1, a=radius)
i = Injector(glob_m)


plumes = [[0, 0, 1500000, 3000000, 1500000],

          [-13.5, -6, 2400000, 800000, 130000 ],
          [1, -2, 2400000, 1200000, 100000],
          [-2.5, -6.5, 2400000, 800000, 130000],
          [0, 7.5, 2400000, 900000, 400000],
          [0, 0, 2500000, 600000, 800000],
          [-7, 3, 2500000, 600000, 1000000],
          [10, 3, 2200000, 800000, 500000],
          [5, -8, 2500000, 700000, 300000],
          [-3.5, -4, 2600000, 700000, 300000],
          [-1.5, 6.5, 2500000, 900000, 500000],
          [4, 0, 2500000, 1000000, 450000],
          ]

for pl in range(26):
    p = plumes[pl]
    # Create cylinder:
    c = Cylinder(model=glob_m, vp=perturb, vs=perturb, rho=perturb, dim=[p[3], p[4], 0, 0, 1], loc=p[:3], major_axis='Z')
    i.addObj(c, location=p[:3], overwrite=True)
    print(f"{pl}/26")

# Create ellipse:
ellipse = Ellipsoid(model=glob_m, vp=perturb, vs=perturb, rho=perturb, dim=[3000000, 3000000, 350000, np.pi/2, 0, 1], loc=ell_loc)
i.addObj(ellipse, location=ell_loc, overwrite=True)

# Write to NetCDF file
glob_m.writeNetCDF("llvp.nc", paraview=False)
glob_m.writeNetCDF("llvp_visual.nc", paraview=True)


