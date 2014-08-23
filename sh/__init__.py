__all__ = ['fs', 'join', 'save', 'load', 'exists', 'FSException']

import os, re
from os.path import (
    join as py_join,
    isdir as py_isdir,
    exists as py_exists,
    expanduser as py_expanduser
)

class FSException(Exception):
    pass

def join_listlike(options, list_like):
    
    def trans(element):
        
        if element.startswith('/'):
            element = element[1:]
        if element.endswith('/'):
            element = element[:-1]

        return element

    def expand_tild(part):
        
        expanded_part = py_expanduser(part)
        if os.path.sep != '/':
            expanded_part = expanded_part.replace('\\','/')
        
        return [expanded_part]

    def expand_env(part):
        result = []
        parts = re.split(r'(\$[A-Z_]+)', part)

        for part in parts:
            
            part = part.strip()

            if part.startswith('$'):
                try:
                    result.append(os.environ[part[1:]])
                except KeyError:
                    print "key error", part[1:]
                    result.append(part)
            else:
                result.append(part)

        return "".join(result)

    converted = []

    for part in list_like:

        if isinstance(part, (list, tuple)):
            part = join_listlike(options, part)

        if isinstance(part, basestring):
            if part.count('$'):
                converted.append(expand_env(part))
            elif part.startswith('~'):
                converted = expand_tild(part)
            else:
                converted.append(trans(part))
    
    
    if 'as_list' in options and  options['as_list']:
        result = []
        for part in converted:
            for sub_part in part.split('/'):
                if part:
                    result.append(sub_part)
                    
        return result
            
    path = '/'.join(converted)
    
    
    if not path.startswith('/') and not path[1] == ':':
        return '/' + path
    else:
        return path
    
    
def make_dir_p(options, arguments):
    
    path = join_listlike({},arguments)    
    os.mkdir(path)
    
    #path = join(*path)
    
    #whole = "/"    
    #for part in path.split('/'):
        
        #whole = join(whole, part)
        
        #if not py_exists(whole):
            #os.mkdir(whole)
        #if not py_isdir(whole):
            #raise FSException("File exists at %s" % whole) 
        
        
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

OT_FLAG = 'flag'

def option(shortcut, name, opt_type, message):
    
    def parse(string):
        
        if string.startswith("--%s" % name):
            if opt_type == OT_FLAG:
                return name, True
        
        if string.startswith('-') and not string.startswith('--'):
            if shortcut in string:
                return name, True
            
        return name, False
    
    return parse

def options(*options):
    
    def parse(args):
        
        resovled_options = {}
        
        for option in options:
            
            for string in args:
                
                name, value = option(string)
                if name in resovled_options:
                    raise Exception("Option %s specified multiple times" % name)                
                
                resovled_options[name] = value
                
        return resovled_options
            
    return parse

COMMAND_MAP = {
    "join": (join_listlike, options(
        option("l", "as_list", OT_FLAG, "Specifies that the path should not be joined")
    )),
    "mkdir": (make_dir_p, options())
}


def parse_cmd(cmd):
    
    args = cmd.split()
    cmd, options = COMMAND_MAP[args[0]]
    options = options(args[1:])
    
    return cmd, options    

def sh(cmd, *arguments):
    
    cmd, options = parse_cmd(cmd)
    return cmd(options, arguments)
    
    
    
    
    
    
