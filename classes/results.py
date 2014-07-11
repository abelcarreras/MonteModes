from __future__ import division
import numpy as np
import copy as cp

def normalize_modes(modes):

    normalized_modes = cp.deepcopy(modes)
    for i in range(modes.shape[0]):
        average_vector = np.average(modes[i], axis=0)
        normalized_modes[i] = np.add(modes[i], -np.array([average_vector] * modes.shape[1]))

    return normalized_modes


class Vibration:

    def __init__(self,
                 frequencies=None,
                 modes=None):

        self._frequencies = frequencies
        self._modes = modes
        self._normalized_modes = None

    @property
    def frequencies(self):
        return self._frequencies

    @frequencies.setter
    def frequencies(self, frequencies):
        self._frequencies = frequencies

    @property
    def modes(self):
        return self._modes

    @modes.setter
    def modes(self, modes):
        self._normalized_modes = None
        self._modes = modes

    @property
    def normalized_modes(self):
        if self._normalized_modes is None:
            self._normalized_modes = normalize_modes(self._modes)
        return self._normalized_modes

    @property
    def number_of_modes(self):
        return self._frequencies.shape[0]


class MonteCarlo:
    def __init__(self, molecule):
        self._energy = None
        self._trajectory = []
        self._acceptation_ratio_vector = []
        self._number_of_cycles = 0
        self._accepted_vector = [0]
        self._acceptation_ratio = 0
        self._trajectory.append(molecule)

    @property
    def trajectory(self):
        return self._trajectory

    @trajectory.setter
    def trajectory(self, trajectory):
        self._trajectory = trajectory

    @property
    def energy(self):
        if self._energy is None:
            self._energy = [self.trajectory[i].get_energy() for i in range(self.number_of_data)]
        return self._energy

    @property
    def number_of_data(self):
        return len(self._trajectory)

    @property
    def number_of_cycles(self):
        return self._number_of_cycles

    @number_of_cycles.setter
    def number_of_cycles(self, number_of_cycles):
        self._number_of_cycles = number_of_cycles

    def append_data_from_molecule(self, molecule):
        # self._energy.append(molecule.get_energy())
        self._energy = None
        self._trajectory.append(molecule)

    @property
    def acceptation_ratio(self):
        return self._acceptation_ratio
    @property
    def acceptation_ratio_vector(self):
        return self._acceptation_ratio_vector

    def update_acceptation_vector(self, iteration):
        number_average = 50
        if iteration > 0:
#            print(self._accepted_vector[-number_average:])
#            self._acceptation_ratio = float(len(self._accepted_vector[-number_average:]) / (iteration - self._accepted_vector[-number_average:][0]))
#            self._acceptation_ratio_vector.append(self._acceptation_ratio)
#        print(self._acceptation_ratio_vector)

            for k in reversed(range(len(self._accepted_vector))):
                if self._accepted_vector[k] < (iteration - number_average) or k == 0:
                    self._acceptation_ratio = float(len(self._accepted_vector[k:])/(min(number_average,iteration)+1))
                    break

            self._acceptation_ratio_vector.append(self._acceptation_ratio)




    def add_accepted(self, iteration):
        self._accepted_vector.append(iteration)
#        print(self._accepted_vector)

    def clear_data(self):
        self._energy = None
        self._trajectory = None
        self._accepted = None


class Conditions:
    def __init__(self,
                 number_of_cycles=None,
                 kb=0.0019872041, # kcal/mol
                 temperature_frequency_relation=0.694989, #K/cm
                 temperature=None,
                 initial_expansion_factor=None,
                 acceptation_regulator = 1.0,
                 number_of_modes_to_use=None,
                 number_of_values_for_average=20):

        self._number_of_cycles = number_of_cycles
        self._temperature = temperature
        self._kb = kb
        self._temperature_frequency_relation = temperature_frequency_relation
        self._expansion_factor = initial_expansion_factor
        self._number_of_modes_to_use = number_of_modes_to_use
        self._number_of_vales_for_average = number_of_values_for_average
        self._acceptation_regulator = acceptation_regulator

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, temperature):
        self._temperature = temperature

    @property
    def number_of_vales_for_average(self):
        return self._number_of_vales_for_average

    @number_of_vales_for_average.setter
    def number_of_vales_for_average(self, number_of_vales_for_average):
        self._number_of_vales_for_average = number_of_vales_for_average

    @property
    def number_of_modes_to_use(self):
        return self._number_of_modes_to_use

    @number_of_modes_to_use.setter
    def number_of_modes_to_use(self, number_of_modes_to_use):
        self._number_of_modes_to_use = number_of_modes_to_use

    @property
    def kb(self):
        return self._kb

    @kb.setter
    def kb(self, kb):
        self._kb = kb

    @property
    def temperature_frequency_relation(self):
        return self._temperature_frequency_relation

    @temperature_frequency_relation.setter
    def temperature_frequency_relation(self, temperature_frequency_relation):
        self._temperature_frequency_relation = temperature_frequency_relation

    @property
    def acceptation_regulator(self):
        return self._acceptation_regulator

    @acceptation_regulator.setter
    def acceptation_regulator(self, acceptation_regulator):
        self._acceptation_regulator = acceptation_regulator

    @property
    def number_of_cycles(self):
        return self._number_of_cycles

    @number_of_cycles.setter
    def number_of_cycles(self, number_of_cycles):
        self._number_of_cycles = number_of_cycles

    @property
    def expansion_factor(self):
        return self._expansion_factor

    @expansion_factor.setter
    def expansion_factor(self, expansion_factor):
        self._expansion_factor = expansion_factor