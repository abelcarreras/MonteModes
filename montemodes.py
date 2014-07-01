__author__ = 'abel'
import Functions.reading as io_monte
import Functions.calculate as calculate
import Functions.montecarlo as monte
import classes.results as res
import matplotlib.pyplot as plt


# Test Molecule 1
molecule2 = io_monte.reading_from_file('Data/bifenil2.txyz')
conditions2 = res.Conditions(temperature=100,
                            kb=0.0019872041,  # kcal/mol
                            number_of_cycles=1000,
                            initial_expansion_factor=0.15,
                            number_of_modes_to_use=10)

# Test Molecule 2

molecule = io_monte.reading_from_file('Data/bife_raro.txyz')
conditions = res.Conditions(temperature=200,
                            number_of_cycles=1065,
                            initial_expansion_factor=0.15,
                            number_of_modes_to_use=10)


energy = calculate.get_energy_from_tinker(molecule)
print 'Initial Energy:', energy

vibration = calculate.get_modes_from_tinker(molecule)


# print(molecule.get_coordinates())
# print(monte.alteration_with_modes(molecule,vibration).get_coordinates())
# print(molecule.get_energy())

result = monte.calculate_MonteCarlo(molecule, conditions, vibration)

plt.plot(result.energy)
plt.show()

plt.plot(result.acceptation_ratio_vector)
plt.show()

# exit()

io_monte.write_result_trajectory(result.trajectory, 'test.xyz')
io_monte.write_result_to_file(result, 'test.out')