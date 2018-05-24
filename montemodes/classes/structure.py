__author__ = 'abel'
import tempfile
import os
import numpy as np


def int_to_xyz(molecule, no_dummy=True):

    internal = molecule.get_full_z_matrix()
    coordinates = [[0.0, 0.0, 0.0]]

    for line in internal[1:]:
        bi = int(line[0])  #bond index
        B = line[1]        #bond value
        ai = int(line[2])  #Angle index
        A = line[3]        #Angle value
        ci = int(line[4])  #Dihedral index
        C = line[5]        #Dihedral value

        bond = np.array(coordinates[ai-1]) - np.array(coordinates[bi-1])
        if np.linalg.norm(bond) == 0:
            bond = np.array([1, 0, 0])

        bond2 = np.array(coordinates[ci-1]) - np.array(coordinates[ai-1])
        if np.linalg.norm(bond2) == 0:
            bond2 = np.array([0, 1, 0])

        origin = bond/np.linalg.norm(bond)*B
        ref2 = bond
        ref3 = np.cross(bond, bond2)

        # Check case of linear structure
        if np.linalg.norm(ref3) == 0:
            ref3 = [0.0, 0.0, 0.1]

        inter = np.dot(rotation_matrix(ref3, np.deg2rad(A)), origin)
        final = np.dot(rotation_matrix(ref2, np.deg2rad(C)), inter)
        final = final + np.array(coordinates[bi-1])
        coordinates.append(final)

    coordinates = np.array(coordinates)

    if no_dummy:
      #  mask = np.argwhere(molecule.get_atomic_elements_with_dummy()[:,0]  == 'X')
        mask = np.argwhere((molecule.get_atomic_elements_with_dummy()[:,0] == 'X') |
                           (molecule.get_atomic_elements_with_dummy()[:,0] == 'x')).flatten()
        coordinates = np.delete(coordinates,mask,axis=0)

    return np.array(coordinates, dtype=float)


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    if np.dot(axis, axis) == 0.0:
        print 'Warning, reference rotation axis module is 0'
        exit()


    axis = np.asarray(axis)
    theta = np.asarray(theta)
    axis = axis/np.sqrt(np.dot(axis, axis))

    a = np.cos(theta/2)
    b, c, d = -axis*np.sin(theta/2)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])


class Structure:

    def __init__(self,
                 coordinates=None,
                 internal=None,
                 z_matrix=None,
                 int_label=None,
                 atom_types=None,
                 atomic_elements=None,
                 atomic_numbers=None,
                 connectivity=None,
                 file_name=None,
                 charge=0,
                 #multiplicity=1,

                 #Buscar un lloc millor
                 int_weights=None):

        self._coordinates = coordinates
        self._internal = internal
        self._z_matrix = z_matrix
        self._int_label = int_label
        self._atom_types = atom_types
        self._atomic_numbers = atomic_numbers
        self._connectivity = connectivity
        self._atomic_elements = atomic_elements
        self._charge = charge
        #self._multiplicity = multiplicity

        self._file_name = file_name
        self._int_weights = int_weights

        self._atomic_masses = None
        self._number_of_atoms = None
        self._number_of_internal = None
        self._energy = {}
        self._modes = None

        self._full_z_matrix = None

    def get_coordinates(self):
        if self._coordinates is None:
            self._coordinates = int_to_xyz(self)
        return self._coordinates.copy()

    def set_coordinates(self, coordinates):
        self._coordinates = coordinates
        self._number_of_atoms = None
        self._energy = {}

    def get_internal(self):
        if self._internal is None:
            print('No internal coordinates available\n Load internal file')
            exit()
        return self._internal.copy()

    def set_internal(self, internal):
        self._internal = internal
        self._energy = None
        self._coordinates = int_to_xyz(self)
        self._full_z_matrix = None

    def get_full_z_matrix(self):
        if self._full_z_matrix is None:
            num_z_atoms = self.get_z_matrix().shape[0]
            self._full_z_matrix = np.zeros((num_z_atoms,6))

            for row, i in enumerate(self.get_z_matrix()[1:]):
                    for col, k in enumerate(i[0]):
                        try:
                            self._full_z_matrix[row+1, col] = float(k)
                        except ValueError:
                            self._full_z_matrix[row+1, col] = self.get_int_dict()[k]


        return self._full_z_matrix

    def get_z_matrix(self):
        if self._z_matrix is None:
            print('No Z-matrix available\n Load zmatrix file')
            exit()
        return self._z_matrix

    def set_z_matrix(self, z_matrix):
        self._z_matrix = z_matrix

    def get_int_label(self):
        return self._int_label

    def set_int_label(self, int_label):
        self._int_label = int_label

    def get_int_dict(self):
        self._internal_dict = {}
        for i, label in enumerate(self.get_int_label()[:,0]):
            self._internal_dict.update({label:self.get_internal()[i, 0]})
        return self._internal_dict

    def get_int_weights(self):
        return self._int_weights

    def set_int_weights(self, int_weights):
        self._int_weights = int_weights

    def get_atomic_elements_with_dummy(self):
       # print([i for i in self._atomic_elements if i != "X"])
       return self._atomic_elements

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    @property
    def charge(self):
        return self._charge

    @charge.setter
    def charge(self, charge):
        self._charge = charge

    #@property
    #def multiplicity(self):
    #    return self._multiplicity

    #@multiplicity.setter
    #def multiplicity(self, multiplicity):
    #    self._multiplicity = multiplicity

    def get_atom_types(self):
        if self._atom_types is None:
            print('No atom types available')
            exit()
        return self._atom_types

    def set_atom_types(self, atom_types):
        self._atom_types = atom_types

    def get_atomic_numbers(self):
        if self._atomic_numbers is None:
            self._atomic_numbers = np.array(range(1, self.get_number_of_atoms()+1))[None].T
        return self._atomic_numbers

    def set_atomic_numbers(self, atomic_numbers):
        self._atomic_numbers = atomic_numbers

    def get_atomic_elements(self):
        if self._atomic_elements is None:
            self._atomic_elements = np.array(atom_data)[[self.get_atomic_numbers()]][:,1:2]
        return np.array([[i[0].upper()] for i in self._atomic_elements if i != "X"], dtype=str)

    def set_atomic_elements(self, atomic_elements):
        self._atomic_elements = atomic_elements

    def get_connectivity(self):
        if self._connectivity is None:
            print('No atom connectivity available')
            exit()

        return self._connectivity

    def set_connectivity(self, connectivity):
        self._connectivity = connectivity

#   Real methods

    def get_number_of_atoms(self):
        if self._number_of_atoms is None:
            self._number_of_atoms = self.get_coordinates().shape[0]

        return self._number_of_atoms

    def get_number_of_internal(self):
        if self._number_of_internal is None:
            self._number_of_internal = self.get_internal().shape[0]

        return self._number_of_internal

    def get_energy(self, method=None):
        if method is None:
            if len(self._energy) == 1:
                return self._energy.values()[0]
            raise Exception('No method defined')
        elif '{}'.format(hash(method)) not in self._energy:
            self._energy['{}'.format(hash(method))] = method.single_point(self)
        return self._energy['{}'.format(hash(method))]

    def get_modes(self, method=None):
        if self._modes is None:
            if method is None:
                raise Exception('No method defined')
            self._modes, energy = method.vibrations(self)
            self._energy['{}'.format(method.multiplicity)] = energy
        return self._modes


    def get_atomic_masses(self):
        if self._atomic_masses is None:

            try:
                masses_string = np.array(atom_data)[:,3:4][[np.where(np.array(atom_data)==element)[0][0] for element in self.get_atomic_elements()]]
                self._atomic_masses = np.array(masses_string, dtype=float)
            except TypeError:
                print('Error reading element labels')
                exit()
        return  self._atomic_masses

atom_data = [
    [  0, "X", "X", 0], # 0
    [  1, "H", "Hydrogen", 1.00794], # 1
    [  2, "He", "Helium", 4.002602], # 2
    [  3, "Li", "Lithium", 6.941], # 3
    [  4, "Be", "Beryllium", 9.012182], # 4
    [  5, "B", "Boron", 10.811], # 5
    [  6, "C", "Carbon", 12.0107], # 6
    [  7, "N", "Nitrogen", 14.0067], # 7
    [  8, "O", "Oxygen", 15.9994], # 8
    [  9, "F", "Fluorine", 18.9984032], # 9
    [ 10, "Ne", "Neon", 20.1797], # 10
    [ 11, "Na", "Sodium", 22.98976928], # 11
    [ 12, "Mg", "Magnesium", 24.3050], # 12
    [ 13, "Al", "Aluminium", 26.9815386], # 13
    [ 14, "Si", "Silicon", 28.0855], # 14
    [ 15, "P", "Phosphorus", 30.973762], # 15
    [ 16, "S", "Sulfur", 32.065], # 16
    [ 17, "Cl", "Chlorine", 35.453], # 17
    [ 18, "Ar", "Argon", 39.948], # 18
    [ 19, "K", "Potassium", 39.0983], # 19
    [ 20, "Ca", "Calcium", 40.078], # 20
    [ 21, "Sc", "Scandium", 44.955912], # 21
    [ 22, "Ti", "Titanium", 47.867], # 22
    [ 23, "V", "Vanadium", 50.9415], # 23
    [ 24, "Cr", "Chromium", 51.9961], # 24
    [ 25, "Mn", "Manganese", 54.938045], # 25
    [ 26, "Fe", "Iron", 55.845], # 26
    [ 27, "Co", "Cobalt", 58.933195], # 27
    [ 28, "Ni", "Nickel", 58.6934], # 28
    [ 29, "Cu", "Copper", 63.546], # 29
    [ 30, "Zn", "Zinc", 65.38], # 30
    [ 31, "Ga", "Gallium", 69.723], # 31
    [ 32, "Ge", "Germanium", 72.64], # 32
    [ 33, "As", "Arsenic", 74.92160], # 33
    [ 34, "Se", "Selenium", 78.96], # 34
    [ 35, "Br", "Bromine", 79.904], # 35
    [ 36, "Kr", "Krypton", 83.798], # 36
    [ 37, "Rb", "Rubidium", 85.4678], # 37
    [ 38, "Sr", "Strontium", 87.62], # 38
    [ 39, "Y", "Yttrium", 88.90585], # 39
    [ 40, "Zr", "Zirconium", 91.224], # 40
    [ 41, "Nb", "Niobium", 92.90638], # 41
    [ 42, "Mo", "Molybdenum", 95.96], # 42
    [ 43, "Tc", "Technetium", 0], # 43
    [ 44, "Ru", "Ruthenium", 101.07], # 44
    [ 45, "Rh", "Rhodium", 102.90550], # 45
    [ 46, "Pd", "Palladium", 106.42], # 46
    [ 47, "Ag", "Silver", 107.8682], # 47
    [ 48, "Cd", "Cadmium", 112.411], # 48
    [ 49, "In", "Indium", 114.818], # 49
    [ 50, "Sn", "Tin", 118.710], # 50
    [ 51, "Sb", "Antimony", 121.760], # 51
    [ 52, "Te", "Tellurium", 127.60], # 52
    [ 53, "I", "Iodine", 126.90447], # 53
    [ 54, "Xe", "Xenon", 131.293], # 54
    [ 55, "Cs", "Caesium", 132.9054519], # 55
    [ 56, "Ba", "Barium", 137.327], # 56
    [ 57, "La", "Lanthanum", 138.90547], # 57
    [ 58, "Ce", "Cerium", 140.116], # 58
    [ 59, "Pr", "Praseodymium", 140.90765], # 59
    [ 60, "Nd", "Neodymium", 144.242], # 60
    [ 61, "Pm", "Promethium", 0], # 61
    [ 62, "Sm", "Samarium", 150.36], # 62
    [ 63, "Eu", "Europium", 151.964], # 63
    [ 64, "Gd", "Gadolinium", 157.25], # 64
    [ 65, "Tb", "Terbium", 158.92535], # 65
    [ 66, "Dy", "Dysprosium", 162.500], # 66
    [ 67, "Ho", "Holmium", 164.93032], # 67
    [ 68, "Er", "Erbium", 167.259], # 68
    [ 69, "Tm", "Thulium", 168.93421], # 69
    [ 70, "Yb", "Ytterbium", 173.054], # 70
    [ 71, "Lu", "Lutetium", 174.9668], # 71
    [ 72, "Hf", "Hafnium", 178.49], # 72
    [ 73, "Ta", "Tantalum", 180.94788], # 73
    [ 74, "W", "Tungsten", 183.84], # 74
    [ 75, "Re", "Rhenium", 186.207], # 75
    [ 76, "Os", "Osmium", 190.23], # 76
    [ 77, "Ir", "Iridium", 192.217], # 77
    [ 78, "Pt", "Platinum", 195.084], # 78
    [ 79, "Au", "Gold", 196.966569], # 79
    [ 80, "Hg", "Mercury", 200.59], # 80
    [ 81, "Tl", "Thallium", 204.3833], # 81
    [ 82, "Pb", "Lead", 207.2], # 82
    [ 83, "Bi", "Bismuth", 208.98040], # 83
    [ 84, "Po", "Polonium", 0], # 84
    [ 85, "At", "Astatine", 0], # 85
    [ 86, "Rn", "Radon", 0], # 86
    [ 87, "Fr", "Francium", 0], # 87
    [ 88, "Ra", "Radium", 0], # 88
    [ 89, "Ac", "Actinium", 0], # 89
    [ 90, "Th", "Thorium", 232.03806], # 90
    [ 91, "Pa", "Protactinium", 231.03588], # 91
    [ 92, "U", "Uranium", 238.02891], # 92
    [ 93, "Np", "Neptunium", 0], # 93
    [ 94, "Pu", "Plutonium", 0], # 94
    [ 95, "Am", "Americium", 0], # 95
    [ 96, "Cm", "Curium", 0], # 96
    [ 97, "Bk", "Berkelium", 0], # 97
    [ 98, "Cf", "Californium", 0], # 98
    [ 99, "Es", "Einsteinium", 0], # 99
    [100, "Fm", "Fermium", 0], # 100
    [101, "Md", "Mendelevium", 0], # 101
    [102, "No", "Nobelium", 0], # 102
    [103, "Lr", "Lawrencium", 0], # 103
    [104, "Rf", "Rutherfordium", 0], # 104
    [105, "Db", "Dubnium", 0], # 105
    [106, "Sg", "Seaborgium", 0], # 106
    [107, "Bh", "Bohrium", 0], # 107
    [108, "Hs", "Hassium", 0], # 108
    [109, "Mt", "Meitnerium", 0], # 109
    [110, "Ds", "Darmstadtium", 0], # 110
    [111, "Rg", "Roentgenium", 0], # 111
    [112, "Cn", "Copernicium", 0], # 112
    [113, "Uut", "Ununtrium", 0], # 113
    [114, "Uuq", "Ununquadium", 0], # 114
    [115, "Uup", "Ununpentium", 0], # 115
    [116, "Uuh", "Ununhexium", 0], # 116
    [117, "Uus", "Ununseptium", 0], # 117
    [118, "Uuo", "Ununoctium", 0], # 118
    ]

if __name__ == '__main__':
    import montemodes.functions.methods as meth
    import montemodes.functions.reading as io_monte

    tinker_mm3 = meth.Tinker(parameter_set='mm3')

    gaussian_pm3 = meth.Gaussian()
    molecule = io_monte.reading_from_xyz_file('../test.xyz')

    print(gaussian_pm3.function(molecule))

    # print(molecule.get_full_z_matrix())
    print(len(int_to_xyz(molecule)))