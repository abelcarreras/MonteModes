Structure object
================


$ Structure(coordinates=None,
                 internal=None,
                 z_matrix=None,
                 int_label=None,
                 atom_types=None,
                 atomic_elements=None,
                 atomic_numbers=None,
                 connectivity=None,
                 file_name=None,
                 charge=0,
                 multiplicity=1,
                 int_weights=None):


Methods
+++++++

    def get_coordinates():
        return self._coordinates.copy()

    def set_coordinates(self, coordinates):
        self._coordinates = coordinates
        self._number_of_atoms = None
        self._energy = None

    def get_internal():
        return self._internal.copy()

    def set_internal(internal):
        self._internal = internal

    def get_full_z_matrix():
        return self._full_z_matrix

    def get_z_matrix():
        return self._z_matrix

    def set_z_matrix(z_matrix):
        self._z_matrix = z_matrix

    def get_int_label():
        return self._int_label

    def set_int_label(int_label):
        self._int_label = int_label

    def get_int_dict():
        self._internal_dict = {}
        for i, label in enumerate(self.get_int_label()[:,0]):
            self._internal_dict.update({label:self.get_internal()[i, 0]})
        return self._internal_dict

    def get_int_weights():
        return self._int_weights

    def set_int_weights(int_weights):
        self._int_weights = int_weights

    def get_atomic_elements_with_dummy():
       return self._atomic_elements

    def get_atom_types():
        return self._atom_types

    def set_atom_types(atom_types):
        self._atom_types = atom_types

    def get_atomic_numbers():
        return self._atomic_numbers

    def set_atomic_numbers(atomic_numbers):

    def get_atomic_elements(self):
        return np.array([i for i in self._atomic_elements if i != "X"], dtype=str)

    def set_atomic_elements(atomic_elements):

    def get_connectivity():
        return self._connectivity

    def set_connectivity(connectivity):

    def get_number_of_atoms():
        return self._number_of_atoms

    def get_number_of_internal():
        return self._number_of_internal

    def get_energy(method=None):
        return self._energy

    def get_modes(method=None):
        return self._modes

    def get_atomic_masses(self):
        return  self._atomic_masses

Properties
++++++++++

    @property
    def charge(self):
        return self._charge

    @property
    def multiplicity(self):
        return self._multiplicity


example
-------

::

    initial_coordinates = [[ 0.5784585,  0.7670811,  1.3587379],
                           [-1.7015514, -0.0389921, -0.0374715],
                           [ 0.5784290, -1.6512236, -0.0374715],
                           [ 0.5784585,  0.7670811, -1.4336809],
                           [ 0.0000000,  0.0000000,  0.0000000]]
    initial_coordinates = np.array(initial_coordinates)

    atomic_elements = ['O', 'O', 'O', 'O', 'P']
    atomic_elements = np.array(atomic_elements)[None].T

    molecule = Structure(coordinates=initial_coordinates,
                           atomic_elements=atomic_elements)

    molecule.charge = 0
    molecule.multiplicity = 1

