"""
Nanocar builder Avogadro 2 plug-in.

Author: Kutay B. Sezginel
Date: August 2018
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

chassis_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'chassis')
chassis_list = [i.split('.')[0] for i in os.listdir(chassis_dir)]


def get_options():
    """Create user interface options."""
    user_options = {}
    user_options['wheel'] = {'label': 'Wheel',
                             'type': 'stringList',
                             'default': 'C60',
                             'values': wheel_list}

    user_options['chassis'] = {'label': 'Chassis',
                               'type': 'stringList',
                               'default': 'benzene',
                               'values': chassis_list}

    return {'userOptions': user_options }


def build_nanocar(opts):
    """Builds Nanocar molecule."""
    chassis = Molecule(read=os.path.join(chassis_dir, '%s.xyz' % opts['chassis']))
    wheel = Molecule(read=os.path.join(wheel_dir, '%s.xyz' % opts['wheel']))
    wheel.translate([5, 0, 0])
    nanocar = chassis + wheel
    return mol2xyz(nanocar)

def mol2xyz(mol):
    """Converts Angstrom Molecule to xyz string"""
    mol_xyz = "%i\n%s\n" % (len(mol.atoms), mol.name)
    for atom, coor in zip(mol.atoms, mol.coordinates):
        mol_xyz += "%s %f %f %f\n" % (atom, coor[0], coor[1], coor[2])
    return mol_xyz


def add_molecule(opts):
    """Read selected molecule."""
    mol_xyz = os.path.join(mol_dir, '%s.xyz' % opts['mol'])
    with open(mol_xyz, 'r') as f:
        newmol = f.readlines()
    return ''.join(newmol)


def run_workflow():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Prepare the result
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
        print("Nanocar!")
    if args['menu_path']:
        print("&Build")
    if args['print_options']:
        print(json.dumps(get_options()))
    elif args['run_workflow']:
        print(json.dumps(run_workflow()))
