import math
import numpy as np
import netCDF4 as nc

class model(object):

    def __init__(self, x_lim, y_lim, z_lim, elements_per_wavelength, dominant_freq, min_velocity, oversaturation=1):
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.z_lim = z_lim
        self.epw = elements_per_wavelength
        self.freq = dominant_freq
        self.min_velocity = min_velocity

        # Calculate min wavelength from frequency and min velocity
        self.min_wavelength = min_velocity/dominant_freq

        # Calculate the number of elements in each dimension based on domain size, min wavelength and elements per wavelength
        self.nx = oversaturation*math.ceil((x_lim[1] - x_lim[0])*self.epw /self.min_wavelength)
        self.ny = oversaturation*math.ceil((y_lim[1] - y_lim[0])*self.epw /self.min_wavelength)
        self.nz = oversaturation*math.ceil((z_lim[1] - z_lim[0])*self.epw /self.min_wavelength)

        # For global:
        # Ensure that nx, ny, nz are odd
        if self.nx%2==0:
            self.nx += 1
        if self.ny % 2 == 0:
            self.ny += 1
        if self.nz % 2 == 0:
            self.nz += 1
        
        # Some details on the original 3D model (homogenous in this case)
        self.padding = np.array([0, 0, 0])
        self.unpadded_n = np.array([self.nx, self.ny, self.nz])
        self.original_shape = np.array([self.nx, self.ny, self.nz])

        # Calculate the length of each dimension:
        self.x_length = self.x_lim[1] - self.x_lim[0]
        self.y_length = self.y_lim[1] - self.y_lim[0]
        self.z_length = self.z_lim[1] - self.z_lim[0]

        # Calculate spatial step sizes
        self.dx = self.x_length / self.nx
        self.dy = self.y_length / self.ny
        self.dz = self.z_length / self.nz

        # Define a default background model arrays for Rho, Vp and Vs which are zeros 3D arrays of the correct size:
        # Note here that the model is defined originally as homogenous
        # This could be edited to take an input from the user of some pre-defined 3D array that has non-zero values
        self.bm_rho = np.zeros((self.nx, self.ny, self.nz))
        self.bm_vp  = np.zeros((self.nx, self.ny, self.nz))
        self.bm_vs  = np.zeros((self.nx, self.ny, self.nz))


    

    import numpy as np 
    def writeNetCDF(self, filename):

        f = nc.Dataset(filename, 'w', format='NETCDF4')
        
        # Create dimension arrays
        x_array = np.linspace(-self.x_lim[1]/2, self.x_lim[1]/2, self.nx)
        y_array = np.linspace(-self.y_lim[1]/2, self.y_lim[1]/2, self.ny)
        z_array = np.linspace(-self.z_lim[0], self.z_lim[1], self.nz)
        
        # Create the dimensions:
        x_dim = f.createDimension('x_dim', self.nx)
        y_dim = f.createDimension('y_dim', self.ny)
        z_dim = f.createDimension('z_dim', self.nz)
        
        # Creating the variables:
        x   = f.createVariable('x', 'f4', ('x_dim',))
        y   = f.createVariable('y', 'f4', ('y_dim',))
        z   = f.createVariable('z', 'f4', ('z_dim',))
        v_rho = f.createVariable('rho', 'f4', ('x_dim', 'y_dim', 'z_dim',))
        v_vp  = f.createVariable('vp', 'f4', ('x_dim', 'y_dim', 'z_dim',))
        v_vs  = f.createVariable('vs', 'f4', ('x_dim', 'y_dim', 'z_dim',))
        
        # Assigning values to the variables:
        x[:] = x_array
        y[:] = y_array
        z[:] = z_array
        v_rho[:,:,:] = self.bm_rho
        v_vp[:,:,:]  =  self.bm_vp
        v_vs[:,:,:]  =  self.bm_vs
        print('Data written to file ', filename)
        f.close()

    # Functions for updating 
    def set_bm_rho(self, bm_rho):
        self.bm_rho = bm_rho

    def set_bm_vp(self, bm_vp):
        self.bm_rho = bm_vp

    def set_bm_vs(self, bm_vs):
        self.bm_rho = bm_vs
