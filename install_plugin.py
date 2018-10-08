"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                o---o NANOCAR o---o
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Install/update Nanocar Avogadro Plug-in.
Usage:
 >>> python install_plugin.py /home/username/.local/share/OpenChemistry/Avogadro

Linux path example: /home/username/.local/share/OpenChemistry/Avogadro
"""
import os
import sys
import shutil


AVOGADRO_PLUGIN_DIR = os.path.abspath(sys.argv[1])
scripts = ['add_chassis.py', 'connect_wheel.py', 'surface_builder.py']
folders = ['wheel', 'chassis']
nanocar_dir = os.path.abspath(os.path.dirname(__file__))
workflows_dir = os.path.join(AVOGADRO_PLUGIN_DIR, 'workflows')


def copy_files(file_list, src_dir, dest_dir):
    """Copy a list of files from source to destination directory."""
    for f in file_list:
        if os.path.exists(os.path.join(dest_dir, f)):
            print('Overwriting %s' % f)
        else:
            print('Creating %s' % f)
        shutil.copy(os.path.join(src_dir, f), dest_dir)


# Copy scripts
print('\n%s Installing scipts %s' % ('-' * 20, '-' * 20))
copy_files(scripts, nanocar_dir, workflows_dir)

# Copy folders (molecules)
print('\n%s Installing molecules %s' % ('-' * 19, '-' * 19))
for f in folders:
    fdir = os.path.join(workflows_dir, f)
    if os.path.exists(fdir):
        print('\nUpdating %s molecules\n%s' % (f, '-' * 40))
    else:
        print('\nCreating %s molecules' % f)
    os.makedirs(fdir, exist_ok=True)
    copy_files(os.listdir(os.path.join(nanocar_dir, f)), os.path.join(nanocar_dir, f), fdir)

print('%s\nDone!' % ('-' * 60))
