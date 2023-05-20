import json
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse

from .advert import AdvertModel


class ResponseAddModel(BaseModel):
    name : str
    destination_url : List[str]
    words : List[str]
    screenshot_ads : str


class ResponseModel(BaseModel):
    url : str
    user_agent : str
    context : str
    ads : List[ResponseAddModel]
    

def response_model(content : dict):    
    return JSONResponse(content=content)


def error_response_model(error : str, code : int):
    return JSONResponse(content={ 'error': error },
                        status_code=code)


def msg_response_model(message : str, code=200):
    content = { 'message' : message, 'code' : code }
    
    return JSONResponse(content=content,
                        status_code=code)   