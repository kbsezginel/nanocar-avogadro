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
from lammps_writer import write_data_file, write_input_file, DATA_FILE, IN_FILE


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
                           'type': 'string',
                           'default': PLUGIN_DIR}

    user_options['multibody'] = {'label': 'Multibody',
                                 'type': 'boolean',
                                 'default': True}

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
    opts['box_x'], opts['box_y'], opts['box_z'] = opts['box_x'] * 10, opts['box_y'] * 10, opts['box_z'] * 10
    nanocar.set_cell([opts['box_x'], opts['box_y'], opts['box_z'], 90, 90, 90])
    nanocar.center([opts['box_x'] / 2, opts['box_y'] / 2, opts['box_z'] / 2])
    if not os.path.isdir(opts['dir']):
        opts['dir'] = PLUGIN_DIR
        print('Directory not found! Using plug-in directory -> %s' % PLUGIN_DIR)

    # Read surface info
    surface_info = read_surface_info()
    surface_ids = surface_info['id']

    # Determine unique atom types and labels
    nanocar.unique_atoms = sorted(list(set(nanocar.atoms)))
    nanocar.atom_types = {atom: idx for idx, atom in enumerate(nanocar.unique_atoms, start=1)}
    nanocar.surface_atom = nanocar.atoms[surface_info['id'][0]]

    # Write data file
    with open(os.path.join(opts['dir'], DATA_FILE), 'w') as f:
        f.write(write_data_file(nanocar))

    # Determine atom grouping | wheel bonding info!
    mol_bonds = []
    mol_groups = {'surface': surface_info['id']}
    if opts['multibody']:
        # Read wheel info
        wheel_list_file = os.path.join(PLUGIN_DIR, 'wheel_list.json')
        if os.path.exists(wheel_list_file):
            with open(wheel_list_file, 'r') as outfile:
                wheels = json.load(outfile)
        # Determine atom groups
        for widx, w in enumerate(wheels, start=1):
            mol_groups['%s_%i' % (w['name'], widx)] = [w['start'], w['start'] + w['n_atoms'] - 1]
            mol_bonds.append(w['bond'])
        mol_groups['chassis'] = [1, min([i[0] for i in mol_groups.values()]) - 1]
        mol_groups['nanocar'] = [1, max([i[1] for g, i in mol_groups.items() if g != 'surface'])]
    else:
        surface_atoms = surface_ids[1] - surface_ids[0]
        num_atoms = len(nanocar.atoms)
        if surface_ids[0] == 1:
            mol_ids = [num_atoms - surface_atoms, num_atoms]
        else:
            mol_ids = [1, num_atoms - surface_atoms - 1]
        mol_groups['nanocar'] = mol_ids

    inp_parameters = {'sim_length': opts['sim_length'], 'ts': opts['timestep'],
                      'groups': mol_groups, 'T': 300, 'multibody': opts['multibody'],
                      'bonds': mol_bonds}

    with open(os.path.join(opts['dir'], IN_FILE), 'w') as f:
        f.write(write_input_file(nanocar, inp_parameters))

    nanocar.write(os.path.join(opts['dir'], 'nanocar.xyz'))


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
