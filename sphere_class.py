import numpy as np

class sphere():
    def __init__(self, sphere, vp, vs, rho, radius):
        self.sphere = sphere
        self.vp = vp
        self.vs = vs
        self.rho = rho
        self.centre = np.array([0,0,0])   # by default
        self.n_centre = np.array([0,0,0]) # by default
        self.radius = radius

        # Calculate the index within the sphere array of the centre point of that array
        self.sa_centre = np.array([0,0,0])
        for i in range(3):
            self.sa_centre[i] = np.floor(np.asarray(self.sphere.shape)[i]/2)


    # Updater functions:
    def set_radius(self, radius):
        self.radius = radius

    def update_vp(self, new_vp):
        self.vp = new_vp

    def update_vs(self, new_vs):
        self.vs = new_vs

    def update_rho(self, new_rho):
        self.rho = new_rho

    def _update_sph_centre_index(self, new_index):
        self.sa_centre = new_index

    def set_centre(self, centre, model, print_conf='n'):
        self.centre = centre
        # Initialise centre:
        self.n_centre = np.array([0, 0, 0])

        self.n_centre[0] = model.unpadded_n[0] * centre[0] // model.x_length
        self.n_centre[1] = model.unpadded_n[1] * centre[1] // model.y_length
        self.n_centre[2] = model.unpadded_n[2] * centre[2] // model.z_length

        if print_conf.upper() == "Y":
            print("Centre of sphere set at", centre, "with normalised indices", self.n_centre)

