import numpy as np
from shape import Object

class Sphere(Object):
    def __init__(self, model, vp, vs, rho, dim, loc=None):
        # Set the Vp, Vs Rho and location
        self.shape_name = 'sphere'
        super().__init__(model, vp, vs, rho, dim, loc)



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



    def set_dimensions(self, radius):
        if type(radius) == float or type(radius) == int or len(radius) == 1:
            self.radius = radius
        else:
            raise ValueError("Dim/radius must have dimensions of 1 (sphere)")

        self.gen_obj()
        self._reset_sa_centre()
