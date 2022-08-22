#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 12:08:42 2022

@author: thassan
"""

from pathlib import Path
import os
import logging

from ggen.ggrids import get_res
from ggen.utils import get_dir_path, exec_shell

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
    _grid = kwargs.get('grid', None)
    mapfile = kwargs.get('mapfile', None)
    
    _data_dir=get_dir_path(_data_dir,'data')
    _grid_dir=get_dir_path(_grid_dir,'grid')
    _map_dir=get_dir_path(_map_dir,'map')
    if _map_dir == Path('.').absolute():
        _map_dir = _data_dir

    if mapfile == None:
        gscrip = get_res(data_dir=_data_dir,grid_dir=_grid_dir,map_dir=_map_dir,grid=_grid)
        
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
                    exec_shell(f'ncremap --alg_typ={algo} --src_grd={in_scrip} --dst_grd={out_scrip} --map={_map_dir}/map_{ins}_{outs}_bl.nc')
                    print('\nGenerated map_'+ins+'_'+outs+'_bl.nc mapping file in '+str(_map_dir))
                    maps.append(str(_map_dir)+'/'+'map_'+ins+'_'+outs+'_bl.nc')
                else:
                    if not os.path.exists(str(_map_dir)+'/'+'map_'+ins+'_'+outs+'.nc'):
                        exec_shell(f'ncremap --alg_typ={algo} --src_grd={in_scrip} --dst_grd={out_scrip} --map={_map_dir}/map_{ins}_{outs}.nc')
                        print('\nGenerated map_'+ins+'_'+outs+'.nc mapping file in '+str(_map_dir))
                        maps.append(str(_map_dir)+'/'+'map_'+ins+'_'+outs+'.nc')
                    else:
                        logger = logging.getLogger(str(_data_dir)+'/log.ggen')
                        logger.info('\n'+str(_map_dir)+'/'+'map_'+ins+'_'+outs+'.nc already exists.\nUsing it!')
                        maps.append(str(_map_dir)+'/'+'map_'+ins+'_'+outs+'.nc')
    else:
        print("\nApplying map file.\n")
        maps = mapfile.strip().split(',')
        
    return maps


        
    
    
