
Distortion index
----------------

Functions
+++++++++

The calculation of the distortion index as defined in the article:
*Baur WH. Acta Crystallogr Sect B Struct Crystallogr Cryst Chem. 1974;30(5):1195–215*.
is implemented in the functions ::

    import montecarlo.analysis.distorsion as distorsion
    distorsion.get_distortion_indices_angles(structure [Structure], 'A', 'B', 'C')
        Return distortion_index [Float]

    distorsion.get_distortion_indices_distances(structure [Structure] , 'A', 'B')
        Return distortion_index [Float]

where structure is a Structure type object and 'A', 'B', and 'C' are the chemical symbol of the elements to analyze.

These functions can be called from a list of Structure type objects to return a dictionary with statistic data ::

    dist_OPO = distorsion.get_distortion_statistic_analysis(structures [List of Structure],
                                                            distorsion.get_distortion_indices_angles [Distorsion function],
                                                            ['A', 'B', 'C'],
                                                            show_plots=False)
            return {'average': average [Float],
                    'deviation': deviation [Float]}

    dist_OP = distorsion.get_distortion_statistic_analysis(structures [List of Structure],
                                                           distorsion.get_distortion_indices_distances [Distorsion function],
                                                           ['A', 'B'],
                                                           show_plots=False)
            return {'average': average [Float],
                    'deviation': deviation [Float]}


Example
+++++++
::

    import montemodes.functions.reading as io_monte
    molecule1 = io_monte.reading_from_xyz_file('PO4_1.xyz')
    molecule2 = io_monte.reading_from_xyz_file('PO4_2.xyz')
    molecule3 = io_monte.reading_from_xyz_file('PO4_3.xyz')

    import montemodes.analysis.distortion as distortion

    di_OPO = distorsion.get_distortion_indices_angles(molecule1, 'P', 'O', 'P')
    di_OP = distorsion.get_distortion_indices_distances(molecule2, 'P', 'O')

    print 'results: {} {}'.format(di_OPO, di_OP)

    ####
    structures = [molecule1, molecule2, molecule3]
    stat_OPO = distorsion.get_distortion_statistic_analysis(structures,
                                                            distorsion.get_distortion_indices_angles,
                                                            ['O', 'P', 'O'],
                                                            show_plots=False)

    stat_OP = distorsion.get_distortion_statistic_analysis(structures,
                                                           distorsion.get_distortion_indices_distances,
                                                           ['O', 'P'],
                                                           show_plots=False)

    print 'averages: {} {} and deviations: {} {}'.format(stat_OP['average'], stat_OPO['average'],
                                                         stat_OP['deviation'], stat_OPO['deviation'])

Symmetry classification
-----------------------

Classify the symmetry of a list of structures is symmetry categories defined by the user ::

    import montecarlo.analysis.symmetry_analysis
    get_symmetry_analysis(structures [List of Structure Objects],
                                       symmetry_to_analyze=None [List of Strings],
                                       shape_to_analyze=1 [Integer],
                                       central_atom=0 [Integer],
                                       symmetry_threshold=0.1 [Float],
                                       cutoff_shape=3.0 [Float],
                                       show_plots=True [Boolean])

        return {symmetry_label : percentage} [Dictionary]


- structures: List of Structure type objects to be analyzed
- symmetry_to_analyze : List of symmetry operations to classify the structures into.
- shape_to_analyze: Ideal shape of the structures
- cutoff_shape: Maximum value of shape measurement (defined in shape_to_analyze) to be accepted.
Structures with a higher value will be discarded.
- symmetry_threshold: Maximum value of a symmetry measurement of a structure to consider that the
structure has the measured symmetry.
- show_plots: If True, graphical data is shown. This includes histrograms showing the distribution
 of symmetry and shape measurements.

Exemple
+++++++
::

    import montemodes.functions.reading as io_monte
    import montecarlo.analysis.symmetry_analysis

    molecule1 = io_monte.reading_from_xyz_file('PO4_1.xyz')
    molecule2 = io_monte.reading_from_xyz_file('PO4_2.xyz')
    molecule3 = io_monte.reading_from_xyz_file('PO4_3.xyz')

    structures = [molecule1, molecule2, molecule3]

    percentage_dict = get_symmetry_analysis(structures [List of Structure Objects],
                                            symmetry_to_analyze=['c 2', 'c 3', 's 4', 'r'],
                                            shape_to_analyze=2,
                                            central_atom=5,
                                            symmetry_threshold=0.15,
                                            cutoff_shape=5.0,
                                            show_plots=False)

    for key in percentage_dict:
        print '{} : {} '.format(key, percentage_dict[key])

