"""
Surface builder Avogadro 2 plug-in.

Author: Kutay B. Sezginel
Date: September 2018
"""
import os
import sys
import json
import argparse
import ase.build


# Some globals:
debug = True
surface_selections = ['bcc100', 'bcc110', 'bcc111', 'fcc100', 'fcc110', 'fcc111', 'fcc211']
PLUGIN_DIR = os.path.abspath(os.path.dirname(__file__))


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


def build_surface(opts):
    """Builds crystal surface."""
    builder = getattr(ase.build, opts['surface'])
    size = [opts['size-x'], opts['size-y'], opts['size-z']]
    ase_surf = builder(opts['metal'], a=opts['a'], size=size, vacuum=opts['vacuum'], orthogonal=opts['orthogonal'])
    ase_surf.center(about=(0, 0, -opts['vacuum']))
    # Get surface atom id to keep track of surface atoms
    try:
        surf_atom_id = int(len(opts['cjson']['atoms']['coords']['3d']) / 3 + 1)
    except KeyError:
        surf_atom_id = 1
    surface_info = {'x': ase_surf.cell[0][0], 'y': ase_surf.cell[1][1],
                    'id': [surf_atom_id, ase_surf.get_number_of_atoms() + surf_atom_id - 1]}
    write_surface_info(surface_info)
    return ase2xyz(ase_surf)


def write_surface_info(surface_info):
    """Write surface size to a file to be read later to get the correct simulation box size."""
    with open(os.path.join(PLUGIN_DIR, 'surface_info.json'), 'w') as outfile:
        json.dump(surface_info, outfile)


def ase2xyz(atoms):
    """Converts ASE Atoms object to xyz string"""
    atoms.write('temp.xyz', append=False)
    xyz = ""
    with open('temp.xyz', 'r') as f:
        for line in f:
            xyz += line
    return xyz


def run_workflow():
    """Run surface builder."""
    stdinStr = sys.stdin.read()
    opts = json.loads(stdinStr)

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
        print("&Build|Nanocar")
    if args['print_options']:
        print(json.dumps(get_options()))
    elif args['run_workflow']:
        print(json.dumps(run_workflow()))
