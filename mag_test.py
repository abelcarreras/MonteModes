import matplotlib.pyplot as plt
import numpy as np

import montemodes.functions.reading as io_monte
import montemodes.functions.montecarlo as monte
import montemodes.functions.methods as meth
import montemodes.classes.results as res
import montemodes.analysis.magnetism as magnetism

bs_singlet = meth.Gaussian(methodology='pm6',
                           internal=False,
                           multiplicity=1,
                           guess='mix',
                           alter=[[1, 2],  # if alter is defined, 'guess=alter' keyword is automatically set
                                  [3, 4]])

triplet = meth.Gaussian(methodology='pm6',
                        internal=False,
                        multiplicity=3,
                        alter=None)

conditions = res.Conditions(temperature=300,
                            number_of_cycles=100,
                            initial_expansion_factor=0.01,  # modes : 10 , cart: 0.01
                            acceptation_regulator=0.08,
                            number_of_values_for_average=93,
                            energy_method=triplet)

molecule = io_monte.reading_from_xyz_file('Example/po4.xyz')
molecule.charge = -1

simulation = res.MonteCarlo(molecule)
result = monte.calculate_MonteCarlo(simulation, conditions, alteration_type='cartesian')

j_list = magnetism.get_magnetic_coupling_trajectory(result.trajectory[10:], bs_singlet, triplet)
io_monte.write_list_to_file(j_list, 'j_coupling.txt', label='J')

print ('Average J: {}'.format(np.average(j_list[10:])))
plt.hist(j_list, density=True)
plt.xlabel('coupling constant (J)')

plt.show()