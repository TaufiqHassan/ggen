#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 21:25:04 2022

@author: thassan
"""

from subprocess import run
import os
import xarray as xr
from pathlib import Path
import sys

class color:
   PURPLE = '\033[35m'
   CYAN = '\033[36m'
   BLUE = '\033[34m'
   LBLUE='\033[94m'
   GREEN = '\033[32m'
   LGREEN='\033[92m'
   YELLOW = '\033[33m'
   RED = '\033[31m'
   LRED='\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class HidePrint:
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._stdout

def get_dir_path(path,dtype):
    if path == None:
        path = Path('.').absolute()
    else:
        path = Path(path)
    return path
    
def make_dir(path):
    if not os.path.exists(path):
        print("\n"+str(path)+" doesn't exist. Creating one...\n")
        os.makedirs(str(path))

def checker(file):
    if os.path.exists(file):
        print(file,'exists . . . reusing it.')
        return file


class get_res(object):
    def __init__(self, **kwargs):
        self._res = kwargs.get('res', None)
        self._file = kwargs.get('file', None)
        self._grid_dir = kwargs.get('grid_dir', None)
        self._data_dir = kwargs.get('data_dir', None)
        self._bilin = kwargs.get('bilin', None)
        
    @property
    def res(self):
        return self.res
    
    @res.setter
    def res(self, val):
        self._res=[0]
        ress = [x.strip() for x in val.split(',')]
        for zz in range(len(ress)):
            self._res.append(ress[zz])
        self._res.remove(0)
        
    @property
    def file(self):
        return self.file
    
    @file.setter
    def file(self, val):
        self._file=[0]
        files = [x.strip() for x in val.split(',')]
        for zz in range(len(files)):
            self._file.append(files[zz])
        self._file.remove(0)
        
    def get_out_scrip(self):
        in_file_list = []
        for r in self._res:
            if r[-3:] == 'pg2':
                in_file_list.append(get_grid(res=r, grid_dir=self._grid_dir,data_dir=self._data_dir).gen_grid_pg2())
            else:
                in_file_list.append(get_grid(res=r, grid_dir=self._grid_dir,data_dir=self._data_dir,bilin=self._bilin).gen_grid())
        return in_file_list
                
    def get_in_scrip(self):
        out_file_list = []
        for f in self._file:
            out_file_list.append(get_grid(file=f,data_dir=self._data_dir).gen_scrip())
        return out_file_list
        

class get_grid(object):
    
    def __init__(self, **kwargs):
        self._res = kwargs.get('res', None)
        self._file = kwargs.get('file', None)
        self._grid_dir = kwargs.get('grid_dir', None)
        self._data_dir = kwargs.get('data_dir', None)
        self._bilin = kwargs.get('bilin', None)
        
    def gen_grid(self):
        self._data_dir=get_dir_path(self._data_dir,'data')
        self._grid_dir=get_dir_path(self._grid_dir,'grid')
        if self._grid_dir == Path('.').absolute():
            self._grid_dir = self._data_dir
        if self._bilin != None:
            penta_file = {'4':'ne4np4_pentagons_c100308.nc','16':'ne16np4_110512_pentagons.nc','30':'ne30np4_pentagons.20190501.nc','120':'ne120np4_pentagons.20190601.nc'}
            return str(self._grid_dir)+'/'+penta_file[self._res]
        else:
            run(f'GenerateCSMesh --alt --res {self._res} --file {self._grid_dir}/ne{self._res}.g'.split(' '), capture_output=True)
            print('\nGenerated ne'+self._res+'np4 grid in '+str(self._grid_dir))
            run(f'ConvertExodusToSCRIP --in {self._grid_dir}/ne{self._res}.g --out {self._grid_dir}/ne{self._res}np4_SCRIP.nc'.split(' '), capture_output=True)
            print('\nGenerated ne'+self._res+'np4 SCRIP file in '+str(self._grid_dir))
            return str(self._grid_dir)+str('/ne'+self._res+'np4_SCRIP.nc')
    
    def gen_grid_pg2(self):
        self._data_dir=get_dir_path(self._data_dir,'data')
        self._grid_dir=get_dir_path(self._grid_dir,'grid')
        if self._grid_dir == Path('.').absolute():
            self._grid_dir = self._data_dir
        run(f'GenerateCSMesh --alt --res {self._res[:-3]} --file {self._grid_dir}/ne{self._res[:-3]}.g'.split(' '), capture_output=True)
        run(f'GenerateVolumetricMesh --in {self._grid_dir}/ne{self._res[:-3]}.g --out {self._grid_dir}/ne{self._res}.g --np 2 --uniform'.split(' '), capture_output=True)
        print('\nGenerated ne'+self._res+' grid in '+str(self._grid_dir))
        run(f'ConvertExodusToSCRIP --in {self._grid_dir}/ne{self._res}.g --out {self._grid_dir}/ne{self._res}_SCRIP.nc'.split(' '), capture_output=True)
        print('\nGenerated ne'+self._res+' SCRIP file in '+str(self._grid_dir))
        return str(self._grid_dir)+str('/ne'+self._res+'_SCRIP.nc')
        
    def gen_scrip(self):
        self._data_dir=get_dir_path(self._data_dir,'data')
        self._grid_dir=get_dir_path(self._grid_dir,'grid')
        if self._grid_dir == Path('.').absolute():
            self._grid_dir = self._data_dir
        se_grids = {96:'ne4np4',1536:'ne16np4',5400:'ne30np4',86400:'ne120np4',384:'ne4pg2',6144:'ne16pg2',21600:'ne30pg2',345600:'ne120pg2'}
        data = xr.open_dataset(self._file)
        try:
            lat = data.dims['lat']
            lon = data.dims['lon']
            run(f'ncks --rgr infer --rgr scrip={self._grid_dir}/{lat}x{lon}_SCRIP.nc {self._file} {self._grid_dir}/foo.nc'.split(' '), capture_output=True, text=True, input="o")
            print('\nGenerated '+str(lat)+'x'+str(lon)+'_SCRIP.nc inferred from '+self._file+' in '+str(self._grid_dir))
            return str(self._grid_dir)+'/'+str(lat)+'x'+str(lon)+'_SCRIP.nc'
        except:
            try:
                ncol = data.dims['ncol']
                se_val = se_grids[ncol]
                run(f'ncks --rgr infer --rgr scrip={self._grid_dir}/{se_val}_SCRIP.nc {self._file} {self._grid_dir}/foo.nc'.split(' '), capture_output=True, text=True, input="o")
                print('\nGenerated '+se_val+'_SCRIP.nc inferred from '+self._file+' in '+str(self._grid_dir))
                return str(self._grid_dir)+'/'+se_val+'_SCRIP.nc'
            except KeyError:
                print('\nMake sure the file ',self._file,' has a lat/lon or ncol dimension.')


  


