import numpy as np
from montemodes.classes.structure import Structure
from montemodes.analysis.symmetry_analysis import get_symmetry_analysis
import montemodes.analysis.distorsion as distorsion

import functions.shape

print functions.shape.get_info(vertices=4)

exit()


def random_alteration_coordinates_box(initial_coordinates, fix_center=None, max_displacement=0.2):
    displacement = 2 * max_displacement * (np.random.random(np.array(initial_coordinates).shape) - 0.5)
    if fix_center is not None:
        displacement[fix_center] *= 0.0

    return initial_coordinates + displacement


# Initial perfect tetrahedral structure
initial_coordinates = [[ 0.5784585,  0.7670811,  1.3587379],
                       [-1.7015514, -0.0389921, -0.0374715],
                       [ 0.5784290, -1.6512236, -0.0374715],
                       [ 0.5784585,  0.7670811, -1.4336809],
                       [ 0.0000000,  0.0000000,  0.0000000]]

atomic_elements = ['O', 'O', 'O', 'O', 'P']


total_proportions = []
for expansion_box in np.arange(0.1, 1.0, 0.1):

#if True:
    # expansion_box = 0.8
    number_of_samples = 20

    structures = []
    for i in range(number_of_samples):
        coordinates = random_alteration_coordinates_box(initial_coordinates, fix_center=4, max_displacement=expansion_box)
        structures.append(Structure(coordinates=np.array(coordinates, dtype=float),
                                    atomic_elements=np.array(atomic_elements, dtype=str)[None].T))

    dist_OPO = distorsion.get_distortion_statistic_analysis(structures,
                                                            distorsion.get_distortion_indices_angles,
                                                            ['O', 'P', 'O'],
                                                            show_plots=False)

    dist_OP = distorsion.get_distortion_statistic_analysis(structures,
                                                           distorsion.get_distortion_indices_distances,
                                                           ['O', 'P'],
                                                           show_plots=False)

    print 'expansion', expansion_box, dist_OP['average'], dist_OPO['average']

    proportion = get_symmetry_analysis(structures,
                                       symmetry_to_analyze=['c 2', 'c 3', 's 4', 'r'],
                                       shape_to_analyze=2,
                                       central_atom=5,
                                       symmetry_threshold=0.15,
                                       cutoff_shape=5.0,
                                       show_plots=False)

    total_proportions.append(proportion)

print ' '.join(total_proportions[0].keys())
for proportion in total_proportions:
    print ' '.join(np.array(proportion.values(), dtype=str))