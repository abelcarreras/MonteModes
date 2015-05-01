import os
from subprocess import Popen, PIPE

class Shape:

    def __init__(self,
                 central_atom=0,
                 code=1,
                 vertices=2):

        self._code = code
        self._vertices = vertices
        self._central_atom = central_atom

    @property
    def code(self):
        return self._code

    @property
    def vertices(self):
        return self._vertices

    @property
    def central_atom(self):
        return self._central_atom



def create_shape_file(molecule, input_data):

    code = input_data.code
    vertices = input_data.vertices
    central_atom = input_data.central_atom

    if central_atom == 0:
        ligands = len(molecule.get_coordinates())
    else:
        ligands = len(molecule.get_coordinates()) - 1

    temp_file_name = 'shape' + '_' + str(os.getpid()) + '.dat'

    shape_input_file = open(temp_file_name, 'w')

    shape_input_file.write('{0} {1}\n'.format(ligands, central_atom))
    shape_input_file.write('{0} {1}\n'.format(vertices, code) )

    shape_input_file.write('montemodes\n')

    for i in range(molecule.get_number_of_atoms()):
        line = str(list(molecule.get_atomic_elements()[i]) +
                   list(molecule.get_coordinates()[i])
        ).strip('[]').replace(',', '').replace("'", "")
        shape_input_file.write(line + '\n')

    return shape_input_file


def get_shape(molecule, input_data):

    shape_input_file = create_shape_file(molecule, input_data)
    shape_input_file.close()
    symop_process = Popen(['shape', shape_input_file.name], stdout=PIPE)
    symop_process.wait()

    measure = float(open(shape_input_file.name[:-4]+'.tab','r').readlines()[-1].split()[-1])

    os.remove(shape_input_file.name)
    os.remove(shape_input_file.name[:-4]+'.tab')

    return measure

def get_shape_trajectory(trajectory, input_data):
    symmetry_list = []
    for molecule in trajectory[1:]:
        symmetry_list.append(get_shape(molecule, input_data))

    return symmetry_list



if __name__ == '__main__':

    import montemodes.functions.reading as io_monte

   # molecule = io_monte.reading_from_gzmat_file('../test.gzmat')
    molecule = io_monte.reading_from_xyz_file('../../test.xyz')
  #  molecule = io_monte.reading_from_txyz_file('../../Data/ethane.txyz')
    shape_input = Shape(code=1)


    print(get_shape(molecule, shape_input))
