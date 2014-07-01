__author__ = 'abel'
import classes.structure as structure
import numpy as np


def reading_from_file(file_name):
    tinker_file = open(file_name, 'r')

    coordinates = []
    atomic_numbers = []
    atomic_elements = []
    atom_types = []
    connectivity = []

    number_of_atoms = int(tinker_file.readline().split()[0])
    # print(number_of_atoms)
    for i in range(number_of_atoms):
        line = tinker_file.readline().split()
        coordinates.append(line[2:5])
        atomic_numbers.append(int(line[0]))
        atomic_elements.append(line[1])
        atom_types.append(line[5])
        connectivity.append([int(f) for f in line[6:]])
    #    print(np.array(coordinates,dtype=float))

    return structure.Structure(coordinates=np.array(coordinates, dtype=float),
                               atom_types=np.array(atom_types, dtype=int)[None].T,
                               atomic_elements=np.array(atomic_elements, dtype=str)[None].T,
                               atomic_numbers=np.array(atomic_numbers, dtype=int)[None].T,
                               connectivity=np.array(connectivity),
                               file_name=tinker_file.name)


def write_molecule_to_xyz(molecule, xyz_file):
    xyz_file.write(str(molecule.get_number_of_atoms()) + '\n\n')

    for i in range(molecule.get_number_of_atoms()):
        line = str([list(molecule.get_atomic_elements()[i]) +
                    list(molecule.get_coordinates()[i])]) \
            .strip('[]').replace(',', '').replace("'", "")

        xyz_file.write(line + '\n')

    return xyz_file


def write_result_trajectory(trajectory, file_name):
    xyz_file = open(file_name, 'w')
    for i in range(len(trajectory)):
        write_molecule_to_xyz(trajectory[i], xyz_file)

    xyz_file.close()

def write_result_to_file(result, file_name):
    result_file = open(file_name, 'w')

    for i,j in zip(result.energy,result.acceptation_ratio_vector):
        result_file.write("{0:10.4f}\t{1:5.4f}\n".format(i,j))

    result_file.close()

    return 0