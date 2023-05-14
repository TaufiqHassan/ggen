## Grid Generator (ggen)

Generates Spectral Element (SE) and Regular Latitude Longitude (RLL) grid meshes and performs conservative remapping between list of meshes. Works with `tempestremap` and `nco` under the hood. Logs are appended to log.ggen.

Usage
-----

```console
python ggen.py -h
```
```bash
usage: ggen.py [-h] [-r R] [-f F] [-ind IND] [-out OUT] [-gf GF] [-mf MF]
               [-sd] [-scrip] [-mp] [-ir IR]

optional arguments:
  -h, --help  show this help message and exit
  -r R        Output resolutions (e.g. 16, 30, 64x128, 180x360)
  -f F        File Names (input netcdf file names). Use ' ' when using
              wildcards.
  -ind IND    Input directory (current directory is default).
  -out OUT    Output directory (current directory is default).
  -gf GF      Insert grid file.
  -mf MF      Insert map file.
  -sd         Add a sigleton lev dim.
  -scrip      Generate SCRIP files
  -mp         Multiprocessing
  -ir IR      Input resolutions (e.g. 16, 30, 64x128, 180x360)
```

General Structure
-----------------

![ggen schematic](./ggen.png)

Installation
------------

Works with e3sm_unifed environment

On compy: 
```bash
source /share/apps/E3SM/conda_envs/load_latest_e3sm_unified_compy.sh
```

On Cori: 
```bash
source /global/common/software/e3sm/anaconda_envs/load_latest_e3sm_unified_cori-haswell.sh
```

For others, use the YAML file provided to create a virtual conda enviroment (genv)

`conda env create -f environment.yml`

And then activate genv to use ggen

`conda activate genv`

Examples
--------

### General use (from command line)

```bash
python ggen.py -r <output resolutions> -f <input file names> -ind /input/file/directory -out /output/file/directory
```

Example `log.ggen` output

```bash
################################## Process Started ##################################

[cmd]: python ggen.py -r 30 -f bc_emission_def.nc -ind /Users/hass877/Work/data_analysis -out /Users/hass877/Work/data_analysis


=== driver init done ===

Specifying input file suppresses resolution.
(Recommended for SE to RLL conversion)

Generating RLL grid metadata

Creating SCRIP file RLL180x360_SCRIP.nc in /Users/hass877/Work/data_analysis

Generated /Users/hass877/Work/data_analysis/RLL180x360_SCRIP.nc

Generated /Users/hass877/Work/data_analysis/RLL180x360_SCRIP.nc

Output Resolution: 30

Generating exodus metadata

Generating pg2 metadata

Creating SCRIP file ne30pg2_SCRIP.nc in /Users/hass877/Work/data_analysis

Generated /Users/hass877/Work/data_analysis/ne30pg2_SCRIP.nc

Generated /Users/hass877/Work/data_analysis/ne30pg2_SCRIP.nc

=== gen_scrips done ===

Input SCRIP:/Users/hass877/Work/data_analysis/RLL180x360_SCRIP.nc
Output SCRIP:/Users/hass877/Work/data_analysis/ne30pg2_SCRIP.nc

[cmd]: ncremap --alg_typ=fv2fv_flx --src_grd=/Users/hass877/Work/data_analysis/RLL180x360_SCRIP.nc --dst_grd=/Users/hass877/Work/data_analysis/ne30pg2_SCRIP.nc --map=/Users/hass877/Work/data_analysis/map_RLL180x360_ne30pg2.nc

Grid(src): /Users/hass877/Work/data_analysis/RLL180x360_SCRIP.nc
Grid(dst): /Users/hass877/Work/data_analysis/ne30pg2_SCRIP.nc


Generated map_RLL180x360_ne30pg2.nc mapping file in /Users/hass877/Work/data_analysis

=== gen_weights done ===

Applying /Users/hass877/Work/data_analysis/map_RLL180x360_ne30pg2.nc on /Users/hass877/Work/data_analysis/bc_emission_def.nc

[cmd]: ncremap --map=/Users/hass877/Work/data_analysis/map_RLL180x360_ne30pg2.nc /Users/hass877/Work/data_analysis/bc_emission_def.nc /Users/hass877/Work/data_analysis/bc_emission_def_RLL180x360_ne30pg2.nc

Input #00: /Users/hass877/Work/data_analysis/bc_emission_def.nc
Map/Wgt  : /Users/hass877/Work/data_analysis/map_RLL180x360_ne30pg2.nc


Generated remapped file /Users/hass877/Work/data_analysis/bc_emission_def_RLL180x360_ne30pg2.nc

=== apply_weights done ===

=== gen_remapped_files done ===

Finished in 4.17 second(s)

################################## Process Finished ##################################
######################################################################################
```

### Using muliprocessing and wildcards

```bash
python ggen.py -r 16,32,180x360 -f "*bc*" -ind /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/ -out /compyfs/hass877/e3sm_scratch/ggen_test -mp
```

<details><summary>Click to view long log file</summary>
<p>

#### log.ggen output

```bash
################################## Process Started ##################################

[cmd]: python ggen.py -r 16,32,180x360 -f *bc* -ind /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/ -out /compyfs/hass877/e3sm_scratch/ggen_test -mp


=== driver init done ===

Specifying input file suppresses resolution.
(Recommended for SE to RLL conversion)

Generating RLL grid metadata

Creating SCRIP file RLL384x576_SCRIP.nc in /compyfs/hass877/e3sm_scratch/ggen_test

Generated /compyfs/hass877/e3sm_scratch/ggen_test/RLL384x576_SCRIP.nc

Generated /compyfs/hass877/e3sm_scratch/ggen_test/RLL384x576_SCRIP.nc

Specifying input file suppresses resolution.
(Recommended for SE to RLL conversion)
/compyfs/hass877/e3sm_scratch/ggen_test/RLL384x576_SCRIP.nc already exists!
 Using it.

Generated /compyfs/hass877/e3sm_scratch/ggen_test/RLL384x576_SCRIP.nc

Output Resolution: 16

Generating exodus metadata

Generating pg2 metadata

Creating SCRIP file ne16pg2_SCRIP.nc in /compyfs/hass877/e3sm_scratch/ggen_test

Generated /compyfs/hass877/e3sm_scratch/ggen_test/ne16pg2_SCRIP.nc

Generated /compyfs/hass877/e3sm_scratch/ggen_test/ne16pg2_SCRIP.nc

Output Resolution: 32

Generating exodus metadata

Generating pg2 metadata

Creating SCRIP file ne32pg2_SCRIP.nc in /compyfs/hass877/e3sm_scratch/ggen_test

Generated /compyfs/hass877/e3sm_scratch/ggen_test/ne32pg2_SCRIP.nc

Generated /compyfs/hass877/e3sm_scratch/ggen_test/ne32pg2_SCRIP.nc

Output Resolution: 180x360

Generating RLL grid metadata

Creating SCRIP file RLL180x360_SCRIP.nc in /compyfs/hass877/e3sm_scratch/ggen_test

Generated /compyfs/hass877/e3sm_scratch/ggen_test/RLL180x360_SCRIP.nc

Generated /compyfs/hass877/e3sm_scratch/ggen_test/RLL180x360_SCRIP.nc

=== gen_scrips done ===

Input SCRIP:/compyfs/hass877/e3sm_scratch/ggen_test/RLL384x576_SCRIP.nc
Output SCRIP:/compyfs/hass877/e3sm_scratch/ggen_test/ne16pg2_SCRIP.nc

[cmd]: ncremap --alg_typ=fv2fv_flx --src_grd=/compyfs/hass877/e3sm_scratch/ggen_test/RLL384x576_SCRIP.nc --dst_grd=/compyfs/hass877/e3sm_scratch/ggen_test/ne16pg2_SCRIP.nc --map=/compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne16pg2.nc

Grid(src): /compyfs/hass877/e3sm_scratch/ggen_test/RLL384x576_SCRIP.nc
Grid(dst): /compyfs/hass877/e3sm_scratch/ggen_test/ne16pg2_SCRIP.nc


Generated map_RLL384x576_ne16pg2.nc mapping file in /compyfs/hass877/e3sm_scratch/ggen_test

Input SCRIP:/compyfs/hass877/e3sm_scratch/ggen_test/RLL384x576_SCRIP.nc
Output SCRIP:/compyfs/hass877/e3sm_scratch/ggen_test/ne32pg2_SCRIP.nc

[cmd]: ncremap --alg_typ=fv2fv_flx --src_grd=/compyfs/hass877/e3sm_scratch/ggen_test/RLL384x576_SCRIP.nc --dst_grd=/compyfs/hass877/e3sm_scratch/ggen_test/ne32pg2_SCRIP.nc --map=/compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne32pg2.nc

Grid(src): /compyfs/hass877/e3sm_scratch/ggen_test/RLL384x576_SCRIP.nc
Grid(dst): /compyfs/hass877/e3sm_scratch/ggen_test/ne32pg2_SCRIP.nc


Generated map_RLL384x576_ne32pg2.nc mapping file in /compyfs/hass877/e3sm_scratch/ggen_test

Input SCRIP:/compyfs/hass877/e3sm_scratch/ggen_test/RLL384x576_SCRIP.nc
Output SCRIP:/compyfs/hass877/e3sm_scratch/ggen_test/RLL180x360_SCRIP.nc

[cmd]: ncremap --alg_typ=fv2fv_flx --src_grd=/compyfs/hass877/e3sm_scratch/ggen_test/RLL384x576_SCRIP.nc --dst_grd=/compyfs/hass877/e3sm_scratch/ggen_test/RLL180x360_SCRIP.nc --map=/compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_RLL180x360.nc

Grid(src): /compyfs/hass877/e3sm_scratch/ggen_test/RLL384x576_SCRIP.nc
Grid(dst): /compyfs/hass877/e3sm_scratch/ggen_test/RLL180x360_SCRIP.nc


Generated map_RLL384x576_RLL180x360.nc mapping file in /compyfs/hass877/e3sm_scratch/ggen_test

=== gen_weights done ===

Applied multiprocessing.

Applied multiprocessing.

Applying /compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne16pg2.nc on /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_elev_1850-2014_c20191108.nc

[cmd]: ncremap --map=/compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne16pg2.nc /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_elev_1850-2014_c20191108.nc /compyfs/hass877/e3sm_scratch/ggen_test/cmip6_mam4_bc_a4_elev_1850-2014_c20191108_RLL384x576_ne16pg2.nc


Applied multiprocessing.

Applying /compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne16pg2.nc on /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_surf_1850-2014_c20191108.nc

[cmd]: ncremap --map=/compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne16pg2.nc /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_surf_1850-2014_c20191108.nc /compyfs/hass877/e3sm_scratch/ggen_test/cmip6_mam4_bc_a4_surf_1850-2014_c20191108_RLL384x576_ne16pg2.nc


Applied multiprocessing.

Applying /compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne32pg2.nc on /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_elev_1850-2014_c20191108.nc

[cmd]: ncremap --map=/compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne32pg2.nc /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_elev_1850-2014_c20191108.nc /compyfs/hass877/e3sm_scratch/ggen_test/cmip6_mam4_bc_a4_elev_1850-2014_c20191108_RLL384x576_ne32pg2.nc


Applied multiprocessing.

Applying /compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne32pg2.nc on /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_surf_1850-2014_c20191108.nc

[cmd]: ncremap --map=/compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne32pg2.nc /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_surf_1850-2014_c20191108.nc /compyfs/hass877/e3sm_scratch/ggen_test/cmip6_mam4_bc_a4_surf_1850-2014_c20191108_RLL384x576_ne32pg2.nc


Applied multiprocessing.

Applying /compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_RLL180x360.nc on /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_elev_1850-2014_c20191108.nc

[cmd]: ncremap --map=/compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_RLL180x360.nc /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_elev_1850-2014_c20191108.nc /compyfs/hass877/e3sm_scratch/ggen_test/cmip6_mam4_bc_a4_elev_1850-2014_c20191108_RLL384x576_RLL180x360.nc


Applying /compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_RLL180x360.nc on /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_surf_1850-2014_c20191108.nc

[cmd]: ncremap --map=/compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_RLL180x360.nc /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_surf_1850-2014_c20191108.nc /compyfs/hass877/e3sm_scratch/ggen_test/cmip6_mam4_bc_a4_surf_1850-2014_c20191108_RLL384x576_RLL180x360.nc

Input #00: /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_surf_1850-2014_c20191108.nc
Map/Wgt  : /compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne16pg2.nc


Generated remapped file /compyfs/hass877/e3sm_scratch/ggen_test/cmip6_mam4_bc_a4_surf_1850-2014_c20191108_RLL384x576_ne16pg2.nc

=== apply_weights done ===
Input #00: /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_surf_1850-2014_c20191108.nc
Map/Wgt  : /compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne32pg2.nc


Generated remapped file /compyfs/hass877/e3sm_scratch/ggen_test/cmip6_mam4_bc_a4_surf_1850-2014_c20191108_RLL384x576_ne32pg2.nc

=== apply_weights done ===
Input #00: /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_surf_1850-2014_c20191108.nc
Map/Wgt  : /compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_RLL180x360.nc


Generated remapped file /compyfs/hass877/e3sm_scratch/ggen_test/cmip6_mam4_bc_a4_surf_1850-2014_c20191108_RLL384x576_RLL180x360.nc

=== apply_weights done ===
Input #00: /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_elev_1850-2014_c20191108.nc
Map/Wgt  : /compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne16pg2.nc


Generated remapped file /compyfs/hass877/e3sm_scratch/ggen_test/cmip6_mam4_bc_a4_elev_1850-2014_c20191108_RLL384x576_ne16pg2.nc

=== apply_weights done ===
Input #00: /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_elev_1850-2014_c20191108.nc
Map/Wgt  : /compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_ne32pg2.nc


Generated remapped file /compyfs/hass877/e3sm_scratch/ggen_test/cmip6_mam4_bc_a4_elev_1850-2014_c20191108_RLL384x576_ne32pg2.nc

=== apply_weights done ===
Input #00: /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/cmip6_mam4_bc_a4_elev_1850-2014_c20191108.nc
Map/Wgt  : /compyfs/hass877/e3sm_scratch/ggen_test/map_RLL384x576_RLL180x360.nc


Generated remapped file /compyfs/hass877/e3sm_scratch/ggen_test/cmip6_mam4_bc_a4_elev_1850-2014_c20191108_RLL384x576_RLL180x360.nc

=== apply_weights done ===

=== gen_remapped_files done ===

Finished in 348.79 second(s)

################################## Process Finished ##################################
######################################################################################
```

</p>
</details>

### Submit as a batch job

Example batch script

```bash
#!/bin/bash -l
#SBATCH --job-name=ggen
#SBATCH --output=ggen.o%j
#SBATCH --account=project
#SBATCH --nodes=1
#SBATCH --time=00:30:00
#SBATCH --partition=short

source /share/apps/E3SM/conda_envs/load_latest_e3sm_unified_compy.sh
python ggen.py -r 16,32,180x360 -f "*bc*" -ind /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/ -out /compyfs/hass877/e3sm_scratch/ggen_test -mp
```

### References

<a id="1">[1]</a> 
Ullrich, Paul A and Taylor, Mark A (2015). 
Arbitrary-order conservative and consistent remapping and a theory of linear maps: Part I. 
Monthly Weather Review, 143, 2419-2440.

<a id="2">[2]</a> 
Ullrich, Paul A and Devendran, Dharshi and Johansen, Hans (2016). 
Arbitrary-order conservative and consistent remapping and a theory of linear maps: Part II.
Monthly Weather Review, 144, 1529-1549.

<a id="3">[3]</a> 
Zender, Charles S (2008). 
Analysis of self-describing gridded geoscience data with netCDF Operators (NCO).
Environmental Modelling & Software, 23, 1338-1342
