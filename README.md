## Grid Generator (ggen)

Generates Spectral Element (SE) and Regular Latitude Longitude (RLL) grid meshes and performs conservative remapping between list of meshes with any resolution. Logs are appended to log.ggen. This is part of an emission pre-processor.

Usage
-----

``python ggen/ggen.py -h``
```
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

Installation
------------

Works with e3sm_unifed environment

On compy: `source /share/apps/E3SM/conda_envs/load_latest_e3sm_unified_compy.sh`

On Cori: `source /global/common/software/e3sm/anaconda_envs/load_latest_e3sm_unified_cori-haswell.sh`

For others, use the YAML file provided to create a virtual conda enviroment (genv)

`conda env create -f environment.yml`

And then activate genv to use ggen

`conda activate genv`

Example
-------

### General use (from command line)

```console
python ggen.py -r <output resolutions> -f <input file names> -ind /input/file/directory -out /output/file/directory
```

Example `log.ggen` output

```
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

```console
python ggen.py -r 16,32,180x360 -f "*bc*" -ind /compyfs/inputdata/atm/cam/chem/trop_mozart_aero/emis/DECK_ne120/ -out /compyfs/hass877/e3sm_scratch/ggen_test -mp
```

Example `log.ggen` output

```
Generated ne4pg2 grid in /compyfs/www/hass877/share/emis_data/DECK120_to_SE

Generated ne4pg2 SCRIP file in /compyfs/www/hass877/share/emis_data/DECK120_to_SE

Using fv2fv_flx

Generated map_384x576_ne4pg2.nc mapping file in /compyfs/www/hass877/share/emis_data/DECK120_to_SE

Using fv2fv_flx

Using fv2fv_flx

Using fv2fv_flx

Using fv2fv_flx

Using fv2fv_flx

Using fv2fv_flx

Using fv2fv_flx

Generated remapped cmip6_mam4_num_a2_surf_1850-2014_c20191108_384x576_ne4pg2.nc in /compyfs/www/hass877/share/emis_data/DECK120_to_SE

Generated remapped cmip6_mam4_so4_a1_surf_1850-2014_c20191108_384x576_ne4pg2.nc in /compyfs/www/hass877/share/emis_data/DECK120_to_SE

Generated remapped cmip6_mam4_so4_a2_surf_1850-2014_c20191108_384x576_ne4pg2.nc in /compyfs/www/hass877/share/emis_data/DECK120_to_SE

Generated remapped cmip6_mam4_so2_surf_1850-2014_c20191108_384x576_ne4pg2.nc in /compyfs/www/hass877/share/emis_data/DECK120_to_SE

Generated remapped cmip6_mam4_num_a1_surf_1850-2014_c20191108_384x576_ne4pg2.nc in /compyfs/www/hass877/share/emis_data/DECK120_to_SE

Generated remapped cmip6_mam4_bc_a4_surf_1850-2014_c20191108_384x576_ne4pg2.nc in /compyfs/www/hass877/share/emis_data/DECK120_to_SE

Generated remapped cmip6_mam4_pom_a4_surf_1850-2014_c20191108_384x576_ne4pg2.nc in /compyfs/www/hass877/share/emis_data/DECK120_to_SE

Generated remapped cmip6_mam4_num_a4_surf_1850-2014_c20191108_384x576_ne4pg2.nc in /compyfs/www/hass877/share/emis_data/DECK120_to_SE
Finished in 588.88 second(s)
```
