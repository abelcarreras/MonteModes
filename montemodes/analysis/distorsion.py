import numpy as np
import itertools


def get_distortion_indices_distances(molecule, type_1, type_2):

    list_type_1 = np.where(molecule.get_atomic_elements().T[0] == type_1)[0]
    list_type_2 = np.where(molecule.get_atomic_elements().T[0] == type_2)[0]

    if len(list_type_1) == 0 or len(list_type_2) == 0:
        print 'Molecule does not contain this atomic type'
        return None

    permutations = itertools.product(list_type_1, list_type_2)
    filtered_permutations = filter(lambda pair: pair[0] != pair[1], permutations)

    if len(filtered_permutations) == 0:
        print 'Cannot find atom pairs'
        return None

    coordinates = molecule.get_coordinates()

    distances = []
    for permutation in filtered_permutations:
        distance = np.linalg.norm(coordinates[permutation[0]] - coordinates[permutation[1]])
        distances.append(distance)

    return np.average([abs(value - np.average(distances)) for value in distances])
    # return np.std(distances)


if __name__ == '__main__':

    import montemodes.functions.reading as io_monte

    # Read initial structure from xyz file
    molecule1 = io_monte.reading_from_xyz_file('../../Example/po4.xyz')

    print get_distortion_indices_distances(molecule1, 'O', 'P')
