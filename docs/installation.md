# Installation

- **[Mac OS X](#mac-os-x)**
- **[Linux](#linux-ubuntu)**
- **[Windows](#windows)**

--------------------

## Mac OS X
### [1. Install Avogadro 2](https://www.openchemistry.org/downloads/)
### [2. Configure the Python environment](#configuring-the-python-environment)
### 3. Install Nanocar plug-in
Clone the `nanocar-avogadro` repository:
```
git clone https://github.com/kbsezginel/nanocar-avogadro.git
cd nanocar-avogadro
```
Find the Avogadro2 plug-ins directory. For Mac, the plug-ins directory will be present at `Applications -> Avogadro2.app -> Contents -> lib -> avogadro2 -> scripts -> workflows`. Copy the path for this directory and then run the installer Python script:
```
python install_plugin.py /path/to/the/plugin/directory
```
Now you should see the `Nanocar` option under `Build` in Avogadro.

--------------------

## Linux (Ubuntu)
### 1. Install Avogadro 2
First build Avogadro 2 from the [openchemistry supermodule](https://github.com/OpenChemistry/openchemistry).
```
git clone https://github.com/OpenChemistry/openchemistry.git
mkdir openchemistry-build
cd openchemistry-build
cmake ../openchemistry
cmake --build . --config Release
```
More build and updating instructions can be found [here](http://wiki.openchemistry.org/Build).

### [2. Configure the Python environment](#configuring-the-python-environment)

### 3. Install Nanocar plug-in
Clone the `nanocar-avogadro` repository:
```
git clone https://github.com/kbsezginel/nanocar-avogadro.git
cd nanocar-avogadro
```
Find your plug-in directory. It should be under `/home/<username>/.local/share/OpenChemistry/Avogadro` where `<username>` is your username. Copy that path and run the Python installer:
```
python install_plugin.py /home/<username>/.local/share/OpenChemistry/Avogadro
```
Now you should see the `Nanocar` option under `Build` in Avogadro.

--------------------

## Windows
### 1. Install Avogadro 2
### [2. Configure the Python environment](#configuring-the-python-environment)
### 3. Install Nanocar plug-in

----------------------

## Configuring the Python environment
1. Install conda [here](https://conda.io/docs/user-guide/install/index.html#regular-installation).

2. Create a new environment in conda.
```
conda create -n nanocar python=3.5
```
Activate the environment:
```
conda activate nanocar
```
Depending on your conda installation you might need to use:
```
source activate nanocar
```

3. Install **[Ångström](https://github.com/kbsezginel/angstrom)** Python package.
```
git clone https://github.com/kbsezginel/angstrom.git
cd angstrom
python setup.py install
```

4. If you would like to use the surface builder you also need to install [ase](https://wiki.fysik.dtu.dk/ase/):
```
conda install -c conda_forge ase
```

5. The Python path must be set in Avogadro2 to the environment which contains the installed python dependencies. Using conda (while the `nanocar` environment is activated) you can find the Python path by:
```
which python
```
This should return a path like `/home/<username>/anaconda3/envs/nanocar/bin/python`. Copy the path for your environment. In Avogadro2, access the Python Path variable under `Quantum -> Input Generators -> Set Python Path` and paste it here.
