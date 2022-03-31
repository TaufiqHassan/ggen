#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 16:32:24 2022

@author: thassan
"""

from pathlib import Path
import xarray as xr
import numpy as np
import os
import logging

from ggen.gmaps import get_maps
from ggen.ggrids import get_res
from ggen.utils import get_dir_path, exec_shell

def get_rfiles(**kwargs):
    _res = kwargs.get('res', None)
    _file = kwargs.get('file', None)
    _map_dir = kwargs.get('map_dir', None)
    _grid_dir = kwargs.get('grid_dir', None)
    _data_dir = kwargs.get('data_dir', None)
    _bilin = kwargs.get('bilin', None)
    _grid = kwargs.get('grid', None)
    _sdim = kwargs.get('sdim', None)
    
    _data_dir=get_dir_path(_data_dir,'data')
    _grid_dir=get_dir_path(_grid_dir,'grid')
    _map_dir=get_dir_path(_map_dir,'map')
    if _map_dir == Path('.').absolute():
        _map_dir = _data_dir
    if _grid_dir == Path('.').absolute():
        _grid_dir = _data_dir

    gscrip = get_res()
    gscrip.file = _file
    file_list = gscrip._file
    
    map_list = get_maps(res=_res, file=_file, data_dir=_data_dir,grid_dir=_grid_dir,map_dir=_map_dir,bilin = _bilin,grid=_grid)
    for f in file_list:
        for map_file in map_list:
            out_map_tag = map_file.split('/')[-1].split('map_')[1]
            new_file = f.split('.nc')[0]+'_'+out_map_tag
            if not os.path.exists(str(_data_dir)+'/'+new_file.split('/')[-1]):
                exec_shell(f'ncremap --map={map_file} {f} {_data_dir}/{new_file}')
                print('\nGenerated remapped '+new_file.split('/')[-1]+' in '+str(_data_dir))
            else:
                logger = logging.getLogger(str(_data_dir)+'/log.ggen')
                logger.info('\n'+str(_data_dir)+'/'+new_file.split('/')[-1]+' already exists.')
            if _sdim!=None:
                logger = logging.getLogger(str(_data_dir)+'/log.ggen')
                logger.info('\nAdding a singleton dim: altitude.')
                lev=np.array([1e5])
                data=xr.open_dataset(str(_data_dir)+'/'+new_file.split('/')[-1])
                data1=data.expand_dims('altitude',axis=1)
                data2 = data1.assign_coords(altitude=('altitude',lev))
                data3=data2
                data3['lon_vertices']=data2['lon_vertices'].sel(altitude=1e5).drop('altitude')
                data3['lat_vertices']=data2['lat_vertices'].sel(altitude=1e5).drop('altitude')
                data3['area']=data2['area'].sel(altitude=1e5).drop('altitude')
                data3.load().to_netcdf(str(_data_dir)+'/'+new_file.split('/')[-1].split('.nc')[0]+'_lev.nc')




    
    