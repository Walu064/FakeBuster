import os
import sys
from fastapi import APIRouter

cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(os.path.dirname(cwd))
sys.path.append(api_dir)

from models import (DflRequestModel, 
                                   SearchRequestModel,
                                   AdvertModel,
                                   response_model,
                                   error_response_model)


router = APIRouter(
    tags=["AddsDetect"],
    prefix="/detect/adds",
)


@router.post('/info', description="")
def detect_adds_on_info_service(req : DflRequestModel):
    # TODO: ADDS DETECTION script and save into adds : list
    adds = list[AdvertModel]
    
    return response_model(adds)
    

@router.post('/social', description="")
def detect_adds_on_social_service(req : DflRequestModel):
    # TODO: ADDS DETECTION script and save into adds : list
    adds = list[AdvertModel]
    
    return response_model(adds)


@router.post('/search', description="")
def detect_adds_in_searchengine(req : SearchRequestModel):
    # TODO: ADDS DETECTION script and save into adds : list
    adds = list[AdvertModel]
    
    return response_model(adds)