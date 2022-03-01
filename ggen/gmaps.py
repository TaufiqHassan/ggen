#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 12:08:42 2022

@author: thassan
"""

from pathlib import Path
from subprocess import run
import os

from ggen.ggrids import get_res, get_dir_path

def get_algo(in_scrip, out_scrip, bilin=None):
    if bilin == None:
        if ('x' in in_scrip.split('/')[-1]) and ('np4' in out_scrip.split('/')[-1]):
            algo = 'fv2se_flx'
        else:
            algo = 'fv2fv_flx'
    else:
        print('\nNOTE: Applying bilinear interpolation')
        algo='bilinear'
    return algo


def get_maps(**kwargs):
    _res = kwargs.get('res', None)
    _file = kwargs.get('file', None)
    _map_dir = kwargs.get('map_dir', None)
    _grid_dir = kwargs.get('grid_dir', None)
    _data_dir = kwargs.get('data_dir', None)
    _bilin = kwargs.get('bilin', None)
    
    _data_dir=get_dir_path(_data_dir,'data')
    _grid_dir=get_dir_path(_grid_dir,'grid')
    _map_dir=get_dir_path(_map_dir,'map')
    if _map_dir == Path('.').absolute():
        _map_dir = _data_dir

    gscrip = get_res(data_dir=_data_dir,grid_dir=_grid_dir,map_dir=_map_dir)
    
    try:
        gscrip.res = _res
    except:
        print('\nYou must put a resolution value.')
        print('\nExample: 30, 16, 30pg2 etc.')
        
    try:
        gscrip.file = _file
    except:
        print('\nYou must provide a file name.')
    
    gscrip._bilin = _bilin    
        
    list_in = gscrip.get_in_scrip()
    list_out = gscrip.get_out_scrip()
    
    maps = []

    for in_scrip in list_in:
        for out_scrip in list_out:
            ins=in_scrip.split('/')[-1].split('_')[0]
            outs=out_scrip.split('/')[-1].split('_')[0]
            algo = get_algo(in_scrip, out_scrip, bilin = _bilin)
            print('\nUsing '+algo)
            if algo == 'bilinear':
                run(f'ncremap --alg_typ={algo} --src_grd={in_scrip} --dst_grd={out_scrip} --map={_map_dir}/map_{ins}_{outs}_bl.nc'.split(' '),capture_output=True)
                print('\nGenerated map_'+ins+'_'+outs+'_bl.nc mapping file in '+str(_map_dir))
                maps.append(str(_map_dir)+'/'+'map_'+ins+'_'+outs+'_bl.nc')
            else:
                if not os.path.exists(str(_map_dir)+'/'+'map_'+ins+'_'+outs+'.nc'):
                    run(f'ncremap --alg_typ={algo} --src_grd={in_scrip} --dst_grd={out_scrip} --map={_map_dir}/map_{ins}_{outs}.nc'.split(' '),capture_output=True)
                    print('\nGenerated map_'+ins+'_'+outs+'.nc mapping file in '+str(_map_dir))
                    maps.append(str(_map_dir)+'/'+'map_'+ins+'_'+outs+'.nc')
                else:
                    maps.append(str(_map_dir)+'/'+'map_'+ins+'_'+outs+'.nc')
    return maps


        
    
    
