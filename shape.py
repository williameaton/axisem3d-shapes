# Abstract base class for shapes from which all shapes will inherit:
from abc import ABC, abstractmethod
import numpy as np

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

