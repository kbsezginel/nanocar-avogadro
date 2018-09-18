"""
Nanocar builder Avogadro 2 plug-in.
Adds chassis molecule.

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

chassis_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'chassis')
chassis_list = [i.split('.')[0] for i in os.listdir(chassis_dir)]


def get_options():
    """Create user interface options."""
    user_options = {}
    user_options['chassis'] = {'label': 'Chassis',
                               'type': 'stringList',
                               'default': 'benzene',
                               'values': chassis_list}

    user_options['center-x'] = {'label': 'X',
                              'type': 'float',
                              'default': 0.0,
                              'precision': 3,
                              'suffix': 'Å'}

    user_options['center-y'] = {'label': 'Y',
                              'type': 'float',
                              'default': 0.0,
                              'precision': 3,
                              'suffix': 'Å'}

    user_options['center-z'] = {'label': 'Z',
                              'type': 'float',
                              'default': 0.0,
                              'precision': 3,
                              'suffix': 'Å'}

    return {'userOptions': user_options }


def build_nanocar(opts):
    """Builds Nanocar molecule."""
    chassis = Molecule(read=os.path.join(chassis_dir, '%s.xyz' % opts['chassis']))
    chassis.center([opts['center-x'], opts['center-y'], opts['center-z']])
    return mol2xyz(chassis)


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

    result = {}
    result['append'] = True
    result['moleculeFormat'] = 'xyz'
    result['xyz'] = build_nanocar(opts)
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
        print("Add Chassis")
    if args['menu_path']:
        print("&Build|Nanocar")
    if args['print_options']:
        print(json.dumps(get_options()))
    elif args['run_workflow']:
        print(json.dumps(run_workflow()))
