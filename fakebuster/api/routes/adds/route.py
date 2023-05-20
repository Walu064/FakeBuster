import os
import sys
from fastapi import APIRouter, status

cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(os.path.dirname(cwd))
sys.path.append(api_dir)

from models import (DefaultRequestModel, 
                    SearchRequestModel,
                    AdvertModel,
                    response_model,
                    error_response_model)

from utils import (url_serialize, adds_detect, get_destination_urls)


router = APIRouter(
    tags=["AddsDetect"],
    prefix="/api/adds",
)


@router.post('/detect', description="Get adds list on specified webservice.")
def detect_adds(data : DefaultRequestModel | SearchRequestModel):
    adds_list : list[AdvertModel] = []
    
    try:   
        address = url_serialize(data.url)
    except Exception as err:
        return error_response_model(str(err), status.HTTP_400_BAD_REQUEST)

    try:
        adds_list = adds_detect(data, address)
    
    except NotImplementedError as err:
        return error_response_model("Detection method not implemented yet.", status.HTTP_501_NOT_IMPLEMENTED)
    
    except Exception as err:
        return error_response_model(str(err), status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
    else:
        adds_list_serialized = []
        for add in adds_list:
            add.destination_url = get_destination_urls(add._url_)
            adds_list.append(add.to_dict)
        
        content : dict = {
                "url" : data.url,
                "user-agent" : data.user_agent,
                "context" : data.context,
                "adds" : adds_list_serialized,
            }
        
        return response_model(content)
