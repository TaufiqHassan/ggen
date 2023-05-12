import logging
import multiprocessing as mp
import pandas as pd
import numpy as np
import xarray as xr

from pathlib import Path
from itertools import product

from ggen.ggrids import generate_grids
from ggen.utils import get_dir_path, exec_shell, checker, get_sizes

class driver(object):
    def __init__(self, **kwargs):
        '''
        Initiates driver class.

        Parameters
        ----------
        **kwargs : Multiple arguments
            Output resolution
            Input resolution
            Input filenames
            Input grid filename
            Input directory
            Output directory
            Input mapping file
        Options:
            Add single dim
            Apply multiprocessing

        '''
        self._res = kwargs.get('res', None)
        self._ires = kwargs.get('ires', None)
        self._file = kwargs.get('file', None)
        self._infile = kwargs.get('infile', None)
        self._grid = kwargs.get('grid', None)
        self._indir = kwargs.get('ind', '')
        self._outdir = kwargs.get('out', '')
        self._mf = kwargs.get('mapfile', None)
        self._sdim = kwargs.get('sdim', None)
        self._mp = kwargs.get('mp', None)
        self.logger = logging.getLogger(str(get_dir_path(self._outdir))+'/log.ggen')
        
        self.logger.info('\n=== driver init done ===')
        
    def gen_remapped_files(self):
        '''
        Generate remapped files.
        Has option to apply multiprocessing.
        
        Depends on gen_weights & apply_weights methods.
        
        '''
        
        ## Instantiating the generate_grids
        gen_grids = generate_grids(ind=self._indir,out=self._outdir)
        gen_grids.file = self._file
        
        file_list = gen_grids._file
        list_of_filelist = get_sizes(file_list)
        
        map_list = self.gen_weights()
        dir_path = get_dir_path(self._outdir)
        
        for filelist in list_of_filelist:
            processes = []
            for mapfile, file in product(map_list,filelist):
                if self._mp==None:
                    self.apply_weights(self,str(mapfile),str(file),dir_path)
                else:
                    self.logger.info('\nApplied multiprocessing.')
                    p = mp.Process(target=self.apply_weights, args=[self,str(mapfile),str(file),dir_path])
                    p.start()
                    processes.append(p)
            if self._mp!=None:
                for process in processes:
                    process.join()
                
        self.logger.info('\n=== gen_remapped_files done ===')
        
    def gen_weights(self):
        '''
        Generates weights/mapping files.

        Returns
        -------
        maps : List
            List of mapping files.

        '''
        maps = []
        if self._mf != None:
            self.logger.info('\nSpecifying map file suppresses weight generation.')
            if not Path(str(self._mf)).is_file():
                dir_path = get_dir_path(self._indir)
                fname = dir_path / self._mf
                checker(str(fname))
                self.logger.info('Using weights from '+str(fname))
                maps.append(fname)
            else:
                fname = str(self._mf)
                checker(fname)
                maps.append(fname)
        else:
            list_in, list_out = self.gen_scrips()
        
            for in_scrip in list_in:
                for out_scrip in list_out:
                    self.logger.info('\nInput SCRIP:'+in_scrip)
                    self.logger.info('Output SCRIP:'+out_scrip)
                    ins=str(in_scrip).split('/')[-1].split('_')[0]
                    outs=str(out_scrip).split('/')[-1].split('_')[0]
                    algo = 'fv2fv_flx'
                    dir_path = get_dir_path(self._outdir)
                    fname = dir_path / str('map_'+ins+'_'+outs+'.nc')
                    if not Path(fname).is_file():
                        rc = exec_shell(f'ncremap --alg_typ={algo} --src_grd={in_scrip} --dst_grd={out_scrip} --map={fname}')
                        if rc == 0:
                            self.logger.info('\nGenerated map_'+ins+'_'+outs+'.nc mapping file in '+str(dir_path))
                        else:
                            self.logger.info('\nERROR: Weights were not generated properly!')
                        maps.append(fname)
                    else:
                        self.logger.info('\n'+str(fname)+' already exists!\nUsing it.')
                        maps.append(fname)
                        
        self.logger.info('\n=== gen_weights done ===')
        
        return maps
    
    def gen_scrips(self):
        '''
        Generates input and out SCRIP files.

        Returns
        -------
        list_in : List
            List of input SCRIP files.
        list_out : List
            List of Output SCRIP files.

        '''
        
        ## Instantiating the generate_grids
        gen_grids = generate_grids(ind=self._indir,out=self._outdir)
        gen_grids.file = self._file
        gen_grids.ires = self._ires
        
        list_in = gen_grids.get_inp_scrip()
        list_in = list(pd.Series(list_in).unique())
        
        ## Instantiating the generate_grids
        gen_grids = generate_grids(ind=self._indir,out=self._outdir)
        gen_grids.grid = self._grid
        gen_grids.res = self._res
        
        list_out = gen_grids.get_out_scrip()
        list_out = list(pd.Series(list_out).unique())
        
        self.logger.info('\n=== gen_scrips done ===')
        
        return list_in, list_out
    
    @staticmethod
    def apply_weights(self,mapfile,file,dir_path):
        '''
        Applies weights on the input files.

        Parameters
        ----------
        mapfile : NetCDF file
            Weights/Mapping files.
        file : NetCDF file
            Input files.
        dir_path : Directory
            Path to output directory.

        '''
        out_map_tag = mapfile.split('/')[-1].split('map_')[1]
        fname = dir_path / str(file.split('/')[-1].split('.nc')[0]+'_'+out_map_tag)
        self.logger.info('\nApplying '+mapfile+' on '+file)
        if not Path(fname).is_file():
            rc = exec_shell(f'ncremap --map={mapfile} {file} {fname}')
            if rc == 0:
                self.logger.info('\nGenerated remapped file '+str(fname))
            else:
                self.logger.info('\nERROR: Remapped files were not generated!')
        else:
            self.logger.info('\n'+str(fname)+' already exists.')
        if self._sdim != None:
            self.logger.info('\nAdding a singleton dim: lev.')
            lev=np.array([1e5])
            data=xr.open_dataset(str(fname))
            data1=data.expand_dims('lev',axis=1)
            data2 = data1.assign_coords(lev=('lev',lev))
            data2.load().to_netcdf(str(fname).replace('.nc','_lev.nc'),format="NETCDF3_64BIT")
            
        self.logger.info('\n=== apply_weights done ===')
                            
            