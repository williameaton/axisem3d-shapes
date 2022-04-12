Model class
===============
.. automodule:: model
   :members:
   :special-members:
   :private-members:



Notes on model parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is used to define the grid resolution and has no effect on the simulation stability, but controls the resoltion of the model. Higher-resolution models are better but you are inherently limited by the GLL resolution in the AxiSEM-3D mesh. Higher-resolution models take longer to calculate and create larger .nc files which may be a bottleneck for AxiSEM3D which loads all models using a single node even in parallel implementations: your models (.nc files) are therefore limited by the memory on nodes being used.
