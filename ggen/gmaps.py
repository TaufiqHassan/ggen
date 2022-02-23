#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 12:08:42 2022

@author: thassan
"""

from pathlib import Path
from subprocess import run

from ggen.ggrids import get_res, _dir_path

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
    _map_dir = kwargs.get('map_dir', Path('.').absolute())
    _grid_dir = kwargs.get('grid_dir', Path('.').absolute())
    _data_dir = kwargs.get('data_dir', Path('.').absolute())
    _bilin = kwargs.get('bilin', None)
    
    if _map_dir != Path('.').absolute():
        _map_dir = _dir_path()._make_grid_dir()

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
                run(f'ncremap --alg_typ={algo} --src_grd={in_scrip} --dst_grd={out_scrip} --map={_map_dir}/map_{ins}_{outs}.nc'.split(' '),capture_output=True)
                print('\nGenerated map_'+ins+'_'+outs+'.nc mapping file in '+str(_map_dir))
                maps.append(str(_map_dir)+'/'+'map_'+ins+'_'+outs+'.nc')
    return maps


        
    
    
