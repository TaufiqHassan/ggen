## ggen

Generate grids and remap to SE at any resolution.

### Usage

`python ggen/ggen.py -h`
```
usage: ggen.py [-h] -r R -f F [-bl] [-m M] [-g G] [-d D] [-gf GF] [-sd] [-mp]

optional arguments:
  -h, --help  show this help message and exit
  -r R        Resolutions (e.g. 4, 16, 30, 30pg2)
  -f F        File Names (input netcdf file names). Use ' ' when using wildcards.
  -bl         Select bilinear interpolation
  -m M        Maps directory.
  -g G        Grids directory.
  -d D        Data directory.
  -gf GF      Insert grid file.
  -sd         Add a sigleton dim.
  -mp         Multiprocessing
```

### Installation

Use the yml file provided to create a virtual conda enviroment (genv)

`conda env create -f environment.yml`

And then activate genv to use ggen

`conda activate genv`

### Example

General use

`python ../ggen/ggen.py -r 30pg2,16pg2,4pg2 -f cmip6_mam4_bc_a4_surf_1850_c20191108.nc -d /Users/hass877/Work/data_analysis`
```
Generated ne30pg2 grid in /Users/hass877/Work/data_analysis

Generated ne30pg2 SCRIP file in /Users/hass877/Work/data_analysis

Generated ne16pg2 grid in /Users/hass877/Work/data_analysis

Generated ne16pg2 SCRIP file in /Users/hass877/Work/data_analysis

Generated ne4pg2 grid in /Users/hass877/Work/data_analysis

Generated ne4pg2 SCRIP file in /Users/hass877/Work/data_analysis

Using fv2fv_flx

Using fv2fv_flx

Generated map_384x576_ne16pg2.nc mapping file in /Users/hass877/Work/data_analysis

Using fv2fv_flx

Generated map_384x576_ne4pg2.nc mapping file in /Users/hass877/Work/data_analysis

Generated remapped cmip6_mam4_bc_a4_surf_1850_c20191108_384x576_ne30pg2.nc in /Users/hass877/Work/data_analysis

Generated remapped cmip6_mam4_bc_a4_surf_1850_c20191108_384x576_ne16pg2.nc in /Users/hass877/Work/data_analysis

Generated remapped cmip6_mam4_bc_a4_surf_1850_c20191108_384x576_ne4pg2.nc in /Users/hass877/Work/data_analysis
Finished in 14.99 second(s)
```
