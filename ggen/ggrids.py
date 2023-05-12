import glob
import logging
from pathlib import Path

from ggen.utils import get_dir_path, checker
from ggen.gen_scrip_file import gen_scrip

class generate_grids(object):
    '''
    generate_grids class handles all type of grid & SCRIP file generation.
    Returns lists of SCRIP filenames.
 
    '''
    def __init__(self, **kwargs):
        self._res = kwargs.get('res', None)
        self._ires = kwargs.get('ires', None)
        self._file = kwargs.get('file', None)
        self._infile = kwargs.get('infile', None)
        self._grid = kwargs.get('grid', None)
        self._indir = kwargs.get('ind', '')
        self._outdir = kwargs.get('out', '')
        self.logger = logging.getLogger(str(get_dir_path(self._outdir))+'/log.ggen')
        
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
    def inres(self):
        return self.ires
    
    @inres.setter
    def inres(self, val):
        self._ires=[0]
        ress = [x.strip() for x in val.split(',')]
        for zz in range(len(ress)):
            self._ires.append(ress[zz])
        self._ires.remove(0)
        
    @property
    def grid(self):
        return self.file
    
    @grid.setter
    def grid(self, val):
        dirval = get_dir_path(self._indir) / str(val)
        if len(glob.glob(str(val)))>0:
            self._grid=glob.glob(str(val))
        elif len(glob.glob(str(dirval)))>0:
            self._grid=glob.glob(str(dirval))
        elif self._grid != None:
            self._grid=[0]
            files = [x.strip() for x in str(val).split(',')]
            for zz in range(len(files)):
                file = get_dir_path(self._indir) / str(files[zz])
                checker(str(file))
                self._grid.append(file)
            self._grid.remove(0)
        
    @property
    def file(self):
        return self.file
    
    @file.setter
    def file(self, val):
        dirval = get_dir_path(self._indir) / str(val)
        if len(glob.glob(str(val)))>0:
            self._file=glob.glob(str(val))
        elif len(glob.glob(str(dirval)))>0:
            self._file=glob.glob(str(dirval))
        else:
            self._file=[0]
            files = [x.strip() for x in str(val).split(',')]
            for zz in range(len(files)):
                file = get_dir_path(self._indir) / str(files[zz])
                checker(str(file))
                self._file.append(file)
            self._file.remove(0)
    
    @property
    def infile(self):
        return self.infile
    
    @infile.setter
    def infile(self, val):
        if not Path(str(val)).is_file():
            val = get_dir_path(self._indir) / str(val)
        checker(str(val))
        self._infile=glob.glob(str(val))
        if self._infile==[]:
            self._infile=[0]
            files = [x.strip() for x in val.split(',')]
            for zz in range(len(files)):
                self._infile.append(files[zz])
            self._infile.remove(0)
    
    def get_inp_scrip(self):
        '''
        Generate SCRIP files from input NetCDF files or resolution.
        Input resolution:
            For SE grids integer values (4, 30, 120 etc.)
            For RLL grids use latitudexlongitude (64x128, 180x360 etc.)

        Returns
        -------
        in_file_list : List
            List of SCRIP file names for the input mesh.

        '''
        in_file_list = []
        if self._ires != None:
            for r in self._ires:
                self.logger.info('\nInput Resolution: '+str(r))
                fname = gen_scrip(res=r,file=self._infile,path=self._outdir,fdir=self._indir,grid=self._grid,nc=True).get_scrip_file()
                self.logger.info('\nGenerated '+str(fname))
                in_file_list.append(str(fname))
        else:
            for f in self._file:
                self.logger.info('\nSpecifying input file suppresses resolution.\n(Recommended for SE to RLL conversion)')
                fname = gen_scrip(res=self._res,file=f,path=self._outdir,fdir=self._indir,grid=self._grid,nc=True).get_scrip_file()
                self.logger.info('\nGenerated '+str(fname))
                in_file_list.append(str(fname))
        return in_file_list
    
    def get_out_scrip(self):
        '''
        Generate SCRIP files from output grid file or resolution.
        Output resolution:
            For SE grids integer values (4, 30, 120 etc.)
            For RLL grids use latitudexlongitude (64x128, 180x360 etc.)

        Returns
        -------
        out_file_list : List
            List of SCRIP file names for the output mesh.

        '''
        out_file_list = []
        if self._grid != None:
            for g in self._grid:
                self.logger.info('\nUsing specified grid file: '+ g)
                self.logger.info('\nSpecifying grid file suppresses resolution.')
                fname = gen_scrip(res=self._res,file=self._file,path=self._outdir,fdir=self._indir,grid=g,nc=True).get_scrip_file()
                self.logger.info('\nGenerated '+str(fname))
                out_file_list.append(str(fname))
        else:
            for r in self._res:
                self.logger.info('\nOutput Resolution: '+r)
                fname = gen_scrip(res=r,file=self._infile,path=self._outdir,fdir=self._indir,grid=self._grid,nc=True).get_scrip_file()
                self.logger.info('\nGenerated '+str(fname))
                out_file_list.append(str(fname))
        return out_file_list

