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

from utils import (url_serialize, adds_detect, get_destination_urls,
                   get_text_from_img, get_keywords, filter_by_query)


router = APIRouter(
    tags=["Ads Detect"],
    prefix="/api/ads",
)


@router.post('/detect', description="Get ads list on specified webservice.")
def detect_ads(data : DefaultRequestModel | SearchRequestModel):
    adds_list : list[AdvertModel] = []
    
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
        
        adds_list_serialized = []
        for add in adds_list:
            print('    - OCR: text from img...', file=sys.stderr)
            add_text : str = get_text_from_img(add.screenshot_ads)
            
            print('    - Keywords retrieving...', file=sys.stderr)
            keywords : list[str] = get_keywords(add_text)
            add.words += keywords
            
            print('    - Keywords filtering...', file=sys.stderr, end=' ')
            if not filter_by_query(" ".join(add.words), data.query):
                print(' Skip', file=sys.stderr)
                continue
            
            print(' Valid', file=sys.stderr)
            
            print('    - Retrieving redirection chain...', file=sys.stderr)
            add.destination_url = get_destination_urls(add.url)
            adds_list.append(add.to_dict)
        
        print(' * Response build done.', file=sys.stderr)        
        content : dict = {
                "url" : data.url,
                "user-agent" : data.user_agent,
                "context" : data.context,
                "adds" : adds_list_serialized,
            }
        
        return response_model(content)
