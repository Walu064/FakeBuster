import os
import sys
from fastapi import APIRouter, status

cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(os.path.dirname(cwd))
sys.path.append(api_dir)

from models import (DefaultRequestModel, 
                    SearchRequestModel,
                    AdvertModel,
                    error_response_model,
                    ResponseModel, ResponseAddModel)

from utils import (url_serialize, adds_detect, get_destination_urls,
                   get_text_from_img, get_keywords, filter_by_query)


router = APIRouter(
    tags=["Ads Detect"],
    prefix="/api/ads",
)


@router.post('/detect', description="Get ads list on specified webservice.")
def detect_ads(data : DefaultRequestModel | SearchRequestModel) -> ResponseModel:
    ads_list : list[AdvertModel] = []
    
    print(' * URL Serialize...', file=sys.stderr)
    try:   
        address = url_serialize(data.url)
    except Exception as err:
        return error_response_model(str(err), status.HTTP_400_BAD_REQUEST)
    print('  * domain: ' + address.domain)

    print(' * Ads Detection...', file=sys.stderr)
    try:
        adds_list = adds_detect(data, address)
    
    except NotImplementedError as err:
        return error_response_model("Detection method not implemented yet.", status.HTTP_501_NOT_IMPLEMENTED)
    
    except Exception as err:
        return error_response_model(str(err), status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
    else:
        print(' * Response building...', file=sys.stderr)
        
        for i, ad in enumerate(ads_list):
            print('    - OCR: text from img...', file=sys.stderr)
            ad_text : str = get_text_from_img(ad.screenshot_ads)
            
            print('    - Keywords retrieving...', file=sys.stderr)
            keywords : list[str] = get_keywords(ad_text)
            ad.words += keywords
            
            print('    - Keywords filtering...', file=sys.stderr, end=' ')
            if not filter_by_query(" ".join(ad.words), data.query):
                print(' Skip', file=sys.stderr)
                continue
            
            print(' Valid', file=sys.stderr)
            
            print('    - Retrieving redirection chain...', file=sys.stderr)
            ad.destination_url = get_destination_urls(ad.url)
            
            print('    - Unique ad name generating...', file=sys.stderr)
            ad.name = f"Ad#{i}"
            
            ads_list.append(ad.to_dict)
        
        print('    - Response serializing...', file=sys.stderr)
        serial_ads_list : list[ResponseAddModel] = []
        for ad in ads_list:
            serial_ads_list.append(
                ResponseAddModel(name=ad.name,
                                 destination_url=ad.destination_url,
                                 words=ad.words,
                                 screenshot_ads=ad.screenshot_ads)
            )
        
        response = ResponseModel(url=data.url,
                                 user_agent=data.user_agent,
                                 context=data.context,
                                 ads=serial_ads_list)
        
        return response
