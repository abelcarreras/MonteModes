import tempfile
import numpy as np
import subprocess
import classes.results as res
import os, glob
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile

force_filed = 'mm3.prm'


def create_tinker_input(molecule):

    temp_file_name = tempfile.gettempdir() + '/tinker_temp'+ '_' + str(os.getpid())
    tinker_input_file = open(temp_file_name,mode='w')

    tinker_input_file.write(str(molecule.get_number_of_atoms()) + '\n')
    for i in range(molecule.get_number_of_atoms()):
        line = str([list(molecule.get_atomic_numbers()[i]) +
                    list(molecule.get_atomic_elements()[i]) +
                    list(molecule.get_coordinates()[i]) +
                    list(molecule.get_atom_types()[i]) +
                    list(molecule.get_connectivity()[i])]).strip('[]').replace(',', '').replace("'", "")

        tinker_input_file.write(line + '\n')

    tinker_input_file.close()

    return tinker_input_file


def create_gaussian_input(molecule, calculation='pm6', internal=False):

    multiplicity = molecule.multiplicity
    charge = molecule.charge

    input_file = "# "+calculation+"\n\nPython Input\n\n"+str(charge)+" "+str(multiplicity)+"\n"

 #Zmatrix
    if internal:
        atomic_elements = molecule.get_atomic_elements_with_dummy()[:, 0]
        z_matrix = molecule.get_z_matrix()
        input_file += atomic_elements[0] + '\n'
        for index, element in enumerate(atomic_elements[1:]):
            input_file += (element + '\t' +
                           '\t'.join(z_matrix[index+1][0]) + '\n')

        internal_labels = molecule.get_int_label()
        input_file += 'Variables:\n'
        for label in internal_labels:
            input_file += (label[0] + '\t' +
                           str(molecule.get_int_dict()[label[0]])+'\n')
  #Cartessian
    else:
        atomic_elements = molecule.get_atomic_elements()[:, 0]
        coordinates = molecule.get_coordinates()

        for index, element in enumerate(atomic_elements):
            input_file += (element + "\t" +
                           str(coordinates[index][0]) + "\t" +
                           str(coordinates[index][1]) + "\t" +
                           str(coordinates[index][2]) + "\n")

    return input_file + "\n"


def get_energy_from_tinker(molecule):
    tinker_input_file = create_tinker_input(molecule)
    key_file_name = os.path.splitext(molecule.file_name)[0] + '.key'
    if not os.path.isfile(key_file_name):
        key_file_name = ''

    tinker_command = 'Data/analyze ' + tinker_input_file.name + \
                     ' Data/' + force_filed + ' E -k ' + key_file_name


    tinker_process = subprocess.Popen(tinker_command, stdout=subprocess.PIPE, shell=True)
    (output, err) = tinker_process.communicate()
    tinker_process.wait()
    os.unlink(tinker_input_file.name)

    try:
        energy = float(output[output.find('Total Potential Energy'):].replace('D','E').split()[4])
    except IndexError:
        print('Failed trying to get energy from tinker output')
        energy = 1E20

    return energy


def get_energy_from_gaussian(molecule, calculation='pm6', internal=False):

    input_data = create_gaussian_input(molecule,
                                       calculation=calculation,
                                       internal=internal)


    conversion = 627.503 # hartree to kcal/mol

    gaussian_process = Popen('g09', stdout=PIPE, stderr=PIPE, shell=True)
    (output, err) = gaussian_process.communicate(input=input_data)
    gaussian_process.wait()

    try:
        energy = float(output[output.find('E('):].split()[2])
    except IndexError or ValueError:
        print('Failed trying to get energy from gaussian output')
        print('\n'.join(output.splitlines()[-10:]))
        energy = 1E20
    return energy * conversion


def get_modes_from_tinker(molecule, conditions):

    if conditions.number_of_modes_to_use is None:
        tinker_list = ' A'
        conditions.number_of_modes_to_use = 3 * molecule.get_number_of_atoms()
    else:
        if conditions.number_of_modes_to_use >= (3 * molecule.get_number_of_atoms()):
            tinker_list = ' A'
            conditions.number_of_modes_to_use = 3 * molecule.get_number_of_atoms()
        else:
            tinker_list = ' ' + ' '.join(map(str, range(1,conditions.number_of_modes_to_use+1)))

    tinker_input_file = create_tinker_input(molecule)
    tinker_command = 'Data/vibrate ' + tinker_input_file.name + ' Data/' + force_filed + tinker_list

    tinker_process = subprocess.Popen(tinker_command, stdout=subprocess.PIPE, shell=True)
    (output, err) = tinker_process.communicate()

    tinker_process.wait()

    # for i in range(10):
    lines = output.split()
    modes = []
    frequencies = []
    pos = lines.index('Vibrational')

    if conditions.number_of_modes_to_use is None:
        number_of_modes = molecule.get_number_of_atoms() * 3
    else:
        number_of_modes = conditions.number_of_modes_to_use

    for f in range(number_of_modes):
        pos = lines.index('Vibrational', pos + 1)
        if pos == -1:
            break
        frequencies.append(float(lines[pos + 6]))
        pos = lines.index('Z', pos + 1)
        mode = []
        for k in range(molecule.get_number_of_atoms()):
            mode.append([float(i) for i in lines[pos + k * 4 + 2:pos + k * 4 + 5]])
        modes.append(mode)

    total_modes = res.Vibration(frequencies=np.array(frequencies),
                                modes=np.array(modes))

    for filePath in glob.glob(tinker_input_file.name+".*"):
        if os.path.isfile(filePath):
            os.remove(filePath)

    return total_modes

def create_symop_file(molecule, symmetry, label, connect, central_atom):

    temp_file_name = '../symmetry'+ '_' + str(os.getpid()) + '.zdat'

    symop_input_file = open(temp_file_name, 'w')
    if label:
        symop_input_file.write('%label')
    if connect:
        symop_input_file.write('%connect')
    symop_input_file.write(str(molecule.get_number_of_atoms()) + ' ' + str(central_atom) + '\n' + symmetry + '\nA\n')
    for i in range(molecule.get_number_of_atoms()):
        line = str(list(molecule.get_atomic_elements()[i]) +
                   list(molecule.get_coordinates()[i])
        ).strip('[]').replace(',', '').replace("'", "")
        symop_input_file.write(line + '\n\n')

    return symop_input_file


def get_symmetry(molecule, symmetry='c 5', label=False, connect=False, central_atom=0):

    symop_input_file = create_symop_file(molecule, symmetry, label, connect, central_atom)
    symop_input_file.close()

    symop_process = Popen(['../External/symop', symop_input_file.name], stdout=PIPE)
    symop_process.wait()

    measure = float(open(symop_input_file.name[:-4]+'ztab','r').readlines()[-1].split()[-1])

    os.remove(symop_input_file.name)
    os.remove(symop_input_file.name[:-4]+'ztab')
    os.remove(symop_input_file.name[:-4]+'zout')

    return measure


if __name__ == '__main__':

    import Functions.reading as io_monte

   # molecule = io_monte.reading_from_gzmat_file('../test.gzmat')
    molecule = io_monte.reading_from_xyz_file('../test.xyz')
    print(get_symmetry(molecule,symmetry='s'))

    print(create_gaussian_input(molecule,internal=False))
    print(get_energy_from_gaussian(molecule,calculation='pm6'))
