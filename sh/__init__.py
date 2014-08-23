__all__ = ['sh', 'SHException']

import os, re

from SHException import SHException
from join_listlike import join_listlike

from os.path import (
    join as py_join,
    isdir as py_isdir,
    exists as py_exists
)



    
    
def make_dir_p(options, arguments):
    
    if 'parents' in options and options['parents']:
        
        whole = ""
        
        for part in join_listlike({"as_list": True}, arguments):
            whole += "/%s" % part
            
            if not py_exists(whole):
                os.mkdir(whole)
            if not py_isdir(whole):
                raise SHException("File exists at %s" % whole)
        
    else:
        
        path = join_listlike({},arguments)
        try:
            os.mkdir(path)
        except Exception, e:
            raise SHException(e.message)
    
    
    
        
        
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
        option("l", "as_list", OT_FLAG, "Specifies that the path should not be joined.")
    )),
    "mkdir": (make_dir_p, options(
        option("p", "parents", OT_FLAG, "Specifies that parent directories should be created if they don't exist.")
    ))
}


def parse_cmd(cmd):
    
    args = cmd.split()
    cmd, options = COMMAND_MAP[args[0]]
    options = options(args[1:])
    
    return cmd, options    

def sh(cmd, *arguments):
    
    cmd, options = parse_cmd(cmd)
    return cmd(options, arguments)
    
    
    
    
    
    
