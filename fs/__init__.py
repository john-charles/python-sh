__all__ = ['fs', 'join', 'save', 'load', 'exists', 'FSException']

import os
from os.path import join as py_join, exists as py_exists, isdir as py_isdir

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
        
        if not py_exists(whole):
            os.mkdir(whole)
        if not py_isdir(whole):
            raise FSException("File exists at %s" % whole) 
        
        
def save(*args, **kw):
    
    content = args[-1]
    path = join(*args[:-1])
    mode = kw.get('mode', 'wb')
    
    f = open(path, mode)
    f.write(content)
    f.close()
    
def load(*path, **kw):    
    path = join(*path)
    mode = kw.get('mode','rb')
    
    f = open(path, mode)
    content = f.read()
    f.close()
    
    return content
    
    

def exists(*args):
    return py_exists(join(*args))


def fs(cmd, *paths):
    if cmd == "join":
        return join(*paths)
    
    if cmd == "exists":
        return exists(*paths)

    if cmd == "mkdir -p":
        make_dir_p(paths)
    
    
    
    
    
    
    