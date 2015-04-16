__author__ = 'abel'

import Functions.reading as io_monte
import Functions.calculate as calculate
import Functions.montecarlo as monte
import classes.results as res
import matplotlib.pyplot as plt
import math

#Define initial conditions
import copy
def alteration_following_mode(molecule, vibration, displacement_value,index):
    altered_coordinates = molecule.get_coordinates()
    for i in [index]:
#        print('freq:',vibration.frequencies[i])
        altered_coordinates += displacement_value * vibration.normalized_modes[i]
    altered_molecule = copy.deepcopy(molecule)

    altered_molecule.set_coordinates(altered_coordinates)

    return altered_molecule

molecule = io_monte.reading_from_txyz_file('Data/bife_raro.txyz')

ene = []
ene2 =[]
vibration = calculate.get_modes_from_tinker(molecule)
print('Num Modes:',vibration.number_of_modes)
for index in range(vibration.number_of_modes):
    #print('energia 1')
    initial = molecule.get_energy()
    #print(initial)

    molecule2 = alteration_following_mode(molecule,vibration,0.5,index)
    #print('energia 2')
    final = molecule2.get_energy()
    #print(final)
    molecule2 = alteration_following_mode(molecule,vibration,-0.5,index)
    final2 = molecule2.get_energy()
    #print(final2)
    print(vibration.frequencies[index])
    print((final-initial)/vibration.frequencies[index],(final2-initial)/vibration.frequencies[index])
    ene.append((final-initial)/pow(vibration.frequencies[index],2))
    ene2.append((final2-initial)/pow(vibration.frequencies[index],2))


plt.plot(ene)
plt.plot(ene2)
plt.show()