import netCDF4 as nc
import numpy as np 
def writeNetCDF(m, filename):

    f = nc.Dataset(filename, 'w', format='NETCDF4')
    # Create dimension arrays
    x_array = np.linspace(-m.x_lim[1]/2, m.x_lim[1]/2, m.nx)
    y_array = np.linspace(-m.y_lim[1]/2, m.y_lim[1]/2, m.ny)
    z_array = np.linspace(-m.z_lim[0], m.z_lim[1], m.nz)
    # We now create the dimensions:
    x_dim = f.createDimension('x_dim', m.nx)
    y_dim = f.createDimension('y_dim', m.ny)
    z_dim = f.createDimension('z_dim', m.nz)
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
    v_rho[:,:,:] = m.bm_rho
    v_vp[:,:,:]  =  m.bm_vp
    v_vs[:,:,:]  =  m.bm_vs
    print('Data written to file ', filename)
    f.close()