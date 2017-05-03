Structure object
================

Object structure

class   Structure(coordinates=None,
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
                 #Buscar un lloc millor
                 int_weights=None):

# Methods of


# Read initial structure from xyz file
molecule = io_monte.reading_from_xyz_file('../Example/test.xyz')

# Add additional information to molecule
molecule.charge = 0
molecule.multiplicity = 1