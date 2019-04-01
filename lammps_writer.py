"""
LAMMPS simulation file generation for Nanocars.

Author: Kutay B. Sezginel
Date: November 2018
"""
import os
import csv
import periodictable
from textwrap import dedent


CSV_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uff_nonbonded.csv')
DATA_FILE = 'data.nanocar'
IN_FILE = 'in.nanocar'


def write_data_file(molecule):
    """
    Write LAMMPS data file.

    Parameters
    ----------
    molecule : Angstrom Molecule object

    Returns
    -------
    str
        LAMMPS formatted data file containing structure information.
    """
    q, mol_id = 0, 0
    data = dedent(f"""Created by Avogadro Nanocar Builder

    {len(molecule.atoms):10} atoms
    {0:10} bonds
    {0:10} angles
    {0:10} dihedrals
    {0:10} impropers
    {len(molecule.unique_atoms):10} atom types
    {0.0:16.5f}   {molecule.cell.a:5.5f}   xlo xhi
    {0.0:16.5f}   {molecule.cell.b:5.5f}   ylo yhi
    {0.0:16.5f}   {molecule.cell.c:5.5f}   zlo zhi

    Masses\n\n
    """)
    for idx, atom in enumerate(molecule.unique_atoms, start=1):
        data += f'{idx:5}   {periodictable.elements.symbol(atom).mass:10.5f} # {atom}\n'
    data += '\nAtoms\n\n'
    for idx, (atom, coor) in enumerate(zip(molecule.atoms, molecule.coordinates), start=1):
        typ = molecule.atom_types[atom]
        x, y, z = coor
        data += f'{idx:10}   {mol_id:3}   {typ:3}   {q:5.5f}  {x:12.5f}  {y:12.5f}  {z:12.5f}\n'
    return data


def write_input_file(molecule, parameters):
    """
    Write LAMMPS input file

    Parameters
    ----------
    molecule : Angstrom Molecule object
        Molecule
    parameters: dict
        Simulation parameters.

    Returns
    -------
    str
        LAMMPS formatted input file.
    """
    write_every = 10000
    num_timesteps = int(parameters['sim_length'] / parameters['ts'] * 1e6)

    # Start simulation input
    inp = dedent(f"""
    units           real
    atom_style      full
    boundary        p p p
    read_data       {DATA_FILE}
    """)

    # Group atoms
    for group in parameters['groups']:
        start, end = parameters['groups'][group]
        inp += f'group           {group:20}  id {start}:{end}\n'

    # Assign force field parameters
    uff = read_uff_parameters(molecule.unique_atoms)
    ff_par = {'*-*': [0, 0]}
    for atom, typ in molecule.atom_types.items():
        if atom != molecule.surface_atom:
            eps = round((uff[atom]['eps'] * uff[molecule.surface_atom]['eps']) ** 0.5, 4)
            sig = round((uff[atom]['sig'] + uff[molecule.surface_atom]['sig']) / 2, 4)
            ff_par[f'{molecule.atom_types[molecule.surface_atom]}-{typ}'] = [eps, sig]
    inp += write_pair_style(ff_par)

    # TODO: If multibody add bonds between wheels
    # Figure out how to make sure we only add bonds between wheels and chassis
    if parameters['multibody']:
        bond_id = 1
        inp += f'\nbond_style      harmonic\nbond_coeff      1 200.0 1.4\n'
        for bond in parameters['bonds']:
            inp += f'create_bonds    single/bond  {bond_id} {bond[0]} {bond[1]}\n'

    inp += dedent(f"""
    compute         C1 nanocar com
    variable        seed equal 123456
    variable        T equal {parameters['T']}
    thermo          {write_every}
    thermo_style    custom step temp press etotal epair emol c_C1[1] c_C1[2] c_C1[3]
    timestep        {parameters['ts']}
    dump            1 nanocar custom {write_every} traj.xyz id element xu yu zu
    dump_modify     1 element {' '.join(molecule.unique_atoms)}
    fix             RIG nanocar rigid/nvt single temp $T $T 100
    run             {num_timesteps}
    unfix           RIG
    """)

    # TODO : Rigid fix for multiple bodies

    # TODO: Figure out velocity assignment for rigid bodies
    # velocity        group-ID zero linear rigid RIG
    return inp


def write_pair_style(parameters, potential='lj/cut', cut_off=13.0):
    """
    Write pair style for LAMMPS.

    Parameters
    ----------
    parameters : dict
        Pairwise potential style and parameters.
        Ex: {'*-*': [0, 0], '1-2': [0.1, 5.0], '1-3': [0.2, 4]}}
    potential : str
        LAMMPS pair potential type (default : lj/cut).
    cut_off : float
        Cut off radius in Angstrom (default : 13.0).

    Returns
    -------
    str
        LAMMPS formatted pair styles and coefficients.
    """
    pair = f'\npair_style      {potential} {cut_off}\npair_modify     tail yes mix arithmetic\n'
    for par in parameters:
        p1, p2 = par.split('-')
        param = ' '.join(map(str, parameters[par]))
        pair += f'pair_coeff      {p1} {p2} {param}\n'
    return pair


def read_uff_parameters(atoms, csv_file=CSV_FILE, skip_headers=True):
    """
    Read UFF nonbonded parameters for a Lennard-Jones potential.

    Parameters
    ----------
    atoms : list
        List of atoms.
    csv_file : str
        Path to uff_parameters.csv file.

    Returns
    -------
    dict
        Epsilon and sigma parameters for the requested atoms.
    """
    rm_to_sigma = 1 / (2 ** (1/6))
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        if skip_headers:
            next(csv_reader, None)
        parameters = {}
        for row in csv_reader:
            if row[0] in atoms:
                parameters[row[0]] = {'eps': float(row[2]),
                                      'sig': float(row[1]) * rm_to_sigma}
    return parameters
