import numpy as np
from object import Object


class Cylinder(Object):
    def __init__(self, model, vp, vs, rho, dim, loc=None, major_axis='X'):
        """
        :param model: The instance of :class:`~model.Model` object shape is injected into.
        :type  model: :class:`~model.Model`
        :param vp:    Homogenous p-wave velocity for cylinder.
        :type vp:   float
        :param vs: Homogenous s-wave velocity for cylinder.
        :type vs:   float
        :param rho: Homogenous density for cylinder.
        :type rho: float
        :param dim: Dimensions of the cylinder. These must be given in the following order: [h, rad, theta, phi, expand_int] where h is the length of the cylinder, rad is the radius of the cylinder, theta and phi are rotation angles away from the major axis and expand_int is an integer value with which to scale the grid in which the shape is searched for. See notes on expand_int below.
        :type dim: 5-element list or numpy array
        :param loc: [x,y,z] of centre of cylinder.
        :type loc: 3-element list or numpy array
        :param major_axis: Either 'X', 'Y' or 'Z'. Specifies the axis of symmetry for the cylinder.
        :type major_axis: str
        """

        # Set the Vp, Vs Rho and location
        self.shape_name = "cylinder"
        self.maxis = major_axis.upper()
        super().__init__(model, vp, vs, rho, dim, loc)

    def _in_shape_condition(self, rot_coords):
        """
        Checks if coordinates are within cylinder.

        :param rot_coords: Rotated coordinates to be checked
        :type rot_coords: Numpy array or list
        :return: bool
        """
        if np.abs(rot_coords[self._hind]) <= self.h:
            if (rot_coords[self._aind1] ** 2 + rot_coords[self._aind2] ** 2) ** 0.5 <= self.rad:
                return True
            else:
                return False

    def set_dimensions(self, dimensions):
        """
        Set dimensions for cylinder.

        :param dimensions: 5-element array/list. These must be given in the following order: [h, rad, theta, phi, expand_int] where h is the length of the cylinder, rad is the radius of the cylinder, theta and phi are rotation angles away from the major axis and expand_int is an integer value with which to scale the grid in which the shape is searched for. See notes on expand_int below.
        """
        if len(np.array(dimensions))==5:
            self.dim = dimensions         # Update dimensions array
            self.h = self.dim[0]/2        # Half length of cylinder
            self.rad = self.dim[1]        # Radius of circular cross-section
            self.theta = self.dim[2]
            self.phi = self.dim[3]
            self.expand_int = int(self.dim[4])
        else:
            raise ValueError("5 values required: h, rad, theta, phi, expand_int")

        self._gen_obj()                    # Regenerate object
        self._reset_sa_centre()           # Update centre of cylinder


    def _get_iter_no(self):
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


