import json
from fastapi.responses import JSONResponse
from .advert import AdvertModel
 
def response_model(content : dict):    
    return JSONResponse(content=content)


def error_response_model(error : str, code : int):
    return JSONResponse(content={ 'error': error },
                        status_code=code)


def msg_response_model(message : str, code=200):
    content = { 'message' : message, 'code' : code }
    
    return JSONResponse(content=content,
                        status_code=code)   