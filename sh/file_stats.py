
import os

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
