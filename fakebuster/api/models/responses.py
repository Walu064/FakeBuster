import json
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse

from .requests import DefaultRequestModel, SearchRequestModel
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
    

class ErrorResponseModel(BaseModel):
    detail : str
    code : int
    

def create_response(request_data : DefaultRequestModel | SearchRequestModel,
                   ads_list : list[AdvertModel] | None = None):
    
    serial_ads_list : list[ResponseAddModel] = []
    if ads_list:
        for ad in ads_list:
            serial_ads_list.append(
                ResponseAddModel(name=ad.name,
                                 destination_url=ad.destination_url,
                                 words=ad.words,
                                 screenshot_ads=ad.screenshot_ads)
            )
    
    return ResponseModel(url=request_data.url,
                             user_agent=request_data.user_agent,
                             context=request_data.context,
                             ads=serial_ads_list)


def create_error_response(error : str, code : int):
    return JSONResponse(ErrorResponseModel(detail=error, code=code).dict(), status_code=code)
