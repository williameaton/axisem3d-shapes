import numpy as np
from shape import Object




class Cylinder(Object):
    def __init__(self, model, vp, vs, rho, dim, loc=None):
        # Set the Vp, Vs Rho and location
        super().__init__(model, vp, vs, rho, dim, loc)

        # These parameters should be given by the location variable - Location should be x, y, z, radius:
        self.n_centre = np.array([0,0,0])

        self.set_dimensions(self.dim)

        print("Generated cylinder.")



    def gen_obj(self):
        # Calculate the number of iterations based on radius and element size:
        x_loop = int(self.h // self.m.dx)*self.expand_int
        y_loop = int(self.rad // self.m.dy)*self.expand_int
        z_loop = int(self.rad // self.m.dz)*self.expand_int



        # Create spare array that holds sphere info for duplicate spheres
        # This will store values of '1' or '0' for whether the element is within the sphere radius
        cyl = np.zeros((int(2*x_loop+1), int(2*y_loop+1), int(2*z_loop+1)))

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


                    if np.abs(rot_coords[0]) <= self.h:
                        if (rot_coords[1]**2 + rot_coords[2]**2)**0.5 <= self.rad:
                            cyl[int(i)+x_loop, int(j)+y_loop, int(k)+z_loop] = 1

        # This loop gives us the positive octet - now need to mirror for all other octets:
        #self.obj = np.lib.pad(ell, ((x_loop, 0), (y_loop, 0), (z_loop, 0)), 'reflect')
        self.obj = cyl



    def set_dimensions(self, radius):
        if len(np.array(radius))==5:
            # Radius holds the e1, e2, e3 radii
            self.h = self.dim[0]        # Half length of cylinder
            self.rad = self.dim[1]      # Radius of circular cross-section
            self.theta = self.dim[2]
            self.phi = self.dim[3]
            self.expand_int = int(self.dim[4])
        else:
            raise ValueError("5 values required: h, rad, theta, phi, expand_int")

        self.gen_obj()
        self._reset_sa_centre()



