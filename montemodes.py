import Functions.reading as io_monte
import Functions.calculate as calculate
import Functions.montecarlo as monte
import classes.results as res
import matplotlib.pyplot as plt


molecule = io_monte.reading_from_file('Data/bife_raro.txyz')
conditions = res.Conditions(temperature=200,
                            number_of_cycles=10,
                            initial_expansion_factor=0.15,
                            number_of_modes_to_use=10)


#continue rutine
if True:
    conditions,last_result = io_monte.load_from_dump()
    conditions._number_of_cycles = 20
    molecule = last_result.trajectory[-1]

#Show initial energy
energy = calculate.get_energy_from_tinker(molecule)
print 'Initial Energy:', energy

#Calculate initial vibrational analysis
vibration = calculate.get_modes_from_tinker(molecule)

#Perform Monte Carlo simulation
result = monte.calculate_MonteCarlo(molecule, conditions, vibration, result=last_result)

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