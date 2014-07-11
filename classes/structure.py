__author__ = 'abel'
import Functions.calculate as calc


class Structure:

    def __init__(self,
                 coordinates=None,
                 atom_types=None,
                 atomic_elements=None,
                 atomic_numbers=None,
                 connectivity=None,
                 file_name=None):

        self._coordinates = coordinates
        self._atom_types = atom_types
        self._atomic_numbers = atomic_numbers
        self._connectivity = connectivity
        self._atomic_elements = atomic_elements
        self._number_of_atoms = None
        self._energy = None
        self._file_name = file_name

    def get_coordinates(self):
        return self._coordinates.copy()

    def set_coordinates(self, coordinates):
        self._coordinates = coordinates
        self._number_of_atoms = None
        self._energy = None

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    def get_atom_types(self):
        return self._atom_types

    def set_atom_types(self, atom_types):
        self._atom_types = atom_types

    def get_atomic_numbers(self):
        return self._atomic_numbers

    def set_atomic_numbers(self, atomic_numbers):
        self._atomic_numbers = atomic_numbers

    def get_atomic_elements(self):
        return self._atomic_elements

    def set_atomic_elements(self, atomic_elements):
        self._atomic_elements = atomic_elements

    def get_connectivity(self):
        return self._connectivity

    def set_connectivity(self, connectivity):
        self._connectivity = connectivity

#   Real methods

    def get_number_of_atoms(self):
        if self._number_of_atoms is None and self._coordinates is not None:
            self._number_of_atoms = self._coordinates.shape[0]

        return self._number_of_atoms

    def get_energy(self):
        if not self._energy:
            self._energy = calc.get_energy_from_tinker(self)
        return self._energy
