import sys
sys.path.append('../../src')

# Import the relevant classes
from model import Model
from sphere import Sphere
from injector import Injector

# Create a model object with the dimensions of the domain.
# Note that in this example where we are injecting just one blob, we could make the domain dimensions simply just a box that
# fits around our sphere of interest - this will substantially reduce the size of the overall .nc file and is therefore
# useful (and sometimes imperetive) for single shapes in large domains. Here however, the domain is small so it doesnt really
# matter.
m = Model(type = "cartesian",
          x_lim = [0, 30000],
          y_lim = [0, 10000],
          z_lim = [0, 18000],
          elements_per_wavelength = 6,
          dominant_freq = 3,
          min_velocity = 2500,
          )

# Create a sphere with radius 2000
ell = Sphere(model = m,
                vp  = -0.4,
                vs  = -0.4,
                rho = -0.4,
                dim = [5000])

# Create an injector object
i = Injector(m)

# Add an object at the centre of the domain using injector
i.addObj(ell, location = [25000, 5000, 12000])

# Write to netcdf file
m.writeNetCDF("./example_4.1.nc")
