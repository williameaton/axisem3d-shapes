import matplotlib.pyplot as plt
import numpy as np
from gen_sphere import gen_sphere
from model_class import model
from add_sphere import addSphere
import scipy

def norm(x):
    return x/np.amax(np.abs(x))

sph_coord_sph = (1300000, 35, 0)     # 3000 km depth, 20 degrees N, 50 degrees E
sph_rad = 4000                        # 10 km

# Convert the ellipsoidal (geographic) coordinates to x,y,z:
d  = sph_coord_sph[0]
lat = np.radians(sph_coord_sph[1])
lon = np.radians(sph_coord_sph[2])
e2  = 6.69437999014*(10**(-3))  # WGS84
a = 6378137.0
b = 6356752.3
N = a/np.sqrt(1 - e2*(np.sin(lat)**2))

e2  =0  # WGS84
a = 6371000.0
b = 6371000.0


X = (N - d )*np.cos(lat)*np.cos(lon)
Y = (N - d)*np.cos(lat)*np.sin(lon)
Z = ((1-e2)*N - d)*np.sin(lat)

# Convert centre to xyz:
# Model parameters
freq = 2        # [Hz]
min_vel = 8000  # [m/s]
epw = 3         # 3 elements per wavelength

p = sph_rad*2.0
# Model dimensions
x = np.array([-p, p]) + X # Model from -150,000 [m] to +150,000 [m] in x direction
y = np.array([-p, p]) + Y # Model from -150,000 [m] to +150,000 [m] in y direction
z = np.array([-p, p]) + Z # Model from -100,000 [m] to +100,000 [m] in z direction

m = model(x,y,z, epw, freq, min_vel, oversaturation=5)

sph = gen_sphere(model=m, radius=sph_rad, RHO=2500, VP=2500, VS=2300)
sph.set_centre(np.array([X,Y,Z]), m, print_conf='n')
# Add sphere to model:
m = addSphere(sph, m)

# Now need to convert our cartesian back to geographic
x_array = np.linspace(m.x_lim[0], m.x_lim[1], m.nx)
y_array = np.linspace(m.y_lim[0], m.y_lim[1], m.ny)
z_array = np.linspace(m.z_lim[0], m.z_lim[1], m.nz)

X,Y,Z = np.meshgrid(x_array, y_array, z_array)

x = X.flatten()
y = Y.flatten()
z = Z.flatten()

# Now need to convert each coordinate back to geographic:
p = ((x**2 + y**2)**0.5)

lat_i = np.arctan(z / ((1-e2)*p))

n=50
for i in range(n):
    N = a/(1 - e2*(np.sin(lat_i))**2)**0.5
    h = p/np.cos(lat_i) - N
    lat_i = np.arctan( z/( p*(1 - (e2*(N/(N+h)))) ) )

# This is now our lat, long, depth coordinates for our blob
longitude = np.rad2deg(np.arctan(y/x))
latitude = np.rad2deg(lat_i)
h = -h  # Flip sign so depth is positive


# Now need to re-sample the data at even spacing in lat-lon-depth space:
lon_min = np.min(longitude)
lon_max = np.max(longitude)
lat_min = np.min(latitude)
lat_max = np.max(latitude)
depth_min = np.min(h)
depth_max = np.max(h)


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata as gd
import time


#grid = np.zeros(K.shape)

v = m.bm_vp.flatten()
x = latitude[v!=0]
y = longitude[v!=0]
z = h[v!=0]
v = v[v!=0]


# Prescribe grid in regular lat-long-depth:
n = 80
k = np.arange(lat_min, lat_max+(lat_max-lat_min)/n, (lat_max-lat_min)/n)
l = np.arange(lon_min, lon_max+ (lon_max-lon_min)/n, (lon_max-lon_min)/n)
j = np.arange(depth_min, depth_max+ (depth_max-depth_min)/n, (depth_max-depth_min)/n)
K, L, J = np.meshgrid(k, l, j)

"""
dist_min = np.infty
# Now for each scattered data point we want to find its nearest grid point
for p in range(len(v)):
    px = x[p]
    py = y[p]
    pz = z[p]

    for kp in k:
        for lp in l:
            for jp in j:
                dist = ((px - kp)**2 + (py - lp)**2 + (pz - jp)**2)**0.5
                if dist < dist_min:
                    dist_min = np.copy(dist)
                    min_x = np.copy(px)
                    min_y = np.copy(py)
                    min_z = np.copy(pz)
"""

interp = scipy.interpolate.griddata(points=(latitude, longitude, h), values=m.bm_vp.flatten(),
                           xi = (K.flatten(), L.flatten(), J.flatten()), method='nearest',
                           rescale=True)

fig1 = plt.figure()
ax1=fig1.gca(projection='3d')

ax1.scatter(x,y,z, c=v)


fig2 = plt.figure()
ax2=fig2.gca(projection='3d')

ax2.scatter(K.flatten()[interp>0], L.flatten()[interp>0], J.flatten()[interp>0], c=interp[interp>0])



plt.show()










import netCDF4 as nc
"""
fname = 'test1.nc'

f = nc.Dataset(fname, 'w', format='NETCDF4')
# Create dimension arrays
# We now create the dimensions:
lat_dim = f.createDimension('lat_dim', len(latitude))
lon_dim = f.createDimension('lon_dim', len(longitude))
depth_dim = f.createDimension('depth_dim', len(h))
# Creating the variables:
lat     = f.createVariable('lat', 'f4', ('lat_dim',))
lat.units = 'degrees_north'
lat.long_name = 'latitude'
lon     = f.createVariable('lon', 'f4', ('lon_dim',))
lon.units = 'degrees_east'
lon.long_name = 'longitude'
depth   = f.createVariable('depth', 'f4', ('depth_dim',))
depth.units = 'metres'
depth.long_name = 'depth'
v_rho = f.createVariable('rho', 'f4', ('lat_dim',))    # Pretty sure they should all be the same dimension
v_vp  = f.createVariable('vp', 'f4', ('lat_dim',))
v_vs  = f.createVariable('vs', 'f4', ('lat_dim',))
# Assigning values to the variables:
lat[:]   = latitude
lon[:]   = longitude
depth[:] = h
v_rho[:] = m.bm_rho
v_vp[:]  = m.bm_vp.flatten()
v_vs[:]  =  m.bm_vs.flatten()
print('Data written to file ', fname)
f.close()"""