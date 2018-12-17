"""
Nanocar Avogadro 2 plug-in - LAMMPS setup.
Write LAMMPs simulation input files.

Author: Kutay B. Sezginel
Date: November 2018
"""
import os
import sys
import json
import argparse
from angstrom import Molecule
import numpy as np
import periodictable
from lammps_writer import write_data_file


FF_LIST = ['UFF', 'UFF4MOF', 'DREIDING']
PLUGIN_DIR = os.path.abspath(os.path.dirname(__file__))


def get_options():
    """Create user interface options."""
    user_options = {}

    box_size = read_surface_size()
    user_options['box_x'] = {'label': 'Simulation Box X',
                              'type': 'float',
                              'default': box_size['x']}

    user_options['box_y'] = {'label': 'Simulation Box Y',
                              'type': 'float',
                              'default': box_size['y']}

    user_options['box_z'] = {'label': 'Simulation Box Z',
                              'type': 'integer',
                              'default': 40}

    user_options['dir'] = {'label': 'Save directory',
                           'type': 'string',
                           'default': PLUGIN_DIR}

    return {'userOptions': user_options }


def run_workflow():
    """Run main function - LAMMPS setup."""
    stdinStr = sys.stdin.read()
    opts = json.loads(stdinStr)

    setup_lammps(opts)


def setup_lammps(opts):
    """Write LAMMPS simulation files."""
    # Read structure information
    coords = np.array(opts['cjson']['atoms']['coords']['3d'])
    atoms = [periodictable.elements[i].symbol for i in opts['cjson']['atoms']['elements']['number']]
    nanocar = Molecule(atoms=atoms, coordinates=np.array(coords).reshape((int(len(coords) / 3)), 3))
    nanocar.set_cell([opts['box_x'], opts['box_y'], opts['box_z'], 90, 90, 90])
    nanocar.center([opts['box_x'] / 2, opts['box_y'] / 2, opts['box_z'] / 2])
    if not os.path.isdir(opts['dir']):
        opts['dir'] = PLUGIN_DIR
        print('Directory not found! Using plug-in directory -> %s' % PLUGIN_DIR)
    data_file = os.path.join(opts['dir'], 'data.nanocar')
    write_data_file(nanocar, data_file)


def read_surface_size():
    """Read surface size for the last metal surface built."""
    filename = os.path.join(PLUGIN_DIR, 'surface_size.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            surface_size = json.load(f)
    else:
        surface_size = {'x': 0.0, 'y': 0.0}
    return surface_size


if __name__ == "__main__":
    parser = argparse.ArgumentParser('LAMMPS!')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-workflow', action='store_true')
    parser.add_argument('--display-name', action='store_true')
    parser.add_argument('--menu-path', action='store_true')
    parser.add_argument('--lang', nargs='?', default='en')
    args = vars(parser.parse_args())

    debug = args['debug']

    if args['display_name']:
        print("LAMMPS setup")
    if args['menu_path']:
        print("&Build|Nanocar")
    if args['print_options']:
        print(json.dumps(get_options()))
    elif args['run_workflow']:
        print(json.dumps(run_workflow()))
