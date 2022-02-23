#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 16:32:24 2022

@author: thassan
"""

from pathlib import Path
from subprocess import run

from ggen.gmaps import get_maps

def get_rfiles(**kwargs):
    _res = kwargs.get('res', None)
    _file = kwargs.get('file', None)
    _map_dir = kwargs.get('map_dir', Path('.').absolute())
    _grid_dir = kwargs.get('grid_dir', Path('.').absolute())
    _data_dir = kwargs.get('data_dir', Path('.').absolute())
    _bilin = kwargs.get('bilin', None)

    map_list = get_maps(res=_res, file=_file, data_dir=_data_dir,grid_dir=_grid_dir,map_dir=_map_dir,bilin = _bilin)
    for map_file in map_list:
        out_map_tag = map_file.split('/')[-1].split('map_')[1]
        new_file = _file.split('.nc')[0]+'_'+out_map_tag
        run(f'ncremap --map={map_file} {_file} {new_file}'.split(' '),capture_output=True)
        print('\nGenerated remapped '+new_file.split('/')[-1]+' in '+str(_map_dir))

    
    