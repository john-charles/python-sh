#!/usr/bin/env python

from SHException import SHException
from join_listlike import join_listlike


def save_file(options, arguments):

    mode = options.get('mode', 'wb')
    path = join_listlike({}, arguments[:-1])
    
    try:

        with open(path, mode) as file:
            file.write(arguments[-1])

    except Exception, e:
        raise SHException(e.message)
        
def load_file(options, arguments):
    
    mode = options.get('mode', 'rb')
    path = join_listlike({}, arguments)

    with open(path, mode) as file:
        return file.read()
