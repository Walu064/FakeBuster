import os
import sys

cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(cwd)
sys.path.append(api_dir)

from models import (AdvertModel, 
                    DefaultRequestModel, 
                    SearchRequestModel, 
                    AddressModel, 
                    QueryParamModel)

from .detectors import (DetectionType,
                        get_detection_type)

from .detectors import info as info_detector
from .detectors import search as search_detector
from .detectors import social as social_detector



def adds_detect(data : DefaultRequestModel | SearchRequestModel, address : AddressModel):
    adds_list : list[AdvertModel]
    
    det_type = get_detection_type(address.domain)
    
    match det_type:
        case DetectionType.SEARCH_BING:
            adds_list = search_detector.bing_detect(data)
        case DetectionType.SEARCH_GOOGLE:
            adds_list = search_detector.google_detect(data)
        case DetectionType.SOCIAL_FACEBOOK:
            adds_list = social_detector.facebook_detect(data)
        case DetectionType.SOCIAL_LINKEDIN:
            adds_list = social_detector.linkedin_detect(data)
        case DetectionType.SOCIAL_YOUTUBE:
            adds_list = social_detector.youtube_detect(data)
        case DetectionType.INFO_DEFAULT:
            adds_list = info_detector.info_detect(data)
        case _:
            raise ValueError("Unrecognized webservice type")

    return adds_list