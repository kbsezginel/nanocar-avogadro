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
surface_selections = ['bcc100', 'bcc110', 'bcc111', 'fcc100', 'fcc110', 'fcc111', 'fcc211']


def get_options():
    """Create user interface options."""
    user_options = {}
    user_options['surface'] = {'label': 'Surface',
                               'type': 'stringList',
                               'default': 'bcc100',
                               'values': surface_selections}

    user_options['metal'] = {'label': 'Metal',
                             'type': 'string',
                             'default': 'Au'}

    user_options['a'] = {'label': 'Lattice Constant',
                         'type': 'float',
                         'precision': 3,
                         'suffix': 'Å'}

    user_options['size-x'] = {'label': 'Size X',
                              'type': 'integer',
                              'default': 5}

    user_options['size-y'] = {'label': 'Size Y',
                              'type': 'integer',
                              'default': 5}

    user_options['size-z'] = {'label': 'Size Z',
                              'type': 'integer',
                              'default': 3}

    user_options['vacuum'] = {'label': 'Vacuum distance',
                              'type': 'float',
                              'precision': 1,
                              'suffix': 'Å'}

    user_options['orthogonal'] = {'label': 'Orthogonal',
                                  'type': 'stringList',
                                  'default': 'True',
                                  'values': ['True', 'False']}

    return {'userOptions': user_options }


    userOptions['Z Scale']['label'] = 'Z Scale'
    userOptions['Z Scale']['type'] = 'float'
    userOptions['Z Scale']['default'] = 1.0
    userOptions['Z Scale']['precision'] = 3
    userOptions['Z Scale']['toolTip'] = 'Multiplier for Z coordinates'


def build_surface(opts):
    """Builds crystal surface."""
    builder = getattr(ase.build, opts['surface'])
    size = [opts['size-x'], opts['size-y'], opts['size-z']]
    ase_surf = builder(opts['metal'], a=opts['a'], size=size, vacuum=opts['vacuum'], orthogonal=opts['orthogonal'])
    ase_surf.center(about=(0, 0, 0))
    return ase2xyz(ase_surf)


def ase2xyz(atoms):
    """Converts ASE Atoms object to xyz string"""
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
    parser = argparse.ArgumentParser('Build Metal Surface')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-workflow', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("Metal Surface")
    if args['menu_path']:
        print("&Build")
    if args['print_options']:
        print(json.dumps(get_options()))
    elif args['run_workflow']:
        print(json.dumps(run_workflow()))
