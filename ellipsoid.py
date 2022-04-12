import numpy as np
from shape import Object
from copy import copy
import warnings



class Ellipsoid(Object):
    def __init__(self, model, vp, vs, rho, dim, loc=None):
        # Set the Vp, Vs Rho and location
        super().__init__(model, vp, vs, rho, dim, loc)

        # These parameters should be given by the location variable - Location should be x, y, z, radius:
        self.n_centre = np.array([0,0,0])

        # Setting radius - also generates model and updates centre indices of 3D array:
        # Note that these extra bits are within the set_radius function as they need to be recalculated any time
        # the radius is changed
        self.set_radius(self.dim)

        print("Generated ellipsoid.")




    def gen_obj(self):
        # Calculate the number of iterations based on radius and element size:
        x_loop = int(self.radius[0] // self.m.dx)*self.expand_int
        y_loop = int(self.radius[1] // self.m.dy)*self.expand_int
        z_loop = int(self.radius[2] // self.m.dz)*self.expand_int

        a = self.radius[0]
        b = self.radius[1]
        c = self.radius[2]

        # Create spare array that holds sphere info for duplicate spheres
        # This will store values of '1' or '0' for whether the element is within the sphere radius
        ell = np.zeros((int(2*x_loop+1), int(2*y_loop+1), int(2*z_loop+1)))

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

                    rad = (rot_coords[0]**2)/(a**2) + (rot_coords[1]**2)/(b**2) + (rot_coords[2]**2)/(c**2)


                    if rad <= 1:
                        ell[int(i)+x_loop, int(j)+y_loop, int(k)+z_loop] = 1

        # This loop gives us the positive octet - now need to mirror for all other octets:
        #self.obj = np.lib.pad(ell, ((x_loop, 0), (y_loop, 0), (z_loop, 0)), 'reflect')
        self.obj = ell



    def set_radius(self, radius):
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



