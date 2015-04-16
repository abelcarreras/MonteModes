import Functions.reading as io_monte
import Functions.calculate as calculate
import Functions.montecarlo as monte
import classes.results as res
import matplotlib.pyplot as plt
import Functions.methods as meth


gaussian_pm3 = meth.gaussian(methodology='pm6',
                             internal=True,)

conditions = res.Conditions(temperature=500,
                            number_of_cycles=50,
                            initial_expansion_factor=0.05,
                            acceptation_regulator=0.1,
                            number_of_values_for_average=50,
                            energy_method=gaussian_pm3)

#molecule = io_monte.reading_from_xyz_file('test.xyz')
#molecule = io_monte.reading_from_txyz_file('Data/ethane.txyz')
molecule = io_monte.reading_from_gzmat_file('test.gzmat')


simulation = res.MonteCarlo(molecule)
result = monte.calculate_MonteCarlo_internal(simulation, conditions)


#result = monte.calculate_MonteCarlo_cartesian(simulation, conditions)

#Show result plot
plt.plot(result.energy)
plt.show()

plt.plot(result.acceptation_ratio_vector)
plt.show()


io_monte.write_result_to_file(result, 'test.out')
io_monte.write_result_trajectory(result.trajectory, 'out.xyz')



exit()
#conditions, simulation = io_monte.load_from_dump(filename='continue.obj')
#io_monte.write_result_to_file(simulation, 'test.out')
#io_monte.write_result_trajectory(simulation.trajectory, 'hf_1500.int', type='int')

#exit()

conditions = res.Conditions(temperature=500,
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
result = monte.calculate_MonteCarlo_mode(simulation, conditions)

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