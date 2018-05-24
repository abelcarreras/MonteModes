import numpy as np


def get_magnetic_coupling(molecule, bs_singlet_method, triplet_method):
    """
    Calculates the magnetic coupling constant J as:
    E(triplet) - E(singlet broken symmetry)
    :param molecule: molecule type object
    :param bs_singlet_method: Gaussian method object defining singlet broken symmetry state calculation
    :param triplet_method: Gaussian method object defining triplet state calculation
    :return: compling constant J
    """

    j = molecule.get_energy(method=triplet_method) - molecule.get_energy(method=bs_singlet_method)

    return j


def get_magnetic_coupling_trajectory(trajectory, bs_singlet_method, triplet_method):
    """
    Calculates the magnetic coupling constant J for a list of molecules
    :param trajectory: list of molecule type objects
    :param bs_singlet_method: Gaussian method object defining singlet broken symmetry state calculation
    :param triplet_method: Gaussian method object defining triplet state calculation
    :return: list of coupling constants J
    """

    return [get_magnetic_coupling(molecule, bs_singlet_method, triplet_method) for molecule in trajectory]