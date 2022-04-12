# AxiSEM-3D_shapes




Author: Will Eaton, Princeton University 2021 \
Last modified: April 12th 2022 \
Contact: weaton@princeton.edu 

Short description: \
A small repo containing scripts to inject shapes such as ellipsoids, slabs and cylinders into 3D cartesian models for use in AxiSEM3D.

## Overview: 
Full documentation can be found ... . If you have any questions please open an issue or contact me via email.

Three classes provide the functionality of this package: 
 * ```Model``` is used to create a background cartesian grid into which shapes can be added. This can represent the entire domain you are simulating, or a subset of it. It holds, among other things, three arrays ```VP```, ```VS``` and ```RHO``` which eventually stored in NetCDF files for AxiSEM-3D to read. 
 * ```Shape``` is an abstract base class. Subclasses of this (e.g. ```Ellipsoid``` or ```Cylinder```) can be instantiated and injected into the model arrays (e.g. ```VP```) using an ```Injector``` object
 * ```Injector``` are instantiated by passing in a ```Model``` object, and are used to inject ```Shape``` objects into the ```Model``` arrays. 

Shapes can be created with dimensions and orientation specified by the user. Originally these codes were just written for injecting spheres. As such, the position of shapes is located by a central point of the shape, rather than an edge. I may add more flexibility for this in the future.

I recommend viewing your generated models in Paraview to check everything has worked, before running simulations. 

## Still to do:
* Complete testing of all scripts 
* Global (spherical) wrapper for use in non-cartesian Axisem-3D.
* Parallel grid searches for shape construction? 

