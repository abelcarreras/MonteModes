__author__ = 'abel'
import montemodes.functions.calculate as calc

method_function = {
    1: calc.get_energy_from_tinker,
    2: calc.get_energy_from_gaussian
}

class gaussian:

    def __init__(self,
                 methodology='pm3',
                 internal=False,
                 memory=None,
                 processors=None):

        self._methodology = methodology
        self._memory = memory
        self._processors = processors
        self._internal=internal


    def single_point(self, molecule):
        return calc.get_energy_from_gaussian(molecule,
                                             calculation=self._methodology,
                                             internal=self._internal)

    def vibrations(self, molecule):
        modes, energy = calc.get_modes_from_gaussian(molecule,
                                                     calculation=self._methodology)
        return modes, energy


    @property
    def internal(self):
        return self._internal

    @internal.setter
    def internal(self, internal):
        self._internal = internal


class tinker:

    def __init__(self,
                 parameter_set='mm3.prm',
                 num_modes=None):

        self._parameter_set = parameter_set
        self._num_modes = num_modes


    def single_point(self, molecule):
        return calc.get_energy_from_tinker(molecule, force_field=self._parameter_set)

    def vibrations(self, molecule):
        modes =  calc.get_modes_from_tinker(molecule,
                                            force_field=self._parameter_set,
                                            num_modes=self._num_modes)
        energy = None
        return modes, energy
