"""
LAMMPS simulation file generation for Nanocars.

Author: Kutay B. Sezginel
Date: November 2018
"""
import periodictable


def write_data_file(molecule, data_file):
    """Write LAMMPS data file"""
    q = 0
    mol_id = 0
    unique_atoms = sorted(list(set(molecule.atoms)))
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
            f.write('%5i   %3.5f # %s\n' % (idx, periodictable.elements.symbol(atom).mass, atom))
        f.write('\nAtoms\n\n')
        for idx, (atom, coor) in enumerate(zip(molecule.atoms, molecule.coordinates), start=1):
            f.write('%10i   %3i   %3i   %5.5f  %12.5f  %12.5f  %12.5f\n' % (idx, mol_id, atom_types[atom], q, coor[0], coor[1], coor[2]))
