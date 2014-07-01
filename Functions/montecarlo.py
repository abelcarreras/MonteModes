__author__ = 'abel'
import classes.results as res
import Functions.calculate as calculate
import math
import random
import copy
import numpy as np


def alteration_with_modes(molecule, vibration, conditions):
    altered_coordinates = molecule.get_coordinates()
    for i in range(vibration.number_of_modes):
        # print('freq:',vibration.frequencies[i])
        altered_coordinates += conditions.expansion_factor \
                               * random.uniform(-1, 1) \
                               * vibration.normalized_modes[i] \
                               * math.exp(
            -conditions.temperature_frequency_relation * vibration.frequencies[i] / conditions.temperature)

    altered_molecule = copy.deepcopy(molecule)

    altered_molecule.set_coordinates(altered_coordinates)

    return altered_molecule


def average_derivative(vector):
    xi = np.arange(len(vector))
    a = np.array([xi, np.ones(len(vector))])
    return -np.linalg.lstsq(a.T, vector)[0][0]


def adjust_expansion_factor(acceptation_vector, conditions):
    last_acceptation_vector = acceptation_vector[-conditions.number_of_vales_for_average:]

    if len(last_acceptation_vector) < conditions.number_of_vales_for_average:
        return conditions.expansion_factor

    current_derivative = average_derivative(last_acceptation_vector)
    A = conditions.acceptation_regulator
    target_derivative = -A * 2 ** 3 * (acceptation_vector[-1] - 0.5) ** 3
    # target_derivative = -A*(acceptation_vector[-1])*2
    # print('derivative',current_derivative,target_derivative)
    Final = math.exp(-(target_derivative - current_derivative))
    #    print'F:', acceptation_vector[-1],Final
    #    conditions.expansion_factor *= Final

    return conditions.expansion_factor * Final


def calculate_MonteCarlo(initial_molecule, conditions, vibration):
    print 'Temperature', conditions.temperature

    # accepted = 0
    result = res.MonteCarlo('Monte Carlo Simulation')
    molecule = copy.deepcopy(initial_molecule)

    for iteration in range(conditions.number_of_cycles):

        result.append_data_from_molecule(molecule)
        conditions.expansion_factor = adjust_expansion_factor(result.acceptation_ratio_vector, conditions)

        molecule_altered = alteration_with_modes(molecule, vibration, conditions)

        print(molecule.get_energy(), molecule_altered.get_energy(), result.acceptation_ratio)

        if molecule.get_energy() < molecule_altered.get_energy():
            energy_ratio = math.exp((molecule.get_energy() - molecule_altered.get_energy())
                                    / (conditions.temperature * conditions.kb))

            if energy_ratio < random.random():
                continue

        molecule = molecule_altered
        result.add_accepted(iteration)
        vibration = calculate.get_modes_from_tinker(molecule)

    return result