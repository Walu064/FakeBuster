import os
import re
import sys


cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(os.path.dirname(cwd))
sys.path.append(api_dir)

from fakebuster.api.models import AddressModel, QueryParamModel


def __serialize(url : str) -> AddressModel:
    line = url
    isWWW = False
    prot = ""
    domain = ""
    theme = ""
    tail = ""
    query_params = []
    
    # URL normalization for regex check
    if url.count('/') == 2:
        url += '/'
    elif url.count('/') > 2:
        if url.count('?') == 0:
            if url[-1] != '/':
                url += '/?'
            else:
                url += '?'
    
    regex = r"^(?P<protocol>.+):\/\/(www\.){0,1}(?P<domain>.+?\/){1}(?P<rest>.*?)$"
    result = re.match(regex, url)
    
    if result:
        prot = result.group('protocol')
        domain = result.group('domain')
        rest = result.group('rest')
        
        if ((prot.__eq__('http')) or (prot.__eq__('https'))):
            isWWW = True
            
        if len(rest) > 0:
            try:
                theme = rest.split('?', 1)[0]
                tail = rest.split('?', 1)[1]
                
                if len(tail) > 0:
                    try:
                        params = tail.split('&')
                        for param in params:
                            name = param.split('=', 1)[0]
                            
                            try:
                                value = param.split('=', 1)[1]
                            except IndexError:
                                value = True
                                
                            query_params.append(QueryParamModel(name, value))
                            
                    except IndexError:
                        tail = ""
                
            except IndexError:
                theme = rest
                tail = ""
                
        else:
            theme = ""
            tail = ""
        
    else:
        raise ValueError(f'Url Validation: `{url}` does not match {regex}')
    
    return AddressModel(line, isWWW, prot, domain, theme, tail, query_params)
    

def url_serialize(url : str) -> AddressModel:
    try:
        address = __serialize(url)
        return address
    
    except ValueError:
        raise
