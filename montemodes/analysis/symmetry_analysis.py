import numpy as np
import montemodes.functions.shape as shape
import montemodes.functions.symgroup as symgroup


def get_symmetry_analysis(structures,
                          symmetry_to_analyze='r',
                          shape_to_analyze=2,
                          central_atom=None,
                          symmetry_threshold=0.1,
                          cutoff_shape=3.0,
                          show_plots=True):

    # Shape analysis (tetrahedron)
    shape_type = shape.Shape(code=shape_to_analyze,
                             central_atom=central_atom)

    # Symmetry analysis (symgroup)
    symgroup_type_list = [symgroup.Symgroup(symmetry=symmetry_type,
                                            central_atom=central_atom)
                          for symmetry_type in symmetry_to_analyze]

    list_shape = []

    proportion = np.array([0] * (len(symgroup_type_list) + 1))

    list_symmetry = [[] for _ in range(len(symgroup_type_list))]

    not_accepted = 0
    for mod_structure in structures:

        # Shape measures
        measure_shape = shape.get_shape(molecule=mod_structure,
                                        input_data=shape_type)

        list_shape.append(measure_shape)

        # Symmetry measures
        for i, symgroup_type in enumerate(symgroup_type_list):
            measure_symmetry = symgroup.get_symmetry(molecule=mod_structure,
                                                     input_data=symgroup_type)
            list_symmetry[i].append(measure_symmetry)

        # Apply shape cutoff
        if measure_shape > cutoff_shape:
            not_accepted +=1
            continue

        # Categorize
        other = True
        for i, measure_symmetry in enumerate(np.array(list_symmetry)[:, -1]):
            if measure_symmetry < symmetry_threshold:
                proportion[i] += 1.0
                other = False

        if other:
            proportion[len(symgroup_type_list)] += 1.0

    try:
        proportion = proportion / float(len(structures) - not_accepted) * 100
    except RuntimeWarning:
        proportion *= 0

    # Plot data
    if show_plots:
        import matplotlib.pyplot as pl

        pl.figure(1)
        pl.title('shape')
        pl.xlabel('measure')
        pl.ylabel('population')
        pl.xlim([0, cutoff_shape])
        pl.hist(list_shape, histtype='step', normed=True)

        pl.figure(2)
        pl.title('symmetry')
        pl.xlabel('measure')
        pl.ylabel('population')

        for i, symmetry_type in enumerate(symgroup_type_list):
            pl.hist(list_symmetry[i], histtype='step', normed=True, label=symmetry_type.symmetry)
        pl.legend()

        pl.figure(3)
        pl.title('proportion')
        ind = range(len(proportion))
        pl.bar(ind, proportion)
        pl.ylim([0, 100])
        pl.xticks(ind, [symgroup_type.symmetry for symgroup_type in symgroup_type_list] + ['None'])

        pl.show()

    result = {symgroup_type.symmetry : proportion[i] for i, symgroup_type in enumerate(symgroup_type_list) }
    result['None'] = proportion[-1]
    return result