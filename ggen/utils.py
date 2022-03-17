#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 15:30:38 2022

@author: hass877
"""

from pathlib import Path
import sys
import os
import logging
from subprocess import Popen, PIPE, STDOUT
import shlex

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

def log_out(p, logger):
    for line in iter(p.readline,b''):
        logger.info('got line from sub: %r', line)
    

def exec_shell(cmd,inp=''):
    logger = logging.getLogger('log.ggen')
    cmd_split = shlex.split(cmd)
    logger.info('\n[cmd]: ' + cmd+ '\n')
    
    p = Popen(cmd_split, stdout=PIPE, stdin=PIPE, stderr=STDOUT, universal_newlines=True)
    p.stdin.write(inp)
    try:
        op, _ =p.communicate()
        items = op.split('\n')
        for line in items:
            logger.info(line)
    except (OSError) as exception:
        logger.info('Exception occured: '+str(exception))
        logger.info('Command failed!')

