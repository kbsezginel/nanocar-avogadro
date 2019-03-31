"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            o---o NANOCAR o---o
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Install/update Nanocar Avogadro Plug-in.
Usage:
 >>> python install_plugin.py /path/to/avogadro/plugin/directory

See installation instructions for more information:
https://kbsezginel.github.io/nanocar-avogadro/installation
"""
import os
import shutil
import argparse
from textwrap import dedent


def copy_files(file_list, src_dir, dest_dir):
    """Copy a list of files from source to destination directory."""
    for f in file_list:
        if os.path.exists(os.path.join(dest_dir, f)):
            print('Overwriting %s' % f)
        else:
            print('Creating %s' % f)
        shutil.copy(os.path.join(src_dir, f), dest_dir)


def install_plugin(args):
    """Install nanocar plug-in: copy all scripts and required files."""
    files = ['add_chassis.py', 'connect_wheel.py', 'surface_builder.py',
             'lammps_writer.py', 'lammps_setup.py', 'uff_nonbonded.csv']
    folders = ['wheel', 'chassis']
    cleanup = ['temp.xyz', 'surface_info.json', 'data.nanocar']

    plugin_dir = os.path.join(os.path.abspath(args['scripts_dir']),
                              args['subfolder'])
    nanocar_dir = os.path.abspath(os.path.dirname(__file__))

    if not os.path.exists(plugin_dir):
        print('Plug-in directory does not exist, creating...')
        os.makedirs(plugin_dir)

    # Copy scripts and other files
    print('\n%s Installing scipts %s' % ('-' * 20, '-' * 20))
    copy_files(files, nanocar_dir, plugin_dir)

    # Copy folders (molecules)
    print('\n%s Installing molecules %s' % ('-' * 19, '-' * 19))
    for f in folders:
        fdir = os.path.join(plugin_dir, f)
        if os.path.exists(fdir):
            print('\nUpdating %s molecules\n%s' % (f, '-' * 40))
        else:
            print('\nCreating %s molecules' % f)
        os.makedirs(fdir, exist_ok=True)
        copy_files(os.listdir(os.path.join(nanocar_dir, f)),
                   os.path.join(nanocar_dir, f), fdir)

    # Cleanup files
    print('\n%s Cleanup %s' % ('-' * 25, '-' * 26))
    for f in cleanup:
        if os.path.exists(os.path.join(plugin_dir, f)):
            os.remove(os.path.join(plugin_dir, f))
            print('Removing temp file -> %s' % f)

    print('\n%s\nDone!' % ('-' * 60))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=dedent("""
    Install/update Nanocar Avogadro Plug-in.
    =================================================
                   o---o NANOCAR o---o
    =================================================
    """), epilog=dedent("""
    Example:
    > python install_plugin.py /path/to/avogadro/plugin/directory

    See installation instructions for more information:
    https://kbsezginel.github.io/nanocar-avogadro/installation
    """), formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('scripts_dir', type=str,
                        help='Avogadro2 plug-in directory.')

    parser.add_argument('--subfolder', '-s', type=str, default='workflows',
                        help='Plugin subfolder name (default: workflows).')
    args = vars(parser.parse_args())

    install_plugin(args)
