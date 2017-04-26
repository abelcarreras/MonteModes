import os
from subprocess import Popen, PIPE

class Symop:

    def __init__(self,
                 symmetry='c 5',
                 label=False,
                 connect=False,
                 central_atom=0):

        self._symmetry = symmetry
        self._label = label
        self._connect = connect
        self._central_atom = central_atom

    @property
    def symmetry(self):
        return self._symmetry

    @property
    def label(self):
        return self._label

    @property
    def connect(self):
        return self._connect

    @property
    def central_atom(self):
        return self._central_atom



def create_symop_file(molecule, input_data):

    label = input_data.label
    connect = input_data.connect
    central_atom = input_data.central_atom
    symmetry = input_data.symmetry

    temp_file_name = 'symmetry'+ '_' + str(os.getpid()) + '.zdat'

    symop_input_file = open(temp_file_name, 'w')
    if label:
        symop_input_file.write('%label')
    if connect:
        symop_input_file.write('%connect')
    symop_input_file.write(str(molecule.get_number_of_atoms()) + ' ' + str(central_atom) + '\n\n' + symmetry + '\nA\n')
    for i in range(molecule.get_number_of_atoms()):
        line = str(list(molecule.get_atomic_elements()[i]) +
                   list(molecule.get_coordinates()[i])
        ).strip('[]').replace(',', '').replace("'", "")
        symop_input_file.write(line + '\n')

    return symop_input_file


def get_symmetry(molecule, input_data):

    symop_input_file = create_symop_file(molecule, input_data)
    symop_input_file.close()

    symop_process = Popen('symop '+ symop_input_file.name, stderr=PIPE, stdout=PIPE, shell=True)
    symop_process.wait()

    measure = float(open(symop_input_file.name[:-4]+'ztab','r').readlines()[-1].split()[-1])
    os.remove(symop_input_file.name)
    os.remove(symop_input_file.name[:-4]+'ztab')
    os.remove(symop_input_file.name[:-4]+'zout')

    return measure

def get_symmetry_trajectory(trajectory, input_data):
    symmetry_list = []
    for molecule in trajectory[1:]:
        symmetry_list.append(get_symmetry(molecule, input_data))

    return symmetry_list



if __name__ == '__main__':

    import montemodes.functions.reading as io_monte

   # molecule = io_monte.reading_from_gzmat_file('../test.gzmat')
  #  molecule = io_monte.reading_from_xyz_file('../../../test.xyz')
    molecule = io_monte.reading_from_txyz_file('../../Data/ethane.txyz')
    symop_input = Symop(symmetry='s')


    print(get_symmetry(molecule, symop_input))
