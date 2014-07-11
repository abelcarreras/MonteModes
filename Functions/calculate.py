import tempfile
import numpy as np
import subprocess
import classes.results as res
import os

force_filed = 'mm3.prm'


def create_tinker_input(molecule):
    temp_file_name = tempfile.gettempdir() + '/' + str(os.getpid())
    tinker_input_file = open(temp_file_name,mode='w')
#    print(tinker_input_file.name)

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


def get_modes_from_tinker(molecule):
    tinker_input_file = create_tinker_input(molecule)
    tinker_command = 'Data/vibrate ' + tinker_input_file.name + ' Data/' + force_filed + ' A'

    tinker_process = subprocess.Popen(tinker_command, stdout=subprocess.PIPE, shell=True)
    (output, err) = tinker_process.communicate()

    tinker_process.wait()

    # for i in range(10):
    lines = output.split()
    modes = []
    frequencies = []
    pos = lines.index('Vibrational')
    for f in range(molecule.get_number_of_atoms() * 3):
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
    #    print(np.array(frequencies)[1])
    #    print(np.array(modes)[2])

    return total_modes