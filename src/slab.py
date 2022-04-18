from object import Object
import numpy as np

class Slab(Object):
    def __init__(self, model, vp, vs, rho, dim, loc=None):
        self.shape_name = "slab"
        super().__init__(model, vp, vs, rho, dim, loc)


    def _in_shape_condition(self, rot_coords):
        ctr = 0
        for i in range(3):
            if np.abs(rot_coords[i]) > self.lengths[i]:
                ctr += 1

        if ctr == 0:
            return True
        else:
            return False


    def set_dimensions(self, dim):
        if len(np.array(dim))==6:
            self.lengths = self.dim[:3]/2
            self.theta = self.dim[3]
            self.phi = self.dim[4]
            self.expand_int = int(self.dim[5])
        else:
            raise ValueError("Dim must have 6 entries: 3 length scales, theta, phi and expand_int (see manual).")

        self._gen_obj()
        self._reset_sa_centre()

