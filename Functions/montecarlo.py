__author__ = 'abel'
import classes.results as res
import Functions.calculate as calculate
import math
import random
import copy
import numpy as np


def weighted_choice(weights):
    total = sum(weights)
    threshold = random.uniform(0, total)
    for k, weight in enumerate(weights):
        total -= weight
        if total < threshold:
            return k

def alteration_with_modes(molecule, vibration, conditions):
    altered_coordinates = molecule.get_coordinates()
    random_number = random.uniform(-1, 1)
    chosen = weighted_choice([ math.exp(-conditions.temperature_frequency_relation * vibration.frequencies[i] / conditions.temperature)
        for i in range(vibration.number_of_modes)])
    chosen = random.randrange(vibration.number_of_modes)
    if abs(vibration.frequencies[chosen]) > 0.01:
        altered_coordinates += conditions.expansion_factor \
                           * random.uniform(-1, 1) \
                           * vibration.normalized_modes[chosen] \
                           * pow(vibration.frequencies[chosen],-2)
#                               * math.exp(
#            -conditions.temperature_frequency_relation * vibration.frequencies[i] / conditions.temperature)

    altered_molecule = copy.deepcopy(molecule)

    altered_molecule.set_coordinates(altered_coordinates)

    return altered_molecule


def average_gradient(vector):
#    print(np.polyfit( np.arange(len(vector)),vector,1,full=True)[1])
    poly_values = (np.polyfit( np.arange(len(vector)),vector,2))
    poly_derivative = np.polyder(np.poly1d(poly_values))
    return -poly_derivative(len(vector))


def adjust_expansion_factor(acceptation_vector, conditions):

    last_acceptation_vector = acceptation_vector[-conditions.number_of_vales_for_average:]
#    print(last_acceptation_vector)
    if len(last_acceptation_vector) < conditions.number_of_vales_for_average:
        return conditions.expansion_factor

    current_gradient = average_gradient(last_acceptation_vector)
    A = conditions.acceptation_regulator
    target_gradient = A * 2 ** 3 * (acceptation_vector[-1] - 0.5) ** 3
    # target_derivative = -A*(acceptation_vector[-1])*2
    # print('derivative',current_derivative,target_derivative)
    final = math.exp(target_gradient - current_gradient)
    #    print'F:', acceptation_vector[-1],Final
    #    conditions.expansion_factor *= Final
#    print('Grad:',current_gradient,target_gradient,final)

    return conditions.expansion_factor * final


def calculate_MonteCarlo(simulation, conditions):

    molecule = copy.deepcopy(simulation.trajectory[-1])
    vibration = calculate.get_modes_from_tinker(molecule)

    print 'Temperature', conditions.temperature
    print('Starting at:',simulation.number_of_cycles)
    for iteration in range(simulation.number_of_cycles, simulation.number_of_cycles + conditions.number_of_cycles):
#        print(iteration)
        simulation.update_acceptation_vector(iteration)

        simulation.append_data_from_molecule(molecule)
 #       print(simulation.acceptation_ratio(iteration))

        conditions.expansion_factor = adjust_expansion_factor(simulation.acceptation_ratio_vector, conditions)

        molecule_altered = alteration_with_modes(molecule, vibration, conditions)

        print(molecule.get_energy(), molecule_altered.get_energy(), simulation.acceptation_ratio)

        if molecule.get_energy() < molecule_altered.get_energy():
            energy_ratio = math.exp((molecule.get_energy() - molecule_altered.get_energy())
                                    / (conditions.temperature * conditions.kb))

            if energy_ratio < random.random():
                continue

        molecule = molecule_altered
        simulation.add_accepted(iteration)
        vibration = calculate.get_modes_from_tinker(molecule)

    simulation.number_of_cycles += conditions.number_of_cycles
    return simulation