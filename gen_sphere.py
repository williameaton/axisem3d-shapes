import numpy as np
from sphere_class import sphere

def gen_sphere(model, radius, RHO, VP, VS):

    # Calculate domain sizes for scaling:
    x_len = model.x_lim[1] - model.x_lim[0]
    y_len = model.y_lim[1] - model.y_lim[0]
    z_len = model.z_lim[1] - model.z_lim[0]

    # Calculate spatial step sizes
    dx = x_len / model.nx
    dy = y_len / model.ny
    dz = z_len / model.nz

    r_original = radius

    # Calculate the number of iterations based on radius and element size:
    x_loop = int(radius // dx)
    y_loop = int(radius // dy)
    z_loop = int(radius // dz)

    # Create spare array that holds sphere info for duplicate spheres
    # This will store values of '1' or '0' for whether the element is within the sphere radius
    sph = np.zeros((int(x_loop+1), int(y_loop+1), int(z_loop+1)))


    # Calculating the valid array elements for a circle in the positive x,y,z octet
    # Loop over all dimensions:
    for k in np.arange(0, z_loop + 1):
        for j in np.arange(0, y_loop + 1):
            for i in np.arange(0, x_loop + 1):

                # check element is within radius:
                element_radius = (((i * dx) ** 2) + ((j * dy) ** 2) + ((k * dz) ** 2)) ** 0.5

                if element_radius <= radius:

                    sph[i, j, k] = 1

    # This loop gives us the positive octet - now need to mirror for all other octets:
    # This reflects s along the first column and row as mirror axes and adds sph_x - 1 etc elements (ie ignoring the row/column being used as the mirror axis)
    # Initialise matrix
    sph_full = np.zeros((2*int(x_loop+1)-1, 2*int(y_loop+1)-1, 2*int(z_loop+1)-1))
    sph_full = np.lib.pad(sph, ((x_loop, 0), (y_loop, 0), (z_loop, 0)), 'reflect')

    # Create instance of the sphere class
    sphere_instance = sphere(sph_full, VP, VS, RHO, radius)
    return sphere_instance