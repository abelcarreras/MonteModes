__author__ = 'abel'
import Functions.calculate as calc

method_function = {
    1: calc.get_energy_from_tinker,
    2: calc.get_energy_from_gaussian
}

class gaussian:

    def __init__(self,
                 methodology='pm3'):


        self._methodology = methodology


    def function(self, molecule):
        return calc.get_energy_from_gaussian(molecule, self._methodology)



class tinker:

    def __init__(self,
                 parameter_set='mm3'):

        self._parameter_set = parameter_set


    def function(self, molecule):

        return calc.get_energy_from_tinker(molecule)

