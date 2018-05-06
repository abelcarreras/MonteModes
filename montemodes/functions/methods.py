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
                 multiplicity=1):  # default multiplicity 1 (can be improved to set multiplicity according to charge)

        self._methodology = methodology
        self._memory = memory
        self._processors = processors
        self._internal = internal
        self._binary = binary
        self._multiplicity = multiplicity

    def single_point(self, molecule):

        return calc.get_energy_from_gaussian(molecule,
                                             calculation=self._methodology,
                                             internal=self._internal,
                                             processors=self._processors,
                                             binary=self._binary,
                                             multiplicity=self._multiplicity)

    def vibrations(self, molecule):
        modes, energy = calc.get_modes_from_gaussian(molecule,
                                                     calculation=self._methodology,
                                                     binary=self._binary,
                                                     multiplicity=self._multiplicity)
        return modes, energy


    @property
    def internal(self):
        return self._internal

    @internal.setter
    def internal(self, internal):
        self._internal = internal

    @property
    def multiplicity(self):
        return self._multiplicity

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

