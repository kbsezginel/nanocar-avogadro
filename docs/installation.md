# Installation

## Mac OS X
[First install Avogadro 2.](https://www.openchemistry.org/downloads/)

Then download this repository and copy the contents into your Avogadro 2 plug-ins directory.

For Mac, the plug-ins directory will be present at `Applications -> Avogadro2.app -> Contents -> lib -> avogadro2 -> scripts -> workflows`.

**Note**: The repository contents (not the repository), should be copied to the plug-ins folder. For example, on a Mac, the `workflows` directory will contain `add_chassis.py` and the other repository contents.

## Linux (Ubuntu)
First build Avogadro 2 from the [openchemistry supermodule](https://github.com/OpenChemistry/openchemistry).
```
git clone https://github.com/OpenChemistry/openchemistry.git
mkdir openchemistry-build
cd openchemistry-build
cmake ../openchemistry
cmake --build . --config Release
```
More build and updating instructions can be found [here](http://wiki.openchemistry.org/Build).

```
python install_plugin.py /home/<username>/.local/share/OpenChemistry/Avogadro
```

## Windows


#### Python dependencies
Nanocar builder uses Ångström Python package to assemble molecules.

[**Ångström**](https://github.com/kbsezginel/angstrom)
```
git clone https://github.com/kbsezginel/angstrom.git
cd angstrom
python setup.py install
```
The python path must be set in Avogadro2 to the environment which contains the installed python dependencies. If you are using conda to manage your python environments, you can find the location of the environment by using the command

`conda info --envs`

Copy the path for your environment. In Avogadro2, access the Python Path variable under `Quantum -> Input Generators -> Set Python Path`
