import Functions.reading as io_monte
import Functions.calculate as calculate
import Functions.montecarlo as monte
import classes.results as res
import matplotlib.pyplot as plt


#Define initial conditions
molecule = io_monte.reading_from_file('Data/ethane.txyz')
conditions = res.Conditions(temperature=100,
                            number_of_cycles=300,
                            initial_expansion_factor=30,
                            number_of_modes_to_use=10,
                            acceptation_regulator=0.1,
                            number_of_values_for_average=50,
)

simulation = res.MonteCarlo(molecule)

#continue routine
if False:
    conditions, simulation = io_monte.load_from_dump()
    conditions.number_of_cycles = 300
    conditions.acceptation_regulator = 0.1
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