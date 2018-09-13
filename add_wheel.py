"""
Nanocar Avogadro 2 plug-in - Add Wheel.
Adds wheel molecule to selected atom.

Author: Kutay B. Sezginel
Date: September 2018
"""
import os
import sys
import json
import argparse
from angstrom import Molecule


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

    return {'userOptions': user_options }


def add_wheel(opts):
    """Add wheel molecule to selected atom position."""
    selected = [idx for idx, atm in enumerate(opts['cjson']['atoms']['selected']) if atm]
    if len(selected) == 1:
        selected = int(selected[0] * 3)
        selected_coors = opts['cjson']['atoms']['coords']['3d'][selected:selected + 3]
        wheel = Molecule(read=os.path.join(wheel_dir, '%s.xyz' % opts['wheel']))
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
    result['append'] = False
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
