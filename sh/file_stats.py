
import os, stat

from os.path import (
    join as py_join,
    isdir as py_isdir,
    exists as py_exists
)

from SHException import SHException
from join_listlike import join_listlike

def file_exists(options, arguments):
    
    path = join_listlike({}, arguments)
    return py_exists(path)

def file_isdir(options, arguments):
    
    path = join_listlike({}, arguments)
    return os.path.isdir(path)

def file_isfile(options, arguments):

    path = join_listlike({}, arguments)
    return os.path.isfile(path)

def file_listdir(options, arguments):
    
    if len(arguments) == 0:
        path = "."
    else:
        path = join_listlike({}, arguments)
    
    return os.listdir(path)

def file_stat(options, arguments):
    
    path = join_listlike({}, arguments)
    stat_res = os.stat(path)

    if 'size' in options and options['size']:
        return stat_res[stat.ST_SIZE]

    return stat_res
