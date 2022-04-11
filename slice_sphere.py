import numpy as np
from sphere_class import Sphere

def slice_sphere(sph, model, print_conf='N'):
    # Extract the sphere array
    sph_array = sph.sphere
    # extract sphere centre:
    n_centre = sph.n_centre
    # Calculate the dimensions of sphere array:
    sph_dim = np.asarray(sph_array.shape)
    # Get the index for the centre of sphere array - may need updating if slice elemets with lower indices than it
    sa_centre = sph.sa_centre
    # Get dimensions of model array:
    mod_dim = [model.nx, model.ny, model.nz]
    # Calculating the number of elements either side of the centre in the sphere array in each dimension:
    el_count = np.floor(sph_dim/2)

    # For the lower bounds:
    # Calculating difference between the number of elements left/beneath the centre in the sph_array and the index of the normalised centre position
    lb_out = np.floor(el_count - n_centre)
    # in x
    if lb_out[0] > 0:
        sph_array = sph_array[int(lb_out[0]):, :, :]
        sa_centre[0] = sa_centre[0] - lb_out[0]
    # in y
    if lb_out[1] > 0:
        sph_array = sph_array[:, int(lb_out[1]):, :]
        sa_centre[1] = sa_centre[1] - lb_out[1]

    # in z
    if lb_out[2] > 0:
        sph_array = sph_array[:, :, int(lb_out[2]):]
        sa_centre[2] = sa_centre[2]-lb_out[2]

    # For the upper bound:
    # If this is below zero then it means there are more on one side of the sph_array than there are elements between the centre point and the edge of the domain - need slicing from RHS
    ub_out = np.floor(mod_dim - (n_centre + 1) - el_count)
    # in x
    if ub_out[0] < 0:
        sph_array = sph_array[:int(ub_out[0]), :, :]
    # in y
    if ub_out[1] < 0:
        sph_array = sph_array[:, :int(ub_out[1]), :]
    # in z
    if ub_out[2] < 0:
        sph_array = sph_array[:, :, :int(ub_out[2])]

    # Create sliced sphere instance:
    sphere_sliced = sphere(sph_array, vp=sph.vp, vs=sph.vs, rho=sph.rho, radius=sph.radius)
    # Need to set centre to be the same as for the normal sphere class:
    sphere_sliced.set_centre(centre=sph.centre, model=model )

    # Update the index location of the sphere centre within the sphere array:
    sphere_sliced._update_sph_centre_index(sa_centre)

    return sphere_sliced