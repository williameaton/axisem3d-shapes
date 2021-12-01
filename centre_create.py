import numpy as np
# ____________________________________________________________________________________________________________________________________________________
def centre_create(model, mfp, domain, spec_domain,  type='edge'):

    if domain.upper() == 'SINGLE':
        X, Y, Z = np.mgrid[model.x_lim[0]:model.x_lim[1] + 0.1:mfp, model.y_lim[0]:model.y_lim[1]+0.1:mfp, model.z_lim[0]:model.z_lim[1]+0.1:mfp]

        # Centre in x and y:
        x_centre_max = X[-1,0,0]
        y_centre_max = Y[0,-1,0]
        z_centre_max = Z[0,0,-1]

        x_add = (model.x_lim[1]-x_centre_max)/2
        y_add = (model.y_lim[1]-y_centre_max)/2
        z_add = (model.z_lim[1]-z_centre_max)/2

        X += x_add
        Y += y_add
        Z += z_add

        xyz = np.vstack((X.flatten(), Y.flatten(), Z.flatten())).T
        return(xyz)