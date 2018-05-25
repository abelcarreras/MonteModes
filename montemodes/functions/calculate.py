import tempfile
import subprocess
import os
import glob
from subprocess import Popen, PIPE
from multiprocessing import  cpu_count

import numpy as np

import montemodes.classes.results as res


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


def create_gaussian_input(molecule,
                          calculation='pm6',
                          internal=False,
                          type='energy',
                          processors=1,
                          multiplicity=1,
                          guess=None,
                          name='Automatically generated input',
                          alter=None):

    keywords = {'energy' : ' ', 'vibration' : ' freq '}

    if processors is None:
        processors = cpu_count()

    charge = molecule.charge
    input_file = '%NProcShared={0}\n'.format(processors)
    # Calculation definition line
    input_file += '#'+keywords[type]+calculation+' '

    guess_string = []
    if alter is not None:
        guess_string.append('alter')
    if guess is not None:
        guess_string.append(guess)

    if len(guess_string) > 0:
        input_file += 'guess=({})'.format(','.join(guess_string))

    input_file += '\n\n{}\n\n'.format(name)
    input_file += '{} {}\n'.format(charge, multiplicity)

 # Z-matrix
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
  # Cartessian
    else:
        atomic_elements = molecule.get_atomic_elements()[:, 0]
        coordinates = molecule.get_coordinates()

        for index, element in enumerate(atomic_elements):
            input_file += (element + "\t" +
                           str(coordinates[index][0]) + "\t" +
                           str(coordinates[index][1]) + "\t" +
                           str(coordinates[index][2]) + "\n")

    if alter is not None:
        input_file += "\n"
        if isinstance(alter, dict):
            for pair in alter['alpha']:
                input_file += '{} {}\n'.format(pair[0], pair[1])
            input_file += "\n"
            for pair in alter['beta']:
                input_file += '{} {}\n'.format(pair[0], pair[1])
            input_file += "\n"
        else:
            for pair in alter:
                input_file += '{} {}\n'.format(pair[0], pair[1])
            input_file += "\n"

    return input_file + "\n"


def get_energy_from_tinker(molecule, force_field = 'mm3.prm'):
    tinker_input_file = create_tinker_input(molecule)
    key_file_name = os.path.splitext(molecule.file_name)[0] + '.key'
    if not os.path.isfile(key_file_name):
        key_file_name = ''

    tinker_command = 'analyze ' + tinker_input_file.name + \
                     ' ' + force_field + ' E -k ' + key_file_name


    tinker_process = subprocess.Popen(tinker_command, stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)
    (output, err) = tinker_process.communicate()
    tinker_process.wait()
    os.unlink(tinker_input_file.name)

    try:
        energy = float(output[output.find('Total Potential Energy'):].replace('D','E').split()[4])
    except IndexError and ValueError:
        print('\n'.join(output.splitlines()[-3:]))
        print('Failed trying to get energy from tinker output')
        energy = 1E20

    return energy


def get_energy_from_gaussian(molecule, parameters, calculation='pm6', internal=False, processors=1, binary='g09'):

    input_data = create_gaussian_input(molecule,
                                       calculation=calculation,
                                       internal=internal,
                                       processors=processors,
                                       multiplicity=parameters['multiplicity'],
                                       alter=parameters['alter'],
                                       guess=parameters['guess'])

    conversion = 627.503 # hartree to kcal/mol

    gaussian_process = Popen(binary, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    (output, err) = gaussian_process.communicate(input=input_data)
    gaussian_process.wait()

    try:
        energy = float(output[output.find('E('):].split()[2])
    except IndexError or ValueError:
        print('Failed trying to get energy from gaussian output')
        print('\n'.join(output.splitlines()[-10:]))
        energy = 1E20
    return energy * conversion


def get_modes_from_gaussian(molecule, parameters, calculation='pm6', binary='g09', processors=1):

    input_data = create_gaussian_input(molecule,
                                       calculation=calculation,
                                       internal=False,
                                       processors=processors,
                                       type='vibration',
                                       multiplicity=parameters['multiplicity'],
                                       alter=parameters['alter'],
                                       guess=parameters['guess'])

    conversion = 627.503  # Hartree to kcal/mol
    gaussian_process = Popen(binary, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    (output, err) = gaussian_process.communicate(input=input_data)
    gaussian_process.wait()

    # Check if calculation is finished successfully
    if 'Error termination' in output:
        print ('Error in Gaussian normal modes calculation!')
        print (output)

    lines = output[output.find('Frequencies'):].split()

    # Frequencies
    indexes = [i for i, x in enumerate(lines) if x == 'Frequencies']
    frequencies = np.array([[lines[i+2], lines[i+3], lines[i+4]] for i in indexes],dtype=float).flatten()


    # Modes
    num_atoms = molecule.get_number_of_atoms()
    num_modes = 3 * num_atoms

    modes = []
    for block in range(num_modes/3-2):
        indexes = [i for i, x in enumerate(lines) if x == 'Atom']
        freq_i = np.array([lines[indexes[block]+11+i*11:indexes[block]+11+(i+1)*11] for i in range(num_atoms)],dtype=float)[:,2:]

        for i in range(0, 9, 3):
            modes.append(freq_i[:,i:i+3].tolist())

    #Energia
    try:
        energy = float(output[output.find('E('):].split()[2])
    except IndexError or ValueError:
        print('Failed trying to get energy from gaussian output')
        print('\n'.join(output.splitlines()[-10:]))
        energy = 1E20

    total_modes = res.Vibration(frequencies=np.array(frequencies),
                                modes=np.array(modes))

    return total_modes, energy * conversion


def get_modes_from_tinker(molecule, force_field='mm3.prm', num_modes=None):

    if num_modes is None:
        tinker_list = ' A'
        num_modes = 3 * molecule.get_number_of_atoms()
    else:
        if num_modes >= (3 * molecule.get_number_of_atoms()):
            tinker_list = ' A'
            num_modes = 3 * molecule.get_number_of_atoms()
        else:
            tinker_list = ' ' + ' '.join(map(str, range(1,num_modes+1)))

    tinker_input_file = create_tinker_input(molecule)
    tinker_command = 'vibrate ' + tinker_input_file.name + ' ' + force_field + tinker_list

    tinker_process = subprocess.Popen(tinker_command, stdout=subprocess.PIPE, shell=True)
    (output, err) = tinker_process.communicate()

    tinker_process.wait()

    # for i in range(10):
    lines = output.split()
    modes = []
    frequencies = []
    pos = lines.index('Vibrational')

    if num_modes is None:
        number_of_modes = molecule.get_number_of_atoms() * 3
    else:
        number_of_modes = num_modes

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

    import montemodes.functions.reading as io_monte

   # molecule = io_monte.reading_from_gzmat_file('../test.gzmat')
    molecule = io_monte.reading_from_xyz_file('../test.xyz')
    print(get_energy_from_gaussian(molecule, calculation='am1'))
   # print(get_symmetry(molecule,symmetry='s'))

   # print(create_gaussian_input(molecule,internal=False))
   # print(get_energy_from_gaussian(molecule,calculation='pm6'))
