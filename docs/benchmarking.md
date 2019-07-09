# Rigid MD

# Multibody Rigid MD

### Procedure
- Add chassis (H2)
- Delete capping H atoms (12 total)
- Add wheel
  - Append: checked
  - Bond distance: 1.2 A
  - Refresh Wheel List: checked
  - Wheel: C60
- Repeat for all wheels uncheck *Refresh Wheel List*
- Metal surface
  - Lattice constant: 4 A
  - Metal: Au
  - Orthogonal: True
  - Size X: 25
  - Size Y: 35
  - Size Z: 5
  - Surface: fcc110
  - Vacuum distance: 10 A
- LAMMPS setup
  - X: 10.0 nm
  - Y: 9.9 nm
  - Z: 3.0 nm
  - Multibody: checked
  - Simulation length: 1.0 ns
  - Timestep: 1.0 fs
