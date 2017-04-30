import os
from subprocess import Popen, PIPE

class Shape:

    def __init__(self,
                 central_atom=0,
                 code=1,
                 custom_atom_list=None):

        self._code = code
        self._central_atom = central_atom
        self._custom_atom_list = custom_atom_list


    @property
    def code(self):
        return self._code

    @property
    def central_atom(self):
        return self._central_atom

    @property
    def custom_atom_list(self):
        return self._custom_atom_list


def create_shape_file(molecule, input_data):

    code = input_data.code
    central_atom = input_data.central_atom
    atoms_list = input_data.custom_atom_list

    if isinstance(atoms_list, type(None)):
        atoms_list = range(molecule.get_number_of_atoms())

    if central_atom == 0:
        ligands = len(atoms_list)
    else:
        ligands = len(atoms_list) - 1

    temp_file_name = 'shape' + '_' + str(os.getpid()) + '.dat'

    shape_input_file = open(temp_file_name, 'w')

    shape_input_file.write('{0} {1}\n'.format(ligands, central_atom))
    shape_input_file.write('{0}\n'.format(code))

    shape_input_file.write('montemodes\n')

    for i in atoms_list:
        line = str(list(molecule.get_atomic_elements()[i]) +
                   list(molecule.get_coordinates()[i])
        ).strip('[]').replace(',', '').replace("'", "")
        shape_input_file.write(line + '\n')

    return shape_input_file


def get_shape(molecule, input_data):

    shape_input_file = create_shape_file(molecule, input_data)
    shape_input_file.close()
    shape_process = Popen('shape ' + shape_input_file.name, stdout=PIPE, shell=True)
    shape_process.wait()

    measure = float(open(shape_input_file.name[:-4]+'.tab','r').readlines()[-1].split()[-1])


    os.remove(shape_input_file.name)
    os.remove(shape_input_file.name[:-4]+'.tab')

    return measure


def get_shape_trajectory(trajectory, input_data):
    symmetry_list = []
    for molecule in trajectory[1:]:
        symmetry_list.append(get_shape(molecule, input_data))

    return symmetry_list


def get_info(vertices=None):

    shape_process = Popen('shape +', stdout=PIPE, shell=True)
    (output, err) = shape_process.communicate()
    shape_process.wait()

    list = output.split('\n')
    indices = [(i, x.split()[1]) for i, x in enumerate(list) if "Vertices" in x]

    vertices_info = {}
    for index, v in indices:
        vertex_info = []
        j = 1
        while j > 0:
            if list[index+j] == '':
                break
            line = list[index+j].split()
            line[3:] = [' '.join(line[3:])]
            line[1] = int(line[1])
            vertex_info.append(line)
            j += 1
        vertices_info[v] = vertex_info

    if vertices is not None:
        return vertices_info[str(vertices)]

    return vertices_info


if __name__ == '__main__':

    import montemodes.functions.reading as io_monte

   # molecule = io_monte.reading_from_gzmat_file('../test.gzmat')
    molecule = io_monte.reading_from_xyz_file('../../test.xyz')
  #  molecule = io_monte.reading_from_txyz_file('../../Data/ethane.txyz')
    shape_input = Shape(code=1)


    print(get_shape(molecule, shape_input))

