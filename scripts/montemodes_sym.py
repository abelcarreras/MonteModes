#!/usr/bin/env python

import montemodes.functions.reading as io_monte
import montemodes.functions.montecarlo as monte
import montemodes.functions.methods as method
import montemodes.classes.results as res
from montemodes.analysis.symmetry_analysis import get_symmetry_analysis


#Define energy calculation methodology
gaussian_calc = method.gaussian(methodology='pm6',
                               internal=False)

#Define MC simulation conditions
conditions = res.Conditions(temperature=50000,
                            number_of_cycles=50,
                            initial_expansion_factor=0.05,
                            acceptation_regulator=0.1,
                            number_of_values_for_average=5,
                            energy_method=gaussian_calc)

#Read initial structure from xyz file
molecule = io_monte.reading_from_xyz_file('../Example/po4.xyz')

#Add additional information to molecule
molecule.charge = -3
molecule.multiplicity = 1

#Create MD simulation object from molecule
simulation = res.MonteCarlo(molecule)

#Run Monte Carlo simulation with cartesian algorithm using simulation object & conditions
result = monte.calculate_MonteCarlo(simulation, conditions,
                                    show_text=True,
                                    alteration_type='cartesian')

#Save results to data files
io_monte.write_result_to_file(result, 'test.out')
io_monte.write_result_trajectory(result.trajectory, 'trajectory.xyz')



#Save full simulation to file (contains all data) [Can be used to restart the simulation]
io_monte.save_to_dump(conditions, result, filename='full.obj')
io_monte.load_from_dump(filename='full.obj')


# Symmetry analysis
proportion = get_symmetry_analysis(result.trajectory,
                                   symmetry_to_analyze=['c 2', 'c 3', 's 4', 'r'],
                                   shape_to_analyze=2,
                                   central_atom=5,
                                   symmetry_threshold=0.1,
                                   cutoff_shape=3.0,
                                   show_plots=True)

print 'proportions'
print proportion