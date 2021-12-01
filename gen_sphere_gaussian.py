from sphere_class import sphere
import  numpy as np
def gen_sphere_gaussian(m, radius, RHO, VP, VS, buffer=3, falloff=1, print_time='n'):

    # Calculate domain sizes for scaling:
    x_len = m.x_lim[1] - m.x_lim[0]
    y_len = m.y_lim[1] - m.y_lim[0]
    z_len = m.z_lim[1] - m.z_lim[0]

    # Calculate spatial step sizes
    dx = x_len / m.nx
    dy = y_len / m.ny
    dz = z_len / m.nz

    r_original = radius
    radius += falloff*dx*buffer

    # Calculate the number of iterations based on radius and element size:
    x_loop = int(radius // dx)
    y_loop = int(radius // dy)
    z_loop = int(radius // dz)

    # Create spare array that holds sphere info for duplicate spheres
    # This will store values of '1' or '0' for whether the element is within the sphere radius
    sph = np.zeros((int(x_loop+1), int(y_loop+1), int(z_loop+1)))

    # calculating values for gaussian:
    gauss_sd = dx

    # Calculating the valid array elements for a circle in the positive x,y,z octet
    # Loop over all dimensions:
    for k in np.arange(0, z_loop + 1):
        for j in np.arange(0, y_loop + 1):
            for i in np.arange(0, x_loop + 1):

                # check element is within radius:
                element_radius = (((i * dx) ** 2) + ((j * dy) ** 2) + ((k * dz) ** 2)) ** 0.5

                if element_radius <= radius:
                    # Apply parameter to the element
                    if element_radius <= r_original:
                        sph[i, j, k] = 1
                    else:
                        sph[i,j,k] = 1 * np.exp(-0.5 * (element_radius - r_original) ** 2 / gauss_sd ** 2)
    # This loop gives us the positive octet - now need to mirror for all other octets:
    # This reflects s along the first column and row as mirror axes and adds sph_x - 1 etc elements (ie ignoring the row/column being used as the mirror axis)
    # Initialise matrix

    sph_full = np.zeros((2*int(x_loop+1)-1, 2*int(y_loop+1)-1, 2*int(z_loop+1)-1))
    sph_full = np.lib.pad(sph, ((x_loop, 0), (y_loop, 0), (z_loop, 0)), 'reflect')

    # Create instance of the sphere class
    sphere_instance = sphere(sph_full, VP, VS, RHO, radius)
    return sphere_instance



    # Get non-zero values of injects:
    truth_vp = vp_inj != 0
    truth_vs = vs_inj != 0
    truth_rho = rho_inj != 0


    model.bm_vp[lb[0]:ub[0], lb[1]:ub[1] ,lb[2]:ub[2]][truth_vp] = vp_inj[truth_vp]
    model.bm_vs[lb[0]:ub[0], lb[1]:ub[1] ,lb[2]:ub[2]][truth_vs ]= vs_inj[truth_vs]
    model.bm_rho[lb[0]:ub[0], lb[1]:ub[1] ,lb[2]:ub[2]][truth_rho] += rho_inj[truth_vp]


