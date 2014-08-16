__all__ = ['fs', 'FSException']

import os

from os.path import join, exists, isdir

class FSException(Exception):
    pass

def super_join(inputs):
    parts = []
    
    for part in inputs:
        if isinstance(part, (list, tuple)):
            parts.extend(part)
        if isinstance(part, basestring):
            parts.append(part)
    
    return join(*parts)
    

def make_dir_p(path):
    
    whole = "/"    
    for part in path.split('/'):
        
        whole = join(whole, part)
        
        if not exists(whole):
            os.mkdir(whole)
        if not isdir(whole):
            raise FSException("File exists at %s" % whole) 
        
        
        

def fs(cmd, *paths):
    if cmd == "join":
        return super_join(paths)
    if cmd == "mkdir -p":
        make_dir_p(paths[0])
    
    
    
    
    
    
    