import numpy as np
from model import Model
from ellipsoid import Ellipsoid
from cylinder import *
from injector import *
import netCDF4 as nc
perturb = 0.2
lat_lim = [-10, 90]
long_lim = [-10, 10]
depth_lim = [0, 2885000]


glob_m = Model("spherical", lat_lim, long_lim, depth_lim, elements_per_wavelength=1, dominant_freq=1, min_velocity=10000, oversaturation=1, a=6371000)

s = Cylinder(model=glob_m, vp=perturb, vs=perturb, rho=perturb, dim=[3000000, 150000, np.pi/4, 0, 1], loc=[45,0, 1442500], major_axis='Z')
i = Injector(glob_m)

i.addObj(s, location=[45,0, 1442500], overwrite=True)



out_dir  = f"../"
filename = f"glob.nc"
fullname = f"{out_dir}/{filename}"


grid_lat = np.linspace(glob_m.x_lim[0], glob_m.x_lim[1], glob_m.nx)
grid_lon = np.linspace(glob_m.y_lim[0], glob_m.y_lim[1], glob_m.ny)
grid_depth = np.linspace(glob_m.z_lim[0], glob_m.z_lim[1], glob_m.nz)

f = nc.Dataset(fullname, 'w', format='NETCDF4')
# Create dimension arrays
# We now create the dimensions:
lat = f.createDimension('lat', glob_m.nx)
lon = f.createDimension('lon', glob_m.ny)
depth = f.createDimension('depth', glob_m.nz)

# Creating the variables:
lats = f.createVariable('lat', 'f4', ('lat',))
lats.units = 'degrees_north'
lats.long_name = 'latitude'

lons = f.createVariable('lon', 'f4', ('lon',))
lons.units = 'degrees_east'
lons.long_name = 'longitude'

depths = f.createVariable('depth', 'f4', ('depth',))
depths.units = 'meters'

v_rho = f.createVariable('rho', 'f4', ('lat', 'lon', 'depth',))
v_vp = f.createVariable('vp', 'f4', ('lat', 'lon', 'depth',))
v_vs = f.createVariable('vs', 'f4', ('lat', 'lon', 'depth',))

# Assigning values to the variables:
lats[:] = grid_lat
lons[:] = grid_lon
depths[:] = 6371000 - grid_depth
v_rho[:, :, :] = glob_m.bm_rho
v_vp[:, :, :] = glob_m.bm_vp
v_vs[:, :, :] = glob_m.bm_vs
print('Data written to file ', filename)
f.close()









