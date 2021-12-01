import numpy as np
# _____________________________________________________________________________________________________________________________________________________
def inject_sphere(model, sphere, print_conf="N"):
    # Lower bound index is given by the index location of the sphere centre (in domain coordinates) - index location of
    # the sphere's centre within the sliced sphere array
    lb = sphere.n_centre - sphere.sa_centre # array for [z,y,x]
    # Upper bound is given by centre of the sphere (in domain) + shape of the sliced array - index location of the sphere
    ub = sphere.n_centre + np.asarray(sphere.sphere.shape) - sphere.sa_centre
    # Creating array to inject for each parameter:
    vp_inj = sphere.sphere * sphere.vp
    vs_inj = sphere.sphere * sphere.vs
    rho_inj = sphere.sphere * sphere.rho

    # This ensures only the non-zeros elements are changed: will be a problem if any part inside the blob actually is
    # meant to be zero but I will need to conjure up a better method in that case...
    truth = vp_inj!=0

    # inject:
    model.bm_vp[lb[0]:ub[0], lb[1]:ub[1] ,lb[2]:ub[2]][truth] = vp_inj[truth]
    model.bm_vs[lb[0]:ub[0], lb[1]:ub[1] ,lb[2]:ub[2]][truth] = vs_inj[truth]
    model.bm_rho[lb[0]:ub[0], lb[1]:ub[1] ,lb[2]:ub[2]][truth] = rho_inj[truth]

    return model