import numpy as np
import itertools


def check_auto(list):
    if len(np.unique(list)) < len(list):
        return False
    return True

def get_distortion_indices_distances(molecule, type_1, type_2):

    list_type_1 = np.where(molecule.get_atomic_elements().T[0] == type_1)[0]
    list_type_2 = np.where(molecule.get_atomic_elements().T[0] == type_2)[0]

    if len(list_type_1) == 0 or len(list_type_2) == 0:
        print 'Molecule does not contain this atomic type'
        return None

    permutations = itertools.product(list_type_1, list_type_2)
    filtered_permutations = filter(lambda pair: check_auto(pair), permutations)

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

def calculate_angle(coor_1, coor_2, coor_3):
    a = (coor_2 - coor_1)
    b = (coor_3 - coor_2)

    angle = np.arccos(np.dot(a,b)/np.linalg.norm(a)/np.linalg.norm(b))
    return angle

def get_distortion_indices_angles(molecule, type_1, type_2, type_3):

    list_type_1 = np.where(molecule.get_atomic_elements().T[0] == type_1)[0]
    list_type_2 = np.where(molecule.get_atomic_elements().T[0] == type_2)[0]
    list_type_3 = np.where(molecule.get_atomic_elements().T[0] == type_3)[0]

    if len(list_type_1) == 0 or len(list_type_2) == 0 or len(list_type_3) == 0:
        print 'Molecule does not contain this atomic type'
        return None

    permutations = itertools.product(list_type_1, list_type_2, list_type_3)
    filtered_permutations = filter(lambda trip: check_auto(trip), permutations)

    if len(filtered_permutations) == 0:
        print 'Cannot find atom angles'
        return None

    coordinates = molecule.get_coordinates()

    angles = []
    for permutation in filtered_permutations:
        angle = calculate_angle(coordinates[permutation[0]], coordinates[permutation[1]], coordinates[permutation[2]])
        angles.append(angle)

    return np.average([abs(value - np.average(angles)) for value in angles])
    # return np.std(distances)


if __name__ == '__main__':

    import montemodes.functions.reading as io_monte

    # Read initial structure from xyz file
    molecule1 = io_monte.reading_from_xyz_file('../../Example/po4.xyz')

    print get_distortion_indices_angles(molecule1, 'O', 'O', 'O')
    exit()

    print get_distortion_indices_distances(molecule1, 'O', 'P')
