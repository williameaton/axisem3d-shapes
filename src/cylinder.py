import numpy as np
from shape import Object


class Cylinder(Object):
    def __init__(self, model, vp, vs, rho, dim, loc=None, major_axis='X'):
        """
        :param model: The instance of :class:`~model.Model` object shape is injected into.
        :type  model: :class:`~model.Model`
        :param vp: t
        :param vs:t
        :param rho:t
        :param dim:t
        :param loc:t
        :param major_axis:t
        """

        # Set the Vp, Vs Rho and location
        self.shape_name = "cylinder"
        self.maxis = major_axis.upper()
        super().__init__(model, vp, vs, rho, dim, loc)

    def _in_shape_condition(self, rot_coords):
        if np.abs(rot_coords[self._hind]) <= self.h:
            if (rot_coords[self._aind1] ** 2 + rot_coords[self._aind2] ** 2) ** 0.5 <= self.rad:
                return True
            else:
                return False

    def set_dimensions(self, radius):
        if len(np.array(radius))==5:
            # Radius holds the e1, e2, e3 radii
            self.h = self.dim[0]/2        # Half length of cylinder
            self.rad = self.dim[1]        # Radius of circular cross-section
            self.theta = self.dim[2]
            self.phi = self.dim[3]
            self.expand_int = int(self.dim[4])
        else:
            raise ValueError("5 values required: h, rad, theta, phi, expand_int")

        self.gen_obj()
        self._reset_sa_centre()


    def get_iter_no(self):
        # THIS NEEDS CLEANING UP
        if self.maxis == 'X':
            x_loop = int(self.h // self.m.dx) * self.expand_int
            y_loop = int(self.rad // self.m.dy) * self.expand_int
            z_loop = int(self.rad // self.m.dz) * self.expand_int
            self._hind = 0
            self._aind1 = 1
            self._aind2 = 2
        elif self.maxis =='Y':
            x_loop = int(self.rad // self.m.dx) * self.expand_int
            y_loop = int(self.h // self.m.dy) * self.expand_int
            z_loop = int(self.rad // self.m.dz) * self.expand_int
            self._hind = 1
            self._aind1 = 0
            self._aind2 = 2
        elif self.maxis == 'Z':
            x_loop = int(self.rad // self.m.dx) * self.expand_int
            y_loop = int(self.rad // self.m.dy) * self.expand_int
            z_loop = int(self.h // self.m.dz) * self.expand_int
            self._hind = 2
            self._aind1 = 0
            self._aind2 = 1
        else:
            raise ValueError("major_axis must be X, Y or Z")
        return x_loop, y_loop, z_loop


