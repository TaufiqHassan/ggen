import time
import argparse
import logging
import sys

from ggen.driver_mod import driver
from ggen.gen_scrip_file import gen_scrip

def main():
    '''
    Created to produce a command line interface (CLI).
    Takes and parses arguments from user and uses those
    to initiate the driver class in gen_files.py

    '''

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-r", help="Output resolutions (e.g. 16, 30, 64x128, 180x360)", default=None)
    parser.add_argument("-f", help="File Names (input netcdf file names). Use ' ' when using wildcards.")
    parser.add_argument("-ind", help="Input directory (current directory is default).", default=None)
    parser.add_argument("-out", help="Output directory (current directory is default).", default=None)
    parser.add_argument("-gf", help="Insert grid file.", default=None)
    parser.add_argument("-mf", help="Insert map file.", default=None)
    parser.add_argument("-sd", help="Add a sigleton lev dim.",action='store_true', default=None)
    parser.add_argument("-scrip", help="Generate SCRIP files",action='store_true', default=None)
    parser.add_argument("-mp", help="Multiprocessing",action='store_true', default=None)
    parser.add_argument("-ir", help="Input resolutions (e.g. 16, 30, 64x128, 180x360)", default=None)
    
    args = parser.parse_args()
    res = args.r
    file = args.f
    indir = args.ind
    outdir = args.out
    grid_file = args.gf
    map_file = args.mf
    sdim = args.sd
    mp = args.mp
    scrip = args.scrip
    in_res = args.ir
    
    logging.basicConfig(filename=str(outdir)+'/log.ggen', level=logging.INFO, format='%(message)s')

    start = time.perf_counter()
    
    logging.info('\n################################## Process Started ##################################')
    
    cmd = " ".join(sys.argv)
    logging.info('\n[cmd]: python ' + cmd+ '\n')
    
    if scrip:
        gen_scrip(res=res, file=file, path=outdir, fdir=indir, grid=grid_file, nc=True).get_scrip_file()
    else:
        driver(res=res, file=file, ind=indir, out=outdir, grid=grid_file, mapfile=map_file, sdim=sdim, mp=mp, ires=in_res).gen_remapped_files()

    finish = time.perf_counter()

    logging.info(f'\nFinished in {round(finish-start, 2)} second(s)')
    logging.info('\n################################## Process Finished ##################################')
    logging.info('######################################################################################\n')
    
    print(f'\nFinished in {round(finish-start, 2)} second(s)')
    

