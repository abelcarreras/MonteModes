from montemodes import classes as res

__author__ = 'abel'
import montemodes.functions.calculate as calculate
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


########### ALTERATION FUNCTIONS ########

def alteration_with_modes(molecule, vibration, conditions):
    altered_coordinates = molecule.get_coordinates()
    random_number = random.uniform(0, 1)
    chosen = random.randrange(vibration.number_of_modes)

    if abs(vibration.frequencies[chosen]) > 0.01:
        altered_coordinates += ( np.sqrt(conditions.expansion_factor*random_number*molecule.get_atomic_masses())
                             * pow(vibration.frequencies[chosen],-1)
                             * random.choice([1,-1])
                             * vibration.normalized_modes[chosen])
#                               * math.exp(
#            -conditions.temperature_frequency_relation * vibration.frequencies[i] / conditions.temperature)

    altered_molecule = copy.deepcopy(molecule)

    altered_molecule.set_coordinates(altered_coordinates)

    return altered_molecule

def alteration_internal_with_weights(molecule, conditions):
    altered_coordinates = molecule.get_internal()
    weights = molecule.get_int_weights()
    altered_coordinates += np.prod([np.random.random((molecule.get_internal().shape[0],))-0.5,
                                  weights],axis=0)[None].T * conditions.expansion_factor


    altered_molecule = copy.deepcopy(molecule)
    altered_molecule.set_internal(altered_coordinates)
    return altered_molecule

def alteration_cartesian(molecule, conditions):
    altered_coordinates = molecule.get_coordinates()
   # print(np.prod([np.random.random(molecule.get_coordinates().shape)-0.5]))
  #  exit()
    altered_coordinates += (np.random.random(molecule.get_coordinates().shape)-0.5) * conditions.expansion_factor

 #   print(altered_coordinates)
    altered_molecule = copy.deepcopy(molecule)
    altered_molecule.set_coordinates(altered_coordinates)
    return altered_molecule


############ REGULATION FUNCTIONS #########

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


#####MONTECARLO ALGORITHMS######

def calculate_MonteCarlo_mode(simulation, conditions, show_text=True):

    molecule = copy.deepcopy(simulation.trajectory[-1])
    vibration = calculate.get_modes_from_tinker(molecule,conditions)

    print 'Temperature', conditions.temperature
    print('Starting at:',simulation.number_of_cycles)
    for iteration in range(simulation.number_of_cycles, simulation.number_of_cycles + conditions.number_of_cycles):

        simulation.update_acceptation_vector(iteration,conditions)
        simulation.append_data_from_molecule(molecule)
        conditions.expansion_factor = adjust_expansion_factor(simulation.acceptation_ratio_vector, conditions)
        molecule_altered = alteration_with_modes(molecule, vibration, conditions)

        if show_text:
            print('{0:12.5f} {1:12.5f}    {2:2.3f}'.format(molecule.get_energy(conditions.energy_method),
                  molecule_altered.get_energy(conditions.energy_method),
                  simulation.acceptation_ratio))

        if molecule.get_energy(conditions.energy_method) < molecule_altered.get_energy(conditions.energy_method):
            energy_ratio = math.exp((molecule.get_energy(conditions.energy_method) - molecule_altered.get_energy(conditions.energy_method))
                                    / (conditions.temperature * conditions.kb))
            if energy_ratio < random.random():
                continue

        molecule = molecule_altered
        simulation.add_accepted(iteration,conditions)
        vibration = calculate.get_modes_from_tinker(molecule, conditions)

    simulation.number_of_cycles += conditions.number_of_cycles
    return simulation




def calculate_MonteCarlo_internal(simulation, conditions, show_text=True):

    molecule = copy.deepcopy(simulation.trajectory[-1])

    print 'Temperature', conditions.temperature
    print('Starting at:',simulation.number_of_cycles)
    for iteration in range(simulation.number_of_cycles, simulation.number_of_cycles + conditions.number_of_cycles):

        simulation.update_acceptation_vector(iteration, conditions)

        simulation.append_data_from_molecule(molecule)
        conditions.expansion_factor = adjust_expansion_factor(simulation.acceptation_ratio_vector, conditions)
        molecule_altered = alteration_internal_with_weights(molecule, conditions)

        if show_text:
            print('{0:12.5f} {1:12.5f}    {2:2.3f}'.format(molecule.get_energy(conditions.energy_method),
                  molecule_altered.get_energy(conditions.energy_method),
                  simulation.acceptation_ratio))

        if molecule.get_energy(conditions.energy_method) < molecule_altered.get_energy(conditions.energy_method):
            energy_ratio = math.exp((molecule.get_energy(conditions.energy_method) - molecule_altered.get_energy(conditions.energy_method))
                                    / (conditions.temperature * conditions.kb))
            if energy_ratio < random.random():
                continue

        molecule = molecule_altered
        simulation.add_accepted(iteration,conditions)

    simulation.number_of_cycles += conditions.number_of_cycles
    return simulation



def calculate_MonteCarlo_cartesian(simulation, conditions, show_text=True):

    molecule = copy.deepcopy(simulation.trajectory[-1])

    print 'Temperature', conditions.temperature
    print('Starting at:',simulation.number_of_cycles)
    for iteration in range(simulation.number_of_cycles, simulation.number_of_cycles + conditions.number_of_cycles):

        simulation.update_acceptation_vector(iteration, conditions)

        simulation.append_data_from_molecule(molecule)
        conditions.expansion_factor = adjust_expansion_factor(simulation.acceptation_ratio_vector, conditions)
        molecule_altered = alteration_cartesian(molecule, conditions)

        if show_text:
            print('{0:12.5f} {1:12.5f}    {2:2.3f}'.format(molecule.get_energy(conditions.energy_method),
                  molecule_altered.get_energy(conditions.energy_method),
                  simulation.acceptation_ratio))

        if molecule.get_energy(conditions.energy_method) < molecule_altered.get_energy(conditions.energy_method):
            energy_ratio = math.exp((molecule.get_energy(conditions.energy_method) - molecule_altered.get_energy(conditions.energy_method))
                                    / (conditions.temperature * conditions.kb))
            if energy_ratio < random.random():
                continue

        molecule = molecule_altered
        simulation.add_accepted(iteration,conditions)

    simulation.number_of_cycles += conditions.number_of_cycles
    return simulation


if __name__ == '__main__':

    import montemodes.functions.reading as io_monte

    conditions = res.Conditions(temperature=500,
                                number_of_cycles=5,
                                initial_expansion_factor=1,
                                energy_method=2,
                                acceptation_regulator=0.1,
                                number_of_values_for_average=50)

    molecule = io_monte.reading_from_gzmat_file('../test.gzmat')

    print(molecule.get_coordinates())
    molecule2 = alteration_cartesian(molecule, conditions)
    print(molecule2.get_coordinates())