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

#### Python dependencies
Nanocar builder uses Ångström Python package to assemble molecules.

[**Ångström**](https://github.com/kbsezginel/angstrom)
```
git clone https://github.com/kbsezginel/angstrom.git
cd angstrom
python setup.py install
```

### Usage
If the installation went smoothly you should see a Nanocar entry under Build menu.
Clicking the Nanocar entry would prompt you to select a wheel and a chassis molecule.
After the selection the Nanocar will be built!
