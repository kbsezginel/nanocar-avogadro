## Avogadro Nanocar Builder Plug-in
Build a Nanocar molecule by picking molecular wheels and chassis in [Avogadro](https://www.openchemistry.org/projects/avogadro2/)! Just select which wheels and chassis you want and your nanocar will be ready.

### Select your parts

<img src='https://raw.githubusercontent.com/kbsezginel/kbsezginel.github.io/master/assets/img/presentations/avogadro/nanocar-bodyparts.png'>



### Assemble
<img src='https://raw.githubusercontent.com/kbsezginel/kbsezginel.github.io/master/assets/img/presentations/avogadro/nanocar-assembly.png'>

## Avogadro Plug-in

<img src='https://raw.githubusercontent.com/kbsezginel/chem-tools-tutorials/master/assets/img/Avogadro2_Full_Large.png'>

### Installation
[First install Avogadro.](https://www.openchemistry.org/downloads/)

Then download this repository and copy the contents into your Avogadro 2 plug-ins directory.

For Mac, the plug-ins directory will be present at `Applications -> Avogadro2.app -> Contents -> lib -> avogadro2 -> scripts -> workflows`.

**Note**: The repository contents (not the repository), should be copied to the plug-ins folder. For example, on a Mac, the `workflows` directory will contain `add_chassis.py` and the other repository contents.


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

### Usage
If the installation went smoothly you should see a Nanocar entry under Build menu.
Clicking the Nanocar entry would prompt you to select a wheel and a chassis molecule.
After the selection the Nanocar will be built!

To start building a nanocar, see the tutorial [here.](https://kbsezginel.github.io/nanocar-avogadro/nanocar-tutorial)
