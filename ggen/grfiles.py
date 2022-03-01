#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 16:32:24 2022

@author: thassan
"""

from pathlib import Path
from subprocess import run

from ggen.gmaps import get_maps
from ggen.gmaps import get_dir_path

def get_rfiles(**kwargs):
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
    if _grid_dir == Path('.').absolute():
        _grid_dir = _data_dir

    map_list = get_maps(res=_res, file=_file, data_dir=_data_dir,grid_dir=_grid_dir,map_dir=_map_dir,bilin = _bilin)
    for map_file in map_list:
        out_map_tag = map_file.split('/')[-1].split('map_')[1]
        new_file = _file.split('.nc')[0]+'_'+out_map_tag
        print(_data_dir,_file,new_file)
        run(f'ncremap --map={map_file} {_file} {_data_dir}/{new_file}'.split(' '),capture_output=True)
        print('\nGenerated remapped '+new_file.split('/')[-1]+' in '+str(_map_dir))

    
    