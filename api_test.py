import matplotlib.pyplot as plt

import montemodes.functions.reading as io_monte
import montemodes.functions.calculate as calculate
import montemodes.functions.montecarlo as monte
import montemodes.functions.methods as meth
import montemodes.classes.results as res
import montemodes.functions.symop as symop
import montemodes.functions.symgroup as symgroup


import montemodes.functions.shape as shape


gaussian_calc = meth.Gaussian(methodology='pm6',
                              internal=False,
                              multiplicity=1)

tinker_calc = meth.Tinker(parameter_set='mm3.prm')

for t in [200]:
    print ('t {}'.format(t))
    conditions = res.Conditions(temperature=t,
                                number_of_cycles=1000,
                                initial_expansion_factor=10,  # modes : 10 , cart: 0.01
                                acceptation_regulator=0.08,
                                #number_of_modes_to_use=15,
                                number_of_values_for_average=93,
                                energy_method=gaussian_calc)

    #molecule = io_monte.reading_from_xyz_file('Example/po4.xyz')
    #molecule = io_monte.reading_from_txyz_file('Example/ethane.txyz')
    #molecule = io_monte.reading_from_gzmat_file('Example/test.gzmat')
    #molecule = io_monte.reading_from_gzmat_file('Example/bifenil.gzmat')
    molecule = io_monte.reading_from_gzmat_file('Example/ethane.gzmat')

    print molecule.get_coordinates()

    molecule.charge = 0
    molecule.multiplicity = 1

    simulation = res.MonteCarlo(molecule)

    if False:
        print('Recovering...')
        conditions, simulation = io_monte.load_from_dump(filename='test.obj')
        conditions.number_of_cycles = 1000
        conditions.number_of_vales_for_average = 100

    #result = monte.calculate_MonteCarlo(simulation, conditions, alteration_type='cartesian',show_text=True)
    result = monte.calculate_MonteCarlo(simulation, conditions, alteration_type='modes')
    #result = monte.calculate_MonteCarlo(simulation, conditions, alteration_type='internal', show_text=True)

    #plt.plot(result.energy)
    #plt.show()

    #plt.plot(result.acceptation_ratio_vector)
    #plt.show()

    #plt.plot(result.cv)
    #plt.show()

    io_monte.write_result_trajectory(result.trajectory, file_name='ethane_int_{}.xyz'.format(t))

exit()

print 'symgroup analysis'
chirality = symgroup.Symgroup(symmetry='r',
                    label=True,
                    custom_atom_list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                    connect=True)

chirality_list = symgroup.get_symmetry_trajectory(result.trajectory, chirality)

plt.plot(chirality_list)
plt.show()

exit()
#shape

shape_input = shape.Shape(code=1,
                          central_atom=1)



shape_list = shape.get_shape_trajectory(result.trajectory, shape_input)
shape_list = shape_list[5:]
io_monte.write_list_to_file(shape_list,'shape.txt')



print(shape_list)
plt.plot(shape_list)
plt.show()




exit()

#Symmetry
symop_c3 = symop.Symop(symmetry='s',
                       label=False,
                       connect=False,
                       central_atom=0)

symmetry_list = symop.get_symmetry_trajectory(result.trajectory, symop_c3)
io_monte.write_list_to_file(symmetry_list,'symmetry.txt')

print(symmetry_list)
plt.plot(symmetry_list)
plt.show()

plt.plot(result.cv)
plt.show()

#Show result plot
plt.plot(result.energy)
plt.show()

plt.plot(result.acceptation_ratio_vector)
plt.show()



io_monte.write_result_to_file(result, 'test.out')
io_monte.write_result_trajectory(result.trajectory, 'out.xyz')


#Save dump to file to continue from this point
io_monte.save_to_dump(conditions,result,filename='test.obj')

exit()
#conditions, simulation = io_monte.load_from_dump(filename='continue.obj')
#io_monte.write_result_to_file(simulation, 'test.out')
#io_monte.write_result_trajectory(simulation.trajectory, 'hf_1500.int', type='int')

#exit()

conditions = res.Conditions(temperature=100,
                            number_of_cycles=5,
                            initial_expansion_factor=1,
                            energy_method=2,
                            acceptation_regulator=0.1,
                            number_of_values_for_average=50)

molecule = io_monte.reading_from_gzmat_file('test.gzmat')

simulation = res.MonteCarlo(molecule)
result = monte.calculate_MonteCarlo_internal(simulation, conditions)


io_monte.write_result_to_file(result, 'test.out')
io_monte.write_result_trajectory(result.trajectory, 'test.xyz')
io_monte.write_result_trajectory(result.trajectory, 'test.int', type='int')

exit()
#Define initial conditions
molecule = io_monte.reading_from_txyz_file('Data/ethane.txyz')
conditions = res.Conditions(temperature=10,
                            number_of_cycles=1000,
                            initial_expansion_factor=30,
                    #        number_of_modes_to_use=100,
                            acceptation_regulator=0.1,
                            number_of_values_for_average=100,
)

simulation = res.MonteCarlo(molecule)

#continue routine
if False:
    print('Recovering...')
    conditions, simulation = io_monte.load_from_dump()
    conditions.number_of_cycles = 3000
#    conditions.temperature = 10
    conditions.acceptation_regulator = 0.1
    conditions.number_of_vales_for_average = 100
#    conditions.expansion_factor = 0.003 #simulation.acceptation_ratio

#Show initial energy
energy = calculate.get_energy_from_tinker(molecule)
print 'Initial Energy:', energy


#Perform Monte Carlo simulation
result = monte.calculate_MonteCarlo(simulation, conditions)

#Show result plot
plt.plot(result.energy)
plt.show()

plt.plot(result.acceptation_ratio_vector)
plt.show()

#Save results to data files
io_monte.write_result_to_file(result, 'test.out')
io_monte.write_result_trajectory(result.trajectory, 'test.xyz')

#Save dump to file to continue from this point
io_monte.save_to_dump(conditions,result)