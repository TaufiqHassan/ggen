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
