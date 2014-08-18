__all__ = ['fs', 'join', 'save', 'load', 'exists', 'FSException']

import os
from os.path import (
    join as py_join,
    isdir as py_isdir,
    exists as py_exists,
    expanduser as py_expanduser
)
    

class FSException(Exception):
    pass

def join(*inputs):
    # super procedural, because this utility should
    # be available to people doing low level work.
    path = ""
    
    for part in inputs:
        if isinstance(part, basestring):
            
            if part.startswith('~'):
                # we have a tild path.
                if part[1] == '/':
                    path = py_expanduser('~')
                    # we need to get a path without ~/ 
                    path += part[2:]
                else:
                    user, part = part.split('/', 1)
                    
                path = py_expanduser()
                    
                            
                        
                    
    
    
    #parts = []
    
    #for part in inputs:
        
        #if isinstance(part, (list, tuple)):
            #parts.extend(part)
        #if isinstance(part, basestring):
            #parts.append(part)
    
    
    #return py_join(*parts)
    

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
    
    
    
    
    
    
    