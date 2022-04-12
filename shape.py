# Abstract base class for shapes from which all shapes will inherit:
from abc import ABC, abstractmethod
import numpy as np
from copy import copy

class Object(ABC):

    @abstractmethod
    def __init__(self, model, vp, vs, rho, dim, loc=None):
        """ Abstract base class for all shapes. Can not be instantiated itself."""
        # General:
        self.dim = np.array(dim)
        self.obj = None
        self.sliced = None

        # Location:
        if loc != None:
            self.loc = loc

            # Shape properties:
        self.vp  = vp
        self.vs  = vs
        self.rho = rho

        # Model:
        self.m = model

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
