#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 17:43:42 2022

@author: thassan
"""

import time
import argparse
import logging
from ggen.grfiles import get_rfiles

def main():

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-r", help="Resolutions (e.g. 4, 16, 30, 30pg2)", required=True)
    parser.add_argument("-f", help="File Names (input netcdf file names). Use ' ' when using wildcards.", required=True)
    parser.add_argument("-bl", help="Select bilinear interpolation", action='store_true', default=None)
    parser.add_argument("-m", help="Maps directory.", default=None)
    parser.add_argument("-g", help="Grids directory.", default=None)
    parser.add_argument("-d", help="Data directory.", default=None)
    parser.add_argument("-gf", help="Insert grid file.", default=None)
    parser.add_argument("-mf", help="Insert map file.", default=None)
    parser.add_argument("-sd", help="Add a sigleton dim.",action='store_true', default=None)
    parser.add_argument("-mp", help="Multiprocessing",action='store_true', default=None)
    
    args = parser.parse_args()
    res = args.r
    file = args.f
    bl = args.bl
    m_dir = args.m
    g_dir = args.g
    d_dir = args.d
    grid_file = args.gf
    map_file = args.mf
    sdim = args.sd
    mp = args.mp
    
    logging.basicConfig(filename=str(d_dir)+'/log.ggen', force=True, level=logging.INFO, format='%(message)s')

    start = time.perf_counter()
    
    get_rfiles(res=res, file=file, data_dir=d_dir,grid_dir=g_dir,map_dir=m_dir,bilin = bl,grid=grid_file,mapfile=map_file,sdim=sdim,mp=mp)

    finish = time.perf_counter()

    logging.info(f'\nFinished in {round(finish-start, 2)} second(s)')
    logging.info('\n################################## Process Finished ##################################')
    logging.info('######################################################################################\n')
    
    print(f'Finished in {round(finish-start, 2)} second(s)')
    

