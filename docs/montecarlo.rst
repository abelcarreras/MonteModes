MonteCarlo simulation
=====================

Prepare the simulation
----------------------

Calculation method
++++++++++++++++++

The calculation method define the software to use to calculate the atomic interactions.
Two software are implemented: :program:`Gaussian09` and :program:`Tinker`. To use these calculators, Gaussian and/or Tinker
should be installed in your system and the binaries (or hard links to them) should be placed in a
directory included in the $PATH environment variable with the name :program:`g09` and :program:`tinker`,
respectively. Note that setting up an alias in :file:`.profile` or :file:`.bashrc` for these software will
not work.

Gaussian 09 ::

    from montecarlo.functions.method import gaussian
    calculator = gaussian(methodology='pm6' [String],
                          internal=False [Boolean],
                          processors=None [Integer])

- methodology: Method label to use in :program:`Gaussian09`. This argument should contain the basis set if it is necessary (Ex: B3LYP/6-31G).
- Internal: Use internal coordinates (z-matrix).
- Set number of processors to use in the :program:Gaussian09` calculation.

Tinker ::

    from montecarlo.functions.method import tinker
    calculator = tinker(parameter_set='mm3.prm' [String]):

- parameter_set: name of the force field file to use. This file should be placed in the work directory or full path should be specified


Conditions
++++++++++

Conditions object contains the parameters of the Monte Carlo simulation ::

    from montecarlo.classes.results import Conditions
    conditions = Conditions(temperature=None [Float],
                            number_of_cycles=100000 [Integer],
                            kb=0.0019872041, # kcal/mol
                            initial_expansion_factor=0.05 [Float],
                            acceptation_regulator=1.0 [Float],
                            number_of_values_for_average=2000 [Integer],
                            energy_method=calculator [Method object])

- temperature: Temperature at which the MonteCarlo simulation is calcuculated.
- number_of_cycles: Number of simulation steps
- energy_method: Calculation method object
- initial_expansion_factor: Initial factor of acceptance
- acceptation_regulator: Ratio of alteration of the factor of acceptance as a function of acceptance.
- number_of_values_for_average: Number of last simulation steps used to calculate the averaged properties.
- kb: Boltzmann constant according to the units of energy and temperature

Run the simulation
------------------

Montecarlo object contains all the information concerting to the simulation. This object is generated from a
structure object tha contains the initial structure ::

    from montecarlo.classes.results import MonteCarlo
    simulation = MonteCarlo(structure)

To Run the simulation the *calculate_MonteCarlo()* is used. This function returns a MonteCarlo object
that contains the results ::

    from montecarlo.functions.montecarlo import calculate_MonteCarlo
    simulation = calculate_MonteCarlo(simulation [Montecarlo type],
                                      conditions [Conditions type],
                                      show_text=True [Boolean],
                                      alteration_type='cartesian' [String])
      Return result [Montecarlo type]


- simulation: Initial Montecarlo object. If this object already contains information of a previous simulation, the simulation will continue adding the data of the new simulation.
- conditions: Conditions object.
- show_text: If True writes montecarlo information on screen during the simulation calculation. If False the calculation is carried out silently.
- alteration_type: Defines the way the structures are altered during each simulation step. The possible options are 'cartesian' 'internal' or 'modes'.

The returned Montecarlo object can be used again in the *calculate_MonteCarlo()* function to continue the simulation.


Save results to data files
--------------------------

To save the MonteCarlo data into files some helper functions are available in ::

    montemodes.functions.reading

Save the energy, acceptation of each simulation ::

    write_result_to_file(result, 'test.out')

Save the trajectory into a file in xyz format ::

    write_result_trajectory(result.trajectory, 'trajectory.xyz')

Save the full simulation objects into a file ::

    save_to_dump(conditions, result, filename='full.obj')

Load the simulation objects from a file ::

    load_from_dump(filename='full.obj')



Example
-------
::

    import montemodes.functions.reading as io_monte
    import montemodes.functions.montecarlo as monte
    import montemodes.functions.methods as method
    import montemodes.classes.results as res


    gaussian_calc = method.gaussian(methodology='pm6',
                                    internal=False)

    conditions = res.Conditions(temperature=500,
                                number_of_cycles=1000,
                                initial_expansion_factor=0.05,
                                acceptation_regulator=0.1,
                                number_of_values_for_average=20,
                                energy_method=gaussian_calc)

    initial_structure = io_monte.reading_from_xyz_file('molecule.xyz')
    initial_structure.charge = 0
    initial_structure.multiplicity = 1

    simulation = res.MonteCarlo(initial_structure)

    result = monte.calculate_MonteCarlo(simulation,
                                        conditions,
                                        show_text=True,
                                        alteration_type='cartesian')

    io_monte.write_result_to_file(result, 'montecarlo.out')
    io_monte.write_result_trajectory(result.trajectory, 'trajectory.xyz')

