from typing import NamedTuple


class QueryParamModel(NamedTuple):
    name : str
    value : any
    

class AddressModel(NamedTuple):
    line : str
    isWWW : bool
    protocol : str
    domain : str
    theme : str
    tail : str
    query_params : list[QueryParamModel]
