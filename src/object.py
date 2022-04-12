from abc import ABC, abstractmethod
import numpy as np
from copy import copy

class Object(ABC):
    @abstractmethod
    def __init__(self, model, vp, vs, rho, dim, loc=None):
        # General:
        self.dim = np.array(dim)
        self.obj = None
        self.sliced = None

        # Location:
        if loc != None:
            self.loc = loc

        self.vp  = vp
        self.vs  = vs
        self.rho = rho
        self.m   = model

        # These parameters should be given by the location variable - Location should be x, y, z, radius:
        self.n_centre = np.array([0, 0, 0])

        # Setting radius - also generates model and updates centre indices of 3D array:
        # Note that these extra bits are within the set_radius function as they need to be recalculated any time
        # the radius is changed
        self.set_dimensions(self.dim)

        print(f"Generated {self.shape_name}.")



    @abstractmethod
    def gen_obj(self):
        pass

    # Some generic updating functions:
    def update_vp(self, new_vp):
        self.vp = new_vp

    def update_vs(self, new_vs):
        self.vs = new_vs

    def update_rho(self, new_rho):
        self.rho = new_rho

    def set_loc(self, centre):
        self.centre = centre
        # Initialise centre:
        self.n_centre = np.array([0, 0, 0])

        self.n_centre[0] = int(self.m.unpadded_n[0] * (centre[0] - self.m.x_lim[0])  // self.m.x_length)
        self.n_centre[1] = int(self.m.unpadded_n[1] * (centre[1] - self.m.y_lim[0])  // self.m.y_length)
        self.n_centre[2] = int(self.m.unpadded_n[2] * (centre[2] - self.m.z_lim[0])  // self.m.z_length)

    def _reset_sa_centre(self):
        # Calculate the index within the sphere array of the centre point of that array
        self.sa_centre = np.array([0, 0, 0])
        for i in range(3):
            self.sa_centre[i] = np.floor(np.asarray(self.obj.shape)[i] / 2)

        self.sa_centre_original = copy(self.sa_centre)

    def _update_sph_centre_index(self, new_index):
        self.sa_centre = new_index

    def _calc_rtn_matrices(self):
        self.Ry = np.array([[np.cos(self.theta), 0, np.sin(self.theta)],
                            [0, 1, 0],
                            [-np.sin(self.theta), 0, np.cos(self.theta)]])

        self.Rz = np.array([[np.cos(self.phi), -np.sin(self.phi), 0],
                            [np.sin(self.phi), np.cos(self.phi), 0],
                            [0, 0, 1]])



    def gen_obj(self):
        # Calculate the number of iterations based on radius and element size:
        x_loop, y_loop, z_loop = self.get_iter_no()


        # Create spare array that holds sphere info for duplicate spheres
        # This will store values of '1' or '0' for whether the element is within the sphere radius
        shape = np.zeros((int(2*x_loop+1), int(2*y_loop+1), int(2*z_loop+1)))

        self._calc_rtn_matrices()

        # Calculating the valid array elements for an ellipse in the positive Y domain (then reflect for other half)
        for k in np.arange(-z_loop, z_loop + 1):
            for i in np.arange(-x_loop, x_loop + 1):
                for j in np.arange(-y_loop, y_loop + 1):

                    cart_coords = np.array([i * self.m.dx,
                                            j * self.m.dy,
                                            k * self.m.dz])

                    # Rotation of cartesian coordinates
                    rot_coords = np.matmul(self.Rz,    np.matmul( self.Ry, cart_coords))

                    # Check if grid point inside shape
                    if self._in_shape_condition(rot_coords) == True:
                        shape[int(i) + x_loop, int(j) + y_loop, int(k) + z_loop] = 1

        self.obj = shape