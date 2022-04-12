import numpy as np
from copy import copy
class Injector():
    def __init__(self, model):
        self.m = model


    def addObj(self, obj, location, overwrite=False):
        # update locations centre:
        obj.set_loc(location)

        # Slice the inputted sphere to the correct array size
        self.slice_obj(obj)

        # Inject into model:
        self.inject_obj(obj, overwrite)



    # _____________________________________________________________________________________________________________________________________________________
    def inject_obj(self, obj, overwrite):
        # Lower bound index is given by the index location of the sphere centre (in domain coordinates) - index location of
        # the sphere's centre within the sliced sphere array
        lb = obj.n_centre - obj.sa_centre  # array for [z,y,x]
        # Upper bound is given by centre of the sphere (in domain) + shape of the sliced array - index location of the sphere
        ub = obj.n_centre + np.asarray(obj.sliced.shape) - obj.sa_centre
        # Creating array to inject for each parameter:
        vp_inj = obj.sliced * obj.vp
        vs_inj = obj.sliced * obj.vs
        rho_inj = obj.sliced * obj.rho

        # This ensures only the non-zeros elements are changed: will be a problem if any part inside the blob actually is
        # meant to be zero but I will need to conjure up a better method in that case...
        truth = vp_inj != 0

        # inject:
        if overwrite == True:
            self.m.bm_vp[lb[0]:ub[0], lb[1]:ub[1], lb[2]:ub[2]][truth]  = vp_inj[truth]
            self.m.bm_vs[lb[0]:ub[0], lb[1]:ub[1], lb[2]:ub[2]][truth]  = vs_inj[truth]
            self.m.bm_rho[lb[0]:ub[0], lb[1]:ub[1], lb[2]:ub[2]][truth] = rho_inj[truth]
        elif overwrite == False:
            self.m.bm_vp[lb[0]:ub[0], lb[1]:ub[1], lb[2]:ub[2]][truth]  += vp_inj[truth]
            self.m.bm_vs[lb[0]:ub[0], lb[1]:ub[1], lb[2]:ub[2]][truth]  += vs_inj[truth]
            self.m.bm_rho[lb[0]:ub[0], lb[1]:ub[1], lb[2]:ub[2]][truth] += rho_inj[truth]
        else:
            raise ValueError("overwrite not given boolean value. Must be True or False.")


    def slice_obj(self, object):
        # Calculate the dimensions of sphere array:
        # Get the index for the centre of sphere array - may need updating if slice elemets with lower indices than it
        object.sliced = copy(object.obj)
        sa_centre     = copy(object.sa_centre_original)

        # Get dimensions of model array:
        mod_dim = [self.m.nx, self.m.ny, self.m.nz]

        # Calculating the number of elements either side of the centre in the sphere array in each dimension:
        el_count = np.floor(np.asarray(object.sliced.shape) / 2)

        # For the lower bounds:
        # Calculating difference between the number of elements left/beneath the centre in the sph_array and the index of the normalised centre position
        lb_out = np.floor(el_count - object.n_centre)
        # in x
        if lb_out[0] > 0:
            object.sliced =  object.sliced[int(lb_out[0]):, :, :]
            sa_centre[0] = sa_centre[0] - lb_out[0]
        # in y
        if lb_out[1] > 0:
            object.sliced =  object.sliced[:, int(lb_out[1]):, :]
            sa_centre[1] = sa_centre[1] - lb_out[1]
        # in z
        if lb_out[2] > 0:
            object.sliced =  object.sliced[:, :, int(lb_out[2]):]
            sa_centre[2] = sa_centre[2] - lb_out[2]

        # For the upper bound:
        # If this is below zero then it means there are more on one side of the sph_array than there are elements between the centre point and the edge of the domain - need slicing from RHS
        ub_out = np.floor(mod_dim - (object.n_centre + 1) - el_count)
        # in x
        if ub_out[0] < 0:
            object.sliced = object.sliced[:int(ub_out[0]), :, :]
        # in y
        if ub_out[1] < 0:
            object.sliced =  object.sliced[:, :int(ub_out[1]), :]
        # in z
        if ub_out[2] < 0:
            object.sliced =  object.sliced[:, :, :int(ub_out[2])]

        # Update the index location of the sphere centre within the sphere array:
        object._update_sph_centre_index(sa_centre)




    def spaced_obj(self, obj, mfl, overwrite=False):


        # Create an array holding the location of sphere centres:
        sc = self._centre_create(mfl)

        for i in range(sc.shape[0]):
            # Add sphere to model:
            self.addObj(obj, location=sc[i, :], overwrite=overwrite)

        print("Added", sc.shape[0], "spheres to model")



    def _centre_create(self, mfp):
        X, Y, Z = np.mgrid[self.m.x_lim[0]:self.m.x_lim[1] + 0.1:mfp, self.m.y_lim[0]:self.m.y_lim[1] + 0.1:mfp,
                  self.m.z_lim[0]:self.m.z_lim[1] + 0.1:mfp]

        # Centre in x and y:
        x_centre_max = X[-1, 0, 0]
        y_centre_max = Y[0, -1, 0]
        z_centre_max = Z[0, 0, -1]

        x_add = (self.m.x_lim[1] - x_centre_max) / 2
        y_add = (self.m.y_lim[1] - y_centre_max) / 2
        z_add = (self.m.z_lim[1] - z_centre_max) / 2

        X += x_add
        Y += y_add
        Z += z_add

        xyz = np.vstack((X.flatten(), Y.flatten(), Z.flatten())).T
        return (xyz)


