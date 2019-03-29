# Installation

- **[Mac OS X](#mac-os-x)**
- **[Linux](#linux)**

--------------------

## Mac OS X
### [1. Install Avogadro 2](https://www.openchemistry.org/downloads/)
### [2. Configure the Python environment](#configuring-the-python-environment)
### 3. Set the Python environment
We need to help Avogadro find our Python environment.
While the `nanocar` environment is activated type
```
which python
```
and copy the path which should look like `/usr/local/miniconda3/envs/nanocar/bin/python`.

Open Avogadro and go to `Quantum -> Input Generators -> Set Python Path`.
Paste this path here. Now Avogadro knows which Python to use for our plug-in!

### 4. Install the Nanocar builder plug-in
Lastly, we need to install our plug-in. For Mac, the plug-ins directory will be present at
`Applications -> Avogadro2.app -> Contents -> lib -> avogadro2 -> scripts`.
Copy the path for this directory which should look like
`/Applications/Avogadro2.app/Contents/lib/avogadro2/scripts`.
Enter the `nanocar-avogadro` repository and run the installer Python script:
```
python install_plugin.py /Applications/Avogadro2.app/Contents/lib/avogadro2/scripts
```
Congratulations! Now you should see the `Nanocar` option under `Build` in Avogadro.

### Notes
If you are planning to use other plug-ins make sure to install their dependencies
to the same Python environment. Currently, Avogadro uses the same Python environment
for all the plug-ins.

For debugging purposes you can run Avogadro from the command line:
```
cd /Applications/Avogadro2.app/Contents/MacOS
./Avogadro2
```

*Last tested: March 28, 2019 on MacOS Mojave 10.14.2 (18C54)*

--------------------

## Linux
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
### 3. Set the Python environment
We need to help Avogadro find our Python environment.
While the `nanocar` environment is activated type
```
which python
```
and copy the path which should look something like
`/home/<username>/miniconda3/envs/nanocar/bin/python`.

Open Avogadro and go to `Quantum -> Input Generators -> Set Python Path`.
Paste this path here. Now Avogadro knows which Python to use for our plug-in!

### 4. Install the Nanocar builder plug-in
Lastly, we need to install our plug-in. For linux the plug-ins directory should
be under `/home/<username>/.local/share/OpenChemistry/Avogadro` where
`<username>` is your username. Copy that path and run the Python installer:
```
python install_plugin.py /home/<username>/.local/share/OpenChemistry/Avogadro
```
Congratulations! Now you should see the `Nanocar` option under `Build` in Avogadro.

### Notes
If you are planning to use other plug-ins make sure to install their dependencies
to the same Python environment. Currently, Avogadro uses the same Python environment
for all the plug-ins.

*Last tested: Oct 8, 2018 on Ubuntu 16.08*

----------------------

## Configuring the Python environment
1. Install miniconda for Python >= 3.6 [here](https://docs.conda.io/en/latest/miniconda.html).

2. Create a new environment in conda.
```
conda create -n nanocar python=3.6
```
Activate the environment:
```
conda activate nanocar
```
Depending on your conda installation / system you might need to use:
```
source activate nanocar
```

3. Clone the `nanocar-avogadro` repository:
```
git clone https://github.com/kbsezginel/nanocar-avogadro.git
cd nanocar-avogadro
```

4. Install requirements:
```
pip install -r requirements.txt
```
