"""
LAMMPS simulation file generation for Nanocars.

Author: Kutay B. Sezginel
Date: November 2018
"""
import os
import csv
import periodictable


CSV_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uff_nonbonded.csv')


def write_data_file(molecule, data_file):
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


def write_input_file(molecule, input_file):
    """Write LAMMPS input file"""
    with open(input_file, 'w') as f:
        f.write('')


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
