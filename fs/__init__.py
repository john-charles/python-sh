__all__ = ['fs', 'join', 'FSException']

import os
from os.path import join as py_join, exists, isdir

class FSException(Exception):
    pass

def join(*inputs):
    #print "inputs: ", inputs
    parts = []
    
    for part in inputs:
        
        if isinstance(part, (list, tuple)):
            parts.extend(part)
        if isinstance(part, basestring):
            parts.append(part)
    
    #print inputs
    return py_join(*parts)
    

def make_dir_p(path):
    
    path = join(*path)
    
    whole = "/"    
    for part in path.split('/'):
        
        whole = join(whole, part)
        
        if not exists(whole):
            os.mkdir(whole)
        if not isdir(whole):
            raise FSException("File exists at %s" % whole) 
        
        


def fs(cmd, *paths):
    if cmd == "join":
        return join(*paths)
    
    if cmd == "exists":
        return exists(join(*paths))

    if cmd == "mkdir -p":
        make_dir_p(paths)
    
    
    
    
    
    
    