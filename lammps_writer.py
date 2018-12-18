"""
LAMMPS simulation file generation for Nanocars.

Author: Kutay B. Sezginel
Date: November 2018
"""
import os
import csv
import periodictable


CSV_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uff_nonbonded.csv')


def write_data_file(data_file, molecule):
    """Write LAMMPS data file"""
    q = 0
    mol_id = 0
    unique_atoms = sorted(list(set(molecule.atoms)))
    uff_par = read_uff_parameters(CSV_FILE, unique_atoms)
    atom_types = {}
    with open(data_file, 'w') as f:
        f.write('Created by Avogadro Nanocar Builder\n\n')
        f.write('%10i atoms\n' % len(molecule.atoms))
        f.write('%10i bonds\n' % 0)
        f.write('%10i angles\n' % 0)
        f.write('%10i dihedrals\n' % 0)
        f.write('%10i impropers\n\n' % 0)
        f.write('%10i atom types\n\n' % len(unique_atoms))
        f.write('%16.5f   %5.5f   xlo xhi\n' % (0.0, molecule.cell.a))
        f.write('%16.5f   %5.5f   ylo yhi\n' % (0.0, molecule.cell.b))
        f.write('%16.5f   %5.5f   zlo zhi\n\n' % (0.0, molecule.cell.c))
        f.write('Masses\n\n')
        for idx, atom in enumerate(unique_atoms, start=1):
            atom_types[atom] = idx
            f.write('%5i   %10.5f # %s\n' % (idx, periodictable.elements.symbol(atom).mass, atom))
        f.write('\nPair Coeffs\n\n')
        for idx, atom in enumerate(unique_atoms, start=1):
            f.write('%5i   %8.5f   %8.5f # %s\n' % (idx, uff_par[atom]['eps'], uff_par[atom]['sig'], atom))
        f.write('\nAtoms\n\n')
        for idx, (atom, coor) in enumerate(zip(molecule.atoms, molecule.coordinates), start=1):
            f.write('%10i   %3i   %3i   %5.5f  %12.5f  %12.5f  %12.5f\n' % (idx, mol_id, atom_types[atom], q, coor[0], coor[1], coor[2]))


def write_input_file(input_file, molecule, parameters):
    """Write LAMMPS input file"""
    write_every = 10000
    num_timesteps = int(parameters['sim_length'] / parameters['ts'] * 1e6)
    mol_ids, surface_ids = parameters['mol_ids'], parameters['surface_ids']
    atom_names = sorted(list(set(molecule.atoms)))
    with open(input_file, 'w') as f:
        f.write('log             log.nanocar append\n')
        f.write('units           real\n')
        f.write('atom_style      full\n')
        f.write('boundary        p p p\n')
        f.write('pair_style      lj/cut 12.500\n')
        f.write('pair_modify     tail yes mix arithmetic\n')
        f.write('read_data       data.nanocar\n\n')
        f.write('group           mol      id   %i:%i\n' % (mol_ids[0], mol_ids[1]))
        f.write('group           surf     id   %i:%i\n' % (surface_ids[0], surface_ids[1]))
        f.write('compute         C1 mol com\n')
        f.write('variable        seed equal 123456\n')
        f.write('variable        T equal %i\n'% parameters['T'])
        f.write('thermo          %i\n' % write_every)
        f.write('thermo_style    custom step temp press etotal epair emol c_C1[1] c_C1[2] c_C1[3]\n')
        f.write('velocity        mol create $T ${seed} dist uniform\n')
        f.write('timestep        %.1f\n' % parameters['ts'])
        f.write('variable        txyz equal %i\n' % write_every)
        f.write('dump            1 mol custom ${txyz} traj.xyz id element xu yu zu\n')
        f.write('dump_modify     1 element %s\n\n' % ' '.join(atom_names))
        f.write('fix             RIG mol rigid/nvt single temp $T $T 100\n')
        f.write('run             %i\n' % num_timesteps)
        f.write('unfix           RIG\n')


def read_uff_parameters(csv_file, atoms, skip_headers=True):
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        if skip_headers:
            next(csv_reader, None)
        parameters = {}
        for row in csv_reader:
            if row[0] in atoms:
                parameters[row[0]] = {'eps': float(row[2]), 'sig': float(row[1])}
    return parameters
