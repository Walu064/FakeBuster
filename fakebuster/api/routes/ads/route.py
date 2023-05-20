import os
import sys
from fastapi import APIRouter, status

cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(os.path.dirname(cwd))
sys.path.append(api_dir)

from models import (DefaultRequestModel, 
                    SearchRequestModel,
                    AdvertModel,
                    create_response, create_error_response,
                    ResponseModel, ResponseAddModel, ErrorResponseModel)

from utils import (url_serialize, adds_detect, get_destination_urls,
                   get_text_from_img, get_keywords, filter_by_query)


router = APIRouter(
    tags=["Ads Detect"],
    prefix="/api/ads",
)


@router.post(path='/detect', 
             description="Get ads list on specified webservice.")
def detect_ads(data : DefaultRequestModel | SearchRequestModel) -> ResponseModel | ErrorResponseModel:
    ads_list : list[AdvertModel] = []
    
    print(' * URL Serialize...', file=sys.stderr)
    try:   
        address = url_serialize(data.url)
    except Exception as err:
        return create_error_response(str(err), status.HTTP_400_BAD_REQUEST)
    print('  * domain: ' + address.domain)

    print(' * Ads Detection...', file=sys.stderr)
    try:
        ads_list = adds_detect(data, address)
    
    except NotImplementedError as err:
        return create_error_response(str(err), status.HTTP_501_NOT_IMPLEMENTED)
    
    except Exception as err:
        return create_error_response(str(err), status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
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
        
        return create_response(data, ads_list)
