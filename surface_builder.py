"""
Surface builder Avogadro 2 plug-in.

Author: Kutay B. Sezginel
Date: September 2018
"""
import os
import sys
import json
import argparse
from angstrom import Molecule
import ase.build


# Some globals:
debug = True
crystals = ['bcc100', 'bcc110', 'bcc111', 'fcc100', 'fcc110', 'fcc111', 'fcc211']


def get_options():
    """Create user interface options."""
    user_options = {}
    user_options['surface'] = {'label': 'Surface',
                               'type': 'stringList',
                               'default': 'bcc100',
                               'values': crystals}

    return {'userOptions': user_options }


def build_surface(opts):
    """Builds crystal surface."""
    surf = dict(crystal=opts['surface'], metal='Au', a=4, size=[10, 10, 5], vacuum=0, orthogonal=True)
    builder = getattr(ase.build, surf['crystal'])
    ase_surf = builder(surf['metal'], a=surf['a'], size=surf['size'], vacuum=surf['vacuum'], orthogonal=surf['orthogonal'])
    ase_surf.center(about=(0, 0, 0))
    return ase2xyz(ase_surf)


def ase2xyz(atoms):
    """Converts Angstrom Molecule to xyz string"""
    atoms.write('temp.xyz', append=False)
    xyz = ""
    with open('temp.xyz', 'r') as f:
        for line in f:
            xyz += line
    return xyz


def run_workflow():
    # Read options from stdin
    stdinStr = sys.stdin.read()

    # Parse the JSON strings
    opts = json.loads(stdinStr)

    # Prepare the result
    result = {}
    result['append'] = True
    result['moleculeFormat'] = 'xyz'
    result['xyz'] = build_surface(opts)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Build Surface')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-workflow', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("ASE Surface")
    if args['menu_path']:
        print("&Build")
    if args['print_options']:
        print(json.dumps(get_options()))
    elif args['run_workflow']:
        print(json.dumps(run_workflow()))
