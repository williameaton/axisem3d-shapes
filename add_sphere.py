import numpy as np

from sphere_class import sphere
from slice_sphere import slice_sphere
from inject import inject_sphere

def addSphere(sph, model, print_time='n'):

    # Extract sph_input:
    sph_input = sphere(sph.sphere, sph.vp, sph.vs, sph.rho, sph.radius)
    # update sph_input centre:
    sph_input.set_centre(sph.centre, model)

    # Slice the inputted sphere to the correct array size
    sphere_sliced = slice_sphere(sph_input, model)

    # Inject into model:
    final = inject_sphere(model, sphere_sliced)


    return final