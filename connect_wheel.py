"""
Nanocar Avogadro 2 plug-in - Add Wheel.
Connects wheel molecule to selected atom.

Author: Kutay B. Sezginel
Date: September 2018
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
                              'type': 'boolean',
                              'default': True}

    user_options['d'] = {'label': 'Bond Distance',
                         'type': 'float',
                         'precision': 2,
                         'default': 1.5,
                         'suffix': 'Å'}

    return {'userOptions': user_options }


def connect_wheel(opts):
    """
    Connect wheel molecule to selected atom position.
    The wheel molecule must have a connection site (Xc) and alignmen site (Xa) to specify connectivity.
    The selected wheel molecule is added to selected atom by aligning the vector of the wheel.
    """
    selected = [idx for idx, atm in enumerate(opts['cjson']['atoms']['selected']) if atm]
    if len(selected) == 1:
        # Get chassi coordinates and bonds
        coords = np.array(opts['cjson']['atoms']['coords']['3d'])
        connections = opts['cjson']['bonds']['connections']['index']
        atoms = [periodictable.elements[i].symbol for i in opts['cjson']['atoms']['elements']['number']]
        chassi = Molecule(atoms=atoms, coordinates=np.array(coords).reshape((int(len(coords) / 3)), 3))

        # Get connection site for the chassis
        selected_cidx = int(selected[0] * 3)
        selected_coors = coords[selected_cidx:selected_cidx + 3]

        # Find atom connected to the selected atom
        bond_idx = connections.index(selected[0])
        if bond_idx % 2 == 0:
            bond_idx += 1
        else:
            bond_idx -= 1
        bond_idx = int(connections[bond_idx] * 3)

        # Get vector btw selected atom and atom connected to it
        v_chassi = selected_coors - np.array(coords[bond_idx:bond_idx + 3])

        # Read wheel molecule information
        wheel = read_wheel(opts['wheel'])

        # Align the wheel with chassis connection vector
        v_wheel = wheel.coordinates[wheel.alignment_site] - wheel.coordinates[wheel.connection_site]
        wheel.align(v_wheel, v_chassi)

        # Translate the wheel to match dummy coor with selected coor
        v_trans = selected_coors - wheel.coordinates[wheel.connection_site]
        wheel.translate(v_trans)

        # Adjust bond distance
        v_bond = wheel.coordinates[wheel.connection_site] - wheel.coordinates[wheel.alignment_site]
        d_bond = np.linalg.norm(v_bond)
        v_bond = v_bond - v_bond / d_bond * opts['d']
        wheel.translate(v_bond)

        # Remove dummy atoms for alignment and connection sites
        wheel.coordinates = np.delete(wheel.coordinates, [wheel.connection_site, wheel.alignment_site], axis=0)
        wheel.atoms = np.delete(wheel.atoms, [wheel.connection_site, wheel.alignment_site])
        if not opts['append']:
            wheel += chassi

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


def read_wheel(wheel_name):
    """Read yaml file to Molecule object"""
    wheel = Molecule(read=os.path.join(wheel_dir, '%s.xyz' % wheel_name))
    wheel.connection_site, = np.where(wheel.atoms == 'Xc')[0]
    wheel.alignment_site, = np.where(wheel.atoms == 'Xa')[0]
    return wheel


def run_workflow():
    """Run main function - add wheel."""
    stdinStr = sys.stdin.read()
    opts = json.loads(stdinStr)

    result = opts['cjson']
    result['append'] = opts['append']
    result['moleculeFormat'] = 'xyz'
    result['xyz'] = connect_wheel(opts)
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
        print("Connect Wheel")
    if args['menu_path']:
        print("&Build|Nanocar")
    if args['print_options']:
        print(json.dumps(get_options()))
    elif args['run_workflow']:
        print(json.dumps(run_workflow()))
