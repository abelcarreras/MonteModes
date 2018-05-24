__author__ = 'abel'
import montemodes.functions.calculate as calc


method_function = {
    1: calc.get_energy_from_tinker,
    2: calc.get_energy_from_gaussian
}


class Gaussian:

    def __init__(self,
                 methodology='pm3',
                 internal=False,
                 memory=None,
                 processors=None,
                 binary='g09',
                 guess=None,
                 multiplicity=1,  # default multiplicity 1 (can be improved to set multiplicity according to charge)
                 alter=None):
        self._methodology = methodology
        self._memory = memory
        self._processors = processors
        self._internal = internal
        self._binary = binary
        self._parameters = {'multiplicity': multiplicity,
                            'alter': alter,
                            'guess': guess}

    def __hash__(self):
        import pickle
        return hash((self._methodology, pickle.dumps(self._parameters)))

    def single_point(self, molecule):

        return calc.get_energy_from_gaussian(molecule,
                                             self._parameters,
                                             calculation=self._methodology,
                                             internal=self._internal,
                                             processors=self._processors,
                                             binary=self._binary,)

    def vibrations(self, molecule):
        if self._internal is True:
            raise Exception('Normal modes in internal coordinates not implemented')
        modes, energy = calc.get_modes_from_gaussian(molecule,
                                                     self._parameters,
                                                     calculation=self._methodology,
                                                     processors=self._processors,
                                                     binary=self._binary)
        return modes, energy


    @property
    def internal(self):
        return self._internal

    @internal.setter
    def internal(self, internal):
        self._internal = internal

    @property
    def multiplicity(self):
        return self._parameters['multiplicity']

    @multiplicity.setter
    def multiplicity(self, multiplicity):
        self._multiplicity = multiplicity


class Tinker:

    def __init__(self,
                 parameter_set='mm3.prm',
                 num_modes=None):

        self._parameter_set = parameter_set
        self._num_modes = num_modes

        # Tinker only allow closed shell calculations
        self._multiplicity = 1

    def single_point(self, molecule):
        return calc.get_energy_from_tinker(molecule, force_field=self._parameter_set)

    def vibrations(self, molecule):
        modes = calc.get_modes_from_tinker(molecule,
                                            force_field=self._parameter_set,
                                            num_modes=self._num_modes)
        energy = None
        return modes, energy

    @property
    def multiplicity(self):
        return self._multiplicity

