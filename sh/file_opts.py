#!/usr/bin/env python

from join_listlike import join_listlike


def save_file(options, arguments):

    mode = options.get('mode', 'wb')
    path = join_listlike({}, arguments[:-1])

    with open(path, mode) as file:
        file.write(arguments[-1])
    
def load_file(options, arguments):
    
    mode = options.get('mode', 'rb')
    path = join_listlike({}, arguments)

    with open(path, mode) as file:
        return file.read()
