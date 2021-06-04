"""
Nanocar Avogadro 2 plug-in - LAMMPS setup.
Write LAMMPs simulation input files.

Author: Kutay B. Sezginel
Date: November 2018
"""
import os
import sys
from pathlib import Path
import json
import argparse
from angstrom import Molecule
import numpy as np
import periodictable
from lammps_writer import write_data_file, write_input_file


FF_LIST = ['UFF', 'UFF4MOF', 'DREIDING']
PLUGIN_DIR = os.path.abspath(os.path.dirname(__file__))


def get_options():
    """Create user interface options."""
    user_options = {}

    surface_info = read_surface_info()
    user_options['box_x'] = {'label': 'Simulation Box X (nm)',
                              'type': 'float',
                              'default': surface_info['x'] / 10}

    user_options['box_y'] = {'label': 'Simulation Box Y (nm)',
                              'type': 'float',
                              'default': surface_info['y'] / 10}

    user_options['box_z'] = {'label': 'Simulation Box Z (nm)',
                              'type': 'float',
                              'default': 3.0}

    user_options['timestep'] = {'label': 'Timestep (fs)',
                                'type': 'float',
                                'default': 1.0}

    user_options['sim_length'] = {'label': 'Simulation length (ns)',
                                  'type': 'float',
                                  'default': 1.0}

    user_options['dir'] = {'label': 'Save directory',
                           'type': 'filePath',
                           'default': PLUGIN_DIR}

    return {'userOptions': user_options }


def run_command():
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
    opts['box_x'], opts['box_y'], opts['box_z'] = opts['box_x'] * 10, opts['box_y'] * 10, opts['box_z'] * 10
    nanocar.set_cell([opts['box_x'], opts['box_y'], opts['box_z'], 90, 90, 90])
    nanocar.center([opts['box_x'] / 2, opts['box_y'] / 2, opts['box_z'] / 2])
    if not os.path.isdir(opts['dir']):
        # try removing the last part of the path (a file)
        parent = (Path(opts['dir']).parent.absolute())
        if not os.path.isdir(parent):
            opts['dir'] = PLUGIN_DIR
            print('Directory not found! Using plug-in directory -> %s' % PLUGIN_DIR)
        else:
            opts['dir'] = parent
    data_file = os.path.join(opts['dir'], 'data.nanocar')
    write_data_file(data_file, nanocar)

    # Write input file
    surface_info = read_surface_info()
    surface_ids = surface_info['id']
    surface_atoms = surface_ids[1] - surface_ids[0]
    num_atoms = len(nanocar.atoms)
    if surface_ids[0] == 1:
        mol_ids = [num_atoms - surface_atoms, num_atoms]
    else:
        mol_ids = [1, num_atoms - surface_atoms - 1]
    input_file = os.path.join(opts['dir'], 'in.nanocar')
    inp_parameters = {'sim_length': opts['sim_length'], 'ts': opts['timestep'],
                      'mol_ids': mol_ids, 'surface_ids': surface_ids, 'T': 300}
    write_input_file(input_file, nanocar, inp_parameters)


def read_surface_info():
    """Read surface size for the last metal surface built."""
    filename = os.path.join(PLUGIN_DIR, 'surface_info.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            surface_info = json.load(f)
    else:
        surface_info = {'x': 0.0, 'y': 0.0, 'id': [0, 0]}
    return surface_info


if __name__ == "__main__":
    parser = argparse.ArgumentParser('LAMMPS!')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--print-options', action='store_true')
    parser.add_argument('--run-command', action='store_true')
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
    elif args['run_command']:
        print(json.dumps(run_command()))
