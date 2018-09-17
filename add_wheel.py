"""
Nanocar Avogadro 2 plug-in - Add Wheel.
Adds wheel molecule to selected atom.

Author: Kutay B. Sezginel
Date: September 2018

TODO:
- Bonding information is lost after adding the wheel. Maybe just append the molecule.
- Append: True might be changing the coordinates of the appended molecule!!!
"""
import os
import sys
import json
import argparse
from angstrom import Molecule
import numpy as np
import periodictable


# Some globals:
debug = True

wheel_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'wheel')
wheel_list = [i.split('.')[0] for i in os.listdir(wheel_dir)]


def get_options():
    """Create user interface options."""
    user_options = {}
    user_options['wheel'] = {'label': 'Wheel',
                             'type': 'stringList',
                             'default': 'C60',
                             'values': wheel_list}

    user_options['append'] = {'label': 'Append',
                              'type': 'stringList',
                              'default': 'True',
                              'values': ['True', 'False']}

    return {'userOptions': user_options }


def add_wheel(opts):
    """
    Add wheel molecule to selected atom position.
    The wheel molecule must have a dummy atom (X) to specify connectivity.
    A selected wheel molecule is added to selected atom by aligning the vector of the wheel.
    """
    selected = [idx for idx, atm in enumerate(opts['cjson']['atoms']['selected']) if atm]
    if len(selected) == 1:
        # Get chassi coordinates and bonds
        coords = np.array(opts['cjson']['atoms']['coords']['3d'])
        connections = opts['cjson']['bonds']['connections']['index']
        atoms = [periodictable.elements[i].symbol for i in opts['cjson']['atoms']['elements']['number']]
        chassi = Molecule(atoms=atoms, coordinates=np.array(coords).reshape((int(len(coords) / 3)), 3))

        # Get wheel coordinate
        selected_cidx = int(selected[0] * 3)
        selected_coors = coords[selected_cidx:selected_cidx + 3]

        # Get dummy atom
        wheel = Molecule(read=os.path.join(wheel_dir, '%s.xyz' % opts['wheel']))
        dummy_idx, = np.where(wheel.atoms == 'X')[0]  # Maybe check if more than one?

        # Find atom connected to the selected atom
        bond_idx = connections.index(selected[0])
        if bond_idx % 2 == 0:
            bond_idx += 1
        else:
            bond_idx -= 1

        # Get vector btw selected atom and atom connected to it
        v_chassi = selected_coors - np.array(coords[bond_idx:bond_idx + 3])

        # Align the wheel with that vector
        v_wheel = wheel.coordinates[0] - wheel.coordinates[dummy_idx]
        wheel.align(v_wheel, v_chassi)

        # Translate the wheel to match dummy coor with selected coor
        v_trans = selected_coors - wheel.coordinates[dummy_idx]
        wheel.translate(v_trans)

        # Remove dummy atom
        wheel.coordinates = np.delete(wheel.coordinates, [dummy_idx], axis=0)
        wheel.atoms = np.delete(wheel.atoms, [dummy_idx])
        if not {'True': True, 'False': False}[opts['append']]:
            wheel += chassi

        wheel.center(selected_coors)
        wheel = mol2xyz(wheel)
    else:
        print('Only 1 atom should be selected!')
        wheel = None

    return wheel


def mol2xyz(mol):
    """Converts Angstrom Molecule to xyz string"""
    mol_xyz = "%i\n%s\n" % (len(mol.atoms), mol.name)
    for atom, coor in zip(mol.atoms, mol.coordinates):
        mol_xyz += "%s %f %f %f\n" % (atom, coor[0], coor[1], coor[2])
    return mol_xyz


def run_workflow():
    """Run main function - add wheel."""
    stdinStr = sys.stdin.read()
    opts = json.loads(stdinStr)

    result = opts['cjson']
    result['append'] = {'True': True, 'False': False}[opts['append']]
    result['moleculeFormat'] = 'xyz'
    result['xyz'] = add_wheel(opts)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Build Nanocar!')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-workflow', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("Add Wheel")
    if args['menu_path']:
        print("&Build|Nanocar")
    if args['print_options']:
        print(json.dumps(get_options()))
    elif args['run_workflow']:
        print(json.dumps(run_workflow()))
