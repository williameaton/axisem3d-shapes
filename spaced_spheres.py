from centre_create import centre_create
from add_sphere import addSphere

def spaced_spheres(sphere, model, mfl, print_time='n', domains='SINGLE', spec_domain=[], type='edge'):

    # Create an array holding the location of sphere centres:
    sc = centre_create(model, mfl, domains, spec_domain=spec_domain,  type=type, )

    for i in range(sc.shape[0]):
        # print("Adding sphere at ", sc[i, :])
        # Set centre of the sphere:
        sphere.set_centre(sc[i, :], model, print_conf='n')
        # Add sphere to model:
        final = addSphere(sphere, model, print_time='n')

    print("Added", sc.shape[0], "spheres to model")
    return final