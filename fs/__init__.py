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

def join_listlike(list_like):
    
    def trans(element):
        
        if element.startswith('/'):
            element = element[1:]
        if element.endswith('/'):
            element = element[:-1]

        return element

    converted = []
    for part in list_like:

        if isinstance(part, (list, tuple)):
            part = join_listlike(part)

        if isinstance(part, basestring):
            if part == '~':
                converted = []
                converted.append(py_expanduser('~'))
            else:
                converted.append(trans(part))
        
    path = '/'.join(converted)
    
    
    if not path.startswith('/') and not path[1] == ':':
        return '/' + path
    else:
        return path


def join(*inputs):
    return join_listlike(inputs)

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
    
    
    
    
    
    
    
