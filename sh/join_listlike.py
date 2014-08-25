import os, re

from os.path import expanduser as py_expanduser

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
            
            if part.count('\\'):
                converted.extend(join_listlike({"as_list": True}, part.split('\\')))
            elif part.count('$'):
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
    
    
    if not path.startswith('/') and not path[1] == ':' and not path.startswith("."):
        return '/' + path
    else:
        return path
