from pathlib import Path
import sys
import os
import logging
from subprocess import Popen, PIPE, STDOUT, DEVNULL
import shlex
import numpy as np
import glob

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

def get_dir_path(path):
    if (path == ''):
        p=Path('.')
        dir_path = p.absolute()
    else:
        dir_path = Path(path)
    return dir_path

def checker(path):
    if len(glob.glob(str(path)))==0:
        raise Exception(color.LRED+"\n"+path+" does not exist!"+color.END)

def make_dir(path):
    if not os.path.exists(path):
        print("\n"+str(path)+" doesn't exist. Creating one...\n")
        os.makedirs(str(path))

def log_out(p, logger):
    for line in iter(p.readline,b''):
        logger.info('got line from sub: %r', line)
    

def get_sizes(filelist, limit=200000):
    '''
    Splits a list of files based on the file sizes
    to handle memory issues in multiprocessing.

    Parameters
    ----------
    filelist : List
        Original list of files.

    Returns
    -------
    listoflists : List
        Split list of lists of files.

    '''
    size_of_file = 0
    listoflists = []
    new_filelist = []
    i=0
    for file in filelist:
        size_of_file = size_of_file + os.stat(str(file)).st_size/1024/1024
        if size_of_file < limit:
            new_filelist.append(file)
        else:
            new_filelist.append(file)
            size_of_file = 0
            listoflists.append(new_filelist)
            new_filelist = []
        i+=1
    if len(filelist[i:]) != 0:
        listoflists.append(filelist[i:])
    if len(new_filelist) == len(filelist):
        listoflists.append(new_filelist)
    return listoflists

def exec_shell(cmd,inp='',hide=False):
    logger = logging.getLogger('log.ggen')
    cmd_split = shlex.split(cmd)
    logger.info('\n[cmd]: ' + cmd+ '\n')
    
    if hide:
        p = Popen(cmd_split, stdout=PIPE, stdin=DEVNULL, stderr=STDOUT, universal_newlines=True)
        op, _ =p.communicate()
    else:
        p = Popen(cmd_split, stdout=PIPE, stdin=PIPE, stderr=STDOUT, universal_newlines=True)
        p.stdin.write(inp)
        op, _ =p.communicate()
        items = op.split('\n')
        for line in items:
            logger.info(line)
    return p.returncode

        
def group_duplicate_index(df):
    a = df.values
    sidx = np.lexsort(a.T)
    b = a[sidx]

    m = np.concatenate(([False], (b[1:] == b[:-1]).all(1), [False] ))
    idx = np.flatnonzero(m[1:] != m[:-1])
    I = df.index[sidx].tolist()       
    return [I[i:j] for i,j in zip(idx[::2],idx[1::2]+1)]
