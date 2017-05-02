===========================
Symmetry and shape analysis
===========================

Shape
-----
The shape analysis is calculated using the external software :program: `shape`.
To use the interface to shape, the binary has to be placed in a directory
included in the $PATH enviroment variable with the name :program:`shape`.
Note that setting up an alias in :file:`.profile` or :file:`bashrc` for :program:`shape will not work.

To use shape interface, shape module has to be loaded by ::

   $ module load montemodes.functions.shape as shape

The use of shape module is divided in two parts:
First a shape input object is created. This shape object defines the kind of
shape calculation to perform ::

   $ input_shape = shape.Shape(code=1,
                               central_atom=0,
                               custom_atom_list=None)

- code: corresponds to the shape code available in shape manual. It depends on the number of vertices.
- central_atoms: defines the atom number that will be used as central atom. Atom number uses the same rule as
:program:`shape` where the first atom is atom number 1. If central_atom is 0 no central atom will be defined.
- custom_atom_list: defines a list of atoms of the structure that will be used in the shape calculation. If this value
is None all atoms are used.

methods
+++++++

- get_shape(structure   (type Structure),
            input_shape (type Shape):
Get the shape measure of a structure


- get_shape_trajectory(trajectory (list of Structure),
                       input_shape (type Shape):
Get the shape of a list of structures

- get_info(vertices=None):
Get information about available shapes. (equivalent to shape +).


example
+++++++
::

   $ impAddeort montemodes.functions.reading as io_monte
   $ import montemodes.functions.shape as shape

   $ structure = io_monte.reading_from_xyz_file('ch4.xyz')
   $ module load montemodes.functions.shape as shape
   $ input_shape = shape.Shape(code=2,
                               central_atom=1,
                               custom_atom_list=None)

   $ measure = get_shape(structure)
   $ print ('The T-4 shape measure of CH4 is {}'.format(measure))

