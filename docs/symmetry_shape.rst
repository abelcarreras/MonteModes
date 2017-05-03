===========================
Symmetry and shape analysis
===========================

The symetry and shape analysis is calculated using the external software :program: `shape`, :program: `symop`,
and :program: `symgroup`. To use the interfaces to the binaries have to be placed in a directory included in the
$PATH environment variable with the name :program:`shape`, :program:`symop`, and :program:`symgroup`, respectively.
Note that setting up an alias in :file:`.profile` or :file:`bashrc` for these software will not work.

Shape
-----
To use shape interface, shape module has to be loaded by ::

   $ module load montemodes.functions.shape as shape

The use of shape module is divided in two parts:
First a shape input object is created. This shape object defines the kind of
shape calculation to perform ::

   $ input_shape = shape.Shape(code=1,
                               central_atom=0,
                               custom_atom_list=None)

- code: corresponds to the shape code available in shape manual. It depends on the number of vertices.
- central_atom: defines the atom number that will be used as central atom. Atom number uses the same rule as
:program:`shape` where the first atom is atom number 1. If central_atom is 0 no central atom will be defined.
- custom_atom_list: defines a list of atoms of the structure that will be used in the shape calculation. If this value
is None all atoms are used.

methods
+++++++

- get_shape(structure [type Structure], input_shape [type Shape]):

            Return: Float

Get the shape measure of a structure


- get_shape_trajectory(trajectory [list of Structure objects], input_shape [type Shape]):

            Return: List of Float

Get the shape of a list of structures

- get_info(vertices=None):
            Return: Null

Get information about available shapes. (equivalent to shape +).


example
+++++++
::

   $ import montemodes.functions.reading as io_monte
   $ import montemodes.functions.shape as shape

   $ structure = io_monte.reading_from_xyz_file('ch4.xyz')
   $ input_shape = shape.Shape(code=2,
                               central_atom=1,
                               custom_atom_list=None)

   $ measure = get_shape(structure, input_shape)
   $ print ('The T-4 shape measure of CH4 is {}'.format(measure))



Symop
-----

To use symop interface, symop module has to be loaded by ::

   $ module load montemodes.functions.symop as symop

Likewise shape module, symop module is divided in two parts:
First a symop input object is created. This symop object defines the kind of
symmetry calculation to perform ::

   $ input_symop = symop.Symop(symmetry='c 3',
                               label=False,
                               connect=False,
                               central_atom=0,
                               custom_atom_list=None)

- symmetry: corresponds to the symmetry operation to be measured.
- label : if True adds %label keyword to symop input (check symop manual for further information).
- connect : if True adds %connect keyword to symop input (check symop manual for further information).
- central_atom: defines the atom number that will be used as central atom. Atom number uses the same rule as
:program:`symop` where the first atom is atom number 1. If central_atom is 0 no central atom will be defined.
- custom_atom_list: defines a list of atoms of the structure that will be used in the shape calculation. If this value
is None all atoms are used.

methods
+++++++

- get_symmetry(structure [type Structure], symop_input [type symop]):

               Return: Float

Get the symmetry measure of a structure.

- get_symmetry_trajectory(trajectory [type Structure], symop_input [type symop]):

               Return: List of Float

Get the symmetry measure of a list of Structure type objects.

example
+++++++

::

   $ import montemodes.functions.reading as io_monte
   $ import montemodes.functions.symop as symop

   $ structure = io_monte.reading_from_xyz_file('ch4.xyz')

   $ input_symop = symop.Symop(symmetry='c 3',
                               label=False,
                               connect=False,
                               central_atom=0,
                               custom_atom_list=[1,2,3,4])

   $ measure = get_symmetry(structure, input_symop)
   $ print ('The C3 symmetry measure of CH4 is {}'.format(measure))


