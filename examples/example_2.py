# Example 2:
# Let us suppose we want to make a 3D model that is layered in one direction and also has a blob in it.
# There are two ways you could do this in axisem3D:
# 1) Create a homogenous 1D model and then a layered 3D model + a blob (this is what is happening in this example)
# 2) Use a layered 1D model and then just a blob in a homogenous 3D model - this is definitely the best way to do it. In
# this case I am just doing this example to demonstrate that you can have whatever 3D model you want and inject blobs
# into it


import numpy as np
from model_class import model
from gen_sphere import gen_sphere
from write_NetCDF import writeNetCDF
from add_sphere import addSphere


# Model dimensions
x = np.array([0, 20000])
y = np.array([0, 20000])
z = np.array([0, 50000])

# Model parameters
freq = 3        # [Hz]
min_vel = 3000  # [m/s]
epw = 3         # 3 elements per wavelength - pretty high res.


# As before, this is going to create an empty 3D box - we can now update this before adding any spheres:
# YOU COULD ALTERNATIVELY HAVE SOME 3D MODEL CREATED. IN THIS CASE YOU WOULD PROBABLY STILL WANT TO MAKE AN INSTANCE
# OF THIS MODEL CLASS AND THEN JUST SET THE model.set_bm_rho() etc... Note that the other parameters like the number of
# elements wont adapt to this update (unless you edit the functions which should be trivial) so be careful with that.
m = model(x,y,z, epw, freq, min_vel, oversaturation=1)

# Lets take our initial background model for vp:
vp_array = m.bm_vp

dis = np.array([0, 10000, 18000, 30000, 50000]) # 0 is surface in this case
layer_vps = np.array([3000, 3300, 4000, 4400])

# get corresponding z indicies for the discontinuities:
dis_indices = dis*m.nz/(z[1]-z[0])

for i in range(len(layer_vps)):
    vp_array[:,:, int(dis_indices[i]):int(dis_indices[i+1])] = layer_vps[i]

# Now we have our layered array, we can update the bm_models:
m.set_bm_vp(vp_array)
# Lets imagine that the vs structure is the same:
m.set_bm_vs(vp_array)
# But we dont change the rho structure so it is still homogenous - this is obviously kinda silly but still...

writeNetCDF(m, "example2.nc")

# What if we now want to add in a blobs to this? Simple. We first take our model and generate a sphere:
sph = gen_sphere(model=m, radius=5000, RHO=2500, VP=2500, VS=2300)

sphere_centre = [5000, 10000, 49400]

sph.set_centre(sphere_centre, m, print_conf='n')
# Add sphere to model:
m = addSphere(sph, m)

writeNetCDF(m, "example2_withblob.nc")

