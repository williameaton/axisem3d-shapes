import numpy as np
from shape import Object
from copy import copy

class Sphere(Object):
    def __init__(self, model, vp, vs, rho, dim, loc=None):
        # Set the Vp, Vs Rho and location
        super().__init__(model, vp, vs, rho, dim, loc)

        # These parameters should be given by the location variable - Location should be x, y, z, radius:
        self.n_centre = np.array([0,0,0])

        # Setting radius - also generates model and updates centre indices of 3D array:
        # Note that these extra bits are within the set_radius function as they need to be recalculated any time
        # the radius is changed
        self.set_radius(dim)


    def set_loc(self, centre):
        self.centre = centre
        # Initialise centre:
        self.n_centre = np.array([0, 0, 0])

        self.n_centre[0] = int(self.m.unpadded_n[0] * (centre[0] - self.m.x_lim[0])  // self.m.x_length)
        self.n_centre[1] = int(self.m.unpadded_n[1] * (centre[1] - self.m.y_lim[0])  // self.m.y_length)
        self.n_centre[2] = int(self.m.unpadded_n[2] * (centre[2] - self.m.z_lim[0])  // self.m.z_length)

        #if print_conf.upper() == "Y":
        #    print("Centre of sphere set at", centre, "with normalised indices", self.n_centre)


    def gen_obj(self):
        # Calculate the number of iterations based on radius and element size:
        x_loop = int(self.radius // self.m.dx)
        y_loop = int(self.radius // self.m.dy)
        z_loop = int(self.radius // self.m.dz)

        # Create spare array that holds sphere info for duplicate spheres
        # This will store values of '1' or '0' for whether the element is within the sphere radius
        sph = np.zeros((int(x_loop+1), int(y_loop+1), int(z_loop+1)))


        # Calculating the valid array elements for a circle in the positive x,y,z octet
        # Loop over all dimensions:
        for k in np.arange(0, z_loop + 1):
            for j in np.arange(0, y_loop + 1):
                for i in np.arange(0, x_loop + 1):

                    # check element is within radius:
                    element_radius = (((i * self.m.dx) ** 2) + ((j * self.m.dy) ** 2) + ((k * self.m.dz) ** 2)) ** 0.5

                    if element_radius <= self.radius:
                        sph[i, j, k] = 1

        # This loop gives us the positive octet - now need to mirror for all other octets:
        self.obj = np.lib.pad(sph, ((x_loop, 0), (y_loop, 0), (z_loop, 0)), 'reflect')


    def _reset_sa_centre(self):
        # Calculate the index within the sphere array of the centre point of that array
        self.sa_centre = np.array([0, 0, 0])
        for i in range(3):
            self.sa_centre[i] = np.floor(np.asarray(self.obj.shape)[i] / 2)

        self.sa_centre_original = copy(self.sa_centre)


    def _update_sph_centre_index(self, new_index):
        self.sa_centre = new_index


    def set_radius(self, radius):
        if type(radius) == float or type(radius) == int or len(radius) == 1:
            self.radius = radius
        else:
            raise ValueError("Dim/radius must have dimensions of 1 (sphere)")

        self.gen_obj()
        self._reset_sa_centre()
