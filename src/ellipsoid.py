import numpy as np
from shape import Object

class Ellipsoid(Object):
    def __init__(self, model, vp, vs, rho, dim, loc=None):
        self.shape_name = "ellipsoid"
        super().__init__(model, vp, vs, rho, dim, loc)


    def _in_shape_condition(self, rot_coords):
        rad = (rot_coords[0] ** 2) / (self.radius[0] ** 2) + (rot_coords[1] ** 2) / (self.radius[1] ** 2) + (
                    rot_coords[2] ** 2) / (self.radius[2] ** 2)
        if rad <= 1:
            return True
        else:
            return False


    def set_dimensions(self, radius):
        if type(radius) == float or type(radius) == int or len(radius) == 1:
            self.radius = radius
        elif len(np.array(radius))==6:
            # Radius holds the e1, e2, e3 radii
            self.radius = self.dim[:3]
            self.theta = self.dim[3]       #
            self.phi = self.dim[4]         #
            self.expand_int = int(self.dim[5])  #
        else:
            raise ValueError("Dim/radius must have either 1 entry (sphere radius) or 5 (3 radii + theta, phi)")

        self.gen_obj()
        self._reset_sa_centre()


    def get_iter_no(self):
        x_loop = int(self.radius[0] // self.m.dx) * self.expand_int
        y_loop = int(self.radius[1]  // self.m.dy) * self.expand_int
        z_loop = int(self.radius[2]  // self.m.dz) * self.expand_int
        return x_loop, y_loop, z_loop


