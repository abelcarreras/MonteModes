import pickle

import numpy as np

import montemodes.classes.structure as structure


def reading_from_txyz_file(file_name):

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
    # print(np.array(coordinates,dtype=float))

    tinker_file.close()

    return structure.Structure(coordinates=np.array(coordinates, dtype=float),
                               atom_types=np.array(atom_types, dtype=int)[None].T,
                               atomic_elements=np.array(atomic_elements, dtype=str)[None].T,
                               atomic_numbers=np.array(atomic_numbers, dtype=int)[None].T,
                               connectivity=np.array(connectivity),
                               file_name=tinker_file.name)



def reading_from_xyz_file(file_name):

    xyz_file = open(file_name, 'r')

    coordinates = []
    atomic_elements = []

    number_of_atoms = int(xyz_file.readline().split()[0])
    xyz_file.readline()
    # print(number_of_atoms)
    for i in range(number_of_atoms):
        line = xyz_file.readline().split()
        coordinates.append(line[1:4])
        atomic_elements.append(line[0])
    coordinates = np.array(coordinates,dtype=float)
    xyz_file.close()

    return structure.Structure(coordinates=np.array(coordinates, dtype=float),
                                   atomic_elements=np.array(atomic_elements, dtype=str)[None].T,
                                   file_name=xyz_file.name)




def reading_from_gzmat_file(file_name):

    gzmat_file = open(file_name, 'r')

    z_mat = []
    internal = []
    int_label = []
    weights = []
    atomic_elements = []
    connectivity = []

    lines = gzmat_file.readlines()
    number_of_atoms = 0
    for number_of_atoms, line in enumerate(lines[5:]):

        if not line.find('Variables:'): break

        atomic_elements.append(line.split()[0])

        if len(line.split()) == 1:
            z_mat.append([])

        if len(line.split()) == 3:
            z_mat.append([line.split()[1:3]])

        if len(line.split()) == 5:
            z_mat.append([line.split()[1:5]])

        if len(line.split()) > 6:
            z_mat.append([line.split()[1:7]])


    for line in lines[number_of_atoms+6:]:
        try:
            int_label.append(line.replace('=',' ').split()[0])
            internal.append(line.replace('=',' ').split()[1])
        except IndexError:
            break
        try:
            weights.append(line.replace('=',' ').split()[2])
        except:
            weights.append(0)

    gzmat_file.close()

    return structure.Structure(internal=np.array(internal, dtype=float)[None].T,
                               int_label=np.array(int_label)[None].T,
                               z_matrix=np.array(z_mat),
                               atomic_elements=np.array(atomic_elements, dtype=str)[None].T,
                               connectivity=np.array(connectivity),
                               file_name=gzmat_file.name,
                               int_weights=np.array(weights, dtype=float))




def write_molecule_to_xyz(molecule, xyz_file):
    xyz_file.write('{0}\n\n'.format(molecule.get_number_of_atoms()))
    for i in range(molecule.get_number_of_atoms()):
        xyz_file.write(molecule.get_atomic_elements()[i][0] +
                       "\t{0:10.6f} {1:10.6f} {2:10.6f}\n".format(*molecule.get_coordinates()[i]))

    return xyz_file

def write_molecule_to_int(molecule, int_file):
    number_of_internal = len(molecule.get_int_label())
    int_file.write(str(number_of_internal) + '\n\n')
    for i in range(number_of_internal):
        int_file.write(molecule.get_int_label()[i][0] +
                       "\t{0:10.6f}\n".format(molecule.get_internal()[i][0]))

    return int_file


def write_result_trajectory(trajectory, file_name, type='xyz'):
    trajectory_file = open(file_name, 'w')
    for i in range(1, len(trajectory)):
        if type == 'xyz':
            write_molecule_to_xyz(trajectory[i], trajectory_file)
        if type == 'int':
            write_molecule_to_int(trajectory[i], trajectory_file)

    trajectory_file.close()


def write_result_to_file(result, file_name):
    result_file = open(file_name, 'w')

    result_file.write('Energy(current)\tEnergy(on test)\tAcceptation\tcv\n')
    for i, j, k in zip(result.energy, result.acceptation_ratio_vector, result.cv):
        result_file.write("{0:10.4f}\t{1:5.4f}\t{1:5.4e} \n".format(i, j, k))

    result_file.close()

    return 0

def write_list_to_file(list, file_name):
    list_file = open(file_name, 'w')
    for i, value in enumerate(list):
        list_file.write("{0} {1}\n".format(i,value))

    list_file.close()


def save_to_dump(conditions, result,filename='continue.obj'):
    dump_file = open(filename, 'w')
    pickle.dump(conditions, dump_file)
    pickle.dump(result, dump_file)
    dump_file.close()


def load_from_dump(filename='continue.obj'):
    dump_file = open(filename, 'r')
    conditions = pickle.load(dump_file)
    results = pickle.load(dump_file)
    dump_file.close()

    return conditions, results


def search_value (val, lines):
    try:
        float(val)
        return float(val)
    except ValueError:
        print('searching', val)

        for line in lines:
            if val in line:
                if '=' in line:
                    return float(line.replace('=', ' ').split()[1])

