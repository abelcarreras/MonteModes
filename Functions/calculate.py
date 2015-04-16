import tempfile
import numpy as np
import subprocess
import classes.results as res
import os, glob
from subprocess import Popen, PIPE

force_filed = 'mm3.prm'


def create_tinker_input(molecule):
#    temp_file_name = tempfile.gettempdir() + '_' + str(os.getpid())
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


def create_gaussian_internal_input(molecule):

    temp_file_name = tempfile.gettempdir() + '/gaussian_temp'+ '_' + str(os.getpid())
#    temp_file_name = 'test_gauss'
    gaussian_input_file = open(temp_file_name,mode='w')
#    gaussian_input_file.write('#p M062X/LANL2DZ NOSYMM opt=Z-matrix NOFMM 5D 7F' + '\n\n')
    gaussian_input_file.write('#p pm6' + '\n\n')

    gaussian_input_file.write('model [Hf(C6F5)6]2- prisma HF=-4414.3959893' + '\n\n')

    gaussian_input_file.write('-2 1\n')

    for i in range(len(molecule.get_atomic_elements_with_dummy())):
        line = str([list(molecule.get_atomic_elements_with_dummy()[i]) +
                    list(molecule.get_z_matrix()[i])]).strip('[]').replace('[', '').replace(',', '').replace("'", "")
        gaussian_input_file.write(line + '\n')

    gaussian_input_file.write('Variables:\n')


    for i in range(molecule.get_int_label().shape[0]):
        line = str([list(molecule.get_int_label()[i]) +
                    list(molecule.get_internal()[i])]).strip('[]').replace('[', '').replace(',', '').replace("'", "")
        gaussian_input_file.write(line + '\n')

    gaussian_input_file.write('\n')

    gaussian_input_file.close()

    return gaussian_input_file

def create_gaussian_input(molecule, calculation='pm6', charge=0, multiplicity=1):

    atomic_elements = molecule.get_atomic_elements()[:, 0]
    coordinates = molecule.get_coordinates()

    input_file = "# "+calculation+"\n\nPython Input\n\n"+str(charge)+" "+str(multiplicity)+"\n"
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




def get_energy_from_gaussian(molecule, calculation='pm6'):

    input_data = create_gaussian_input(molecule,
                                       calculation=calculation)

    conversion = 627.503 # hartree to kcal/mol

    gaussian_process = Popen('g09', stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    (output, err) = gaussian_process.communicate(input=input_data)
    gaussian_process.wait()

   # print(output)
    try:
        energy = float(output[output.find('E('):].split()[2])
    except IndexError or ValueError:
        print('Failed trying to get energy from gaussian output')
        print('\n'.join(output.splitlines()[-10:]))
        energy = 1E20
    return energy * conversion


def get_energy_from_gaussian_2(molecule):
    conversion = 627.503 # hartree to kcal/mol
    gaussian_input_file = create_gaussian_internal_input(molecule)

    gaussian_command = './g09 < ' + gaussian_input_file.name

    tinker_process = subprocess.Popen(gaussian_command, stdout=subprocess.PIPE, shell=True)
    (output, err) = tinker_process.communicate()
    tinker_process.wait()

    os.unlink(gaussian_input_file.name)

    try:
        energy = float(output[output.find('E('):].split()[2])
    except IndexError or ValueError:
        print('Failed trying to get energy from gaussian output')
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

if __name__ == '__main__':

    import Functions.reading as io_monte

    molecule = io_monte.reading_from_gzmat_file('../test.gzmat')

    print(get_energy_from_gaussian(molecule,calculation='pm6'))
