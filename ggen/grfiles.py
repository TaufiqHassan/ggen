#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 16:32:24 2022

@author: hass877
"""

from pathlib import Path
import xarray as xr
import numpy as np
import os
import logging
import multiprocessing as mp

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
    _mp = kwargs.get('mp', None)
    mapfile = kwargs.get('mapfile', None)
    
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
    
    map_list = get_maps(res=_res, file=_file, data_dir=_data_dir,grid_dir=_grid_dir, \
                        map_dir=_map_dir,bilin = _bilin,grid=_grid, mapfile=mapfile)

    file_list = list(set(file_list))
    map_list = list(set(map_list))

    def get_files(map_file,f,_data_dir,new_file,_sdim):
        if not os.path.exists(str(_data_dir)+'/'+new_file.split('/')[-1]):
            exec_shell(f'ncremap --map={map_file} {f} {_data_dir}/{new_file}')
            print('\nGenerated remapped '+new_file.split('/')[-1]+' in '+str(_data_dir))
        else:
            logger = logging.getLogger(str(_data_dir)+'/log.ggen')
            logger.info('\n'+str(_data_dir)+'/'+new_file.split('/')[-1]+' already exists.')
        if _sdim!=None:
            logger = logging.getLogger(str(_data_dir)+'/log.ggen')
            logger.info('\nAdding a singleton dim: lev.')
            lev=np.array([1e5])
            data=xr.open_dataset(str(_data_dir)+'/'+new_file.split('/')[-1])
            data1=data.expand_dims('lev',axis=1)
            data2 = data1.assign_coords(lev=('lev',lev))
            data2.load().to_netcdf(str(_data_dir)+'/'+new_file.split('/')[-1].split('.nc')[0]+'_lev.nc',format="NETCDF3_64BIT")

    processes = []
    for _,f in zip(range(len(file_list)),file_list):
        for map_file in map_list:
            print(map_file)
            out_map_tag = map_file.split('/')[-1].split('map_')[1]
            new_file = f.split('.nc')[0]+'_'+out_map_tag
            if _mp!=None:
                p = mp.Process(target=get_files, args=[map_file,f,_data_dir,new_file,_sdim])
                p.start()
                processes.append(p)
            else:
                get_files(map_file,f,_data_dir,new_file,_sdim)
    if _mp!=None:
        for process in processes:
            process.join()

