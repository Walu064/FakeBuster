import os
import sys
from fastapi import APIRouter, HTTPException, status

cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(os.path.dirname(cwd))
sys.path.append(api_dir)

from fakebuster.api.models import (DefaultRequestModel,
                    SearchRequestModel,
                    AdvertModel,
                    create_response,
                    ResponseModel, ErrorResponseModel)

from fakebuster.api.utils import (url_serialize, adds_detect, get_destination_urls,
                   get_text_from_img, get_keywords, filter_by_query)


router = APIRouter(
    tags=["Ads Detect"],
    prefix="/api/ads",
    responses={
        400 : {
            "description" : "Bad Request",
            "model" : ErrorResponseModel
        },
        500 : {
            "description" : "Unexpected detection script error.",
            "model" : ErrorResponseModel
        },
        501 : {
            "description" : "Detection method not implemented yet",
            "model" : ErrorResponseModel
        }
    }
)


@router.post(path='/detect', 
             description="Get ads list on specified webservice.", 
             response_model=ResponseModel)
def detect_ads(data : DefaultRequestModel | SearchRequestModel) -> ResponseModel:
    ads_list : list[AdvertModel] = []
    
    print(' * URL Serialize...', file=sys.stderr)
    try:   
        address = url_serialize(data.url)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid url field!"
        )
    print('  * domain: ' + address.domain)

    print(' * Ads Detection...', file=sys.stderr)
    try:
        ads_list = adds_detect(data, address)
    
    except NotImplementedError as err:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=str(err)
        )
    
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
    
    else:
        print(' * Response building...', file=sys.stderr)
        
        for i, ad in enumerate(ads_list):
            print('    - OCR: text from img : ' + ad.screenshot_ads, file=sys.stderr)
            ad_text = get_text_from_img(ad.screenshot_ads)
            
            if ad_text:
                print('    - Keywords retrieving...', file=sys.stderr)
                keywords : list[str] = get_keywords(ad_text)
                ad.words.append(keywords)
            
        if len(ads_list) > 0:
            keywords_list = []
            dest_urls = []
            names = []

            for i, ad in enumerate(ads_list):
                print('    - OCR: text from img...', file=sys.stderr)
                ad_text : str = get_text_from_img(ad.screenshot_ads)

                print('    - Keywords retrieving...', file=sys.stderr)
                keywords : list[str] = get_keywords(ad_text)

                print('    - Keywords filtering...', file=sys.stderr, end=' ')
                # if not filter_by_query(" ".join(keywords), data.query):
                #     keywords_list.append(None)
                #     dest_urls.append(None)
                #     names.append(None)
                #     print(' Skip', file=sys.stderr)
                #     print(data.query + " xxd ")
                #     continue
            
                print(' Valid', file=sys.stderr)
                

                print('    - Retrieving redirection chain...', file=sys.stderr)
                destination_url = get_destination_urls(ad.url, data.user_agent, f'{address.protocol}://{address.domain}')
            
                print('    - Unique ad name generating...', file=sys.stderr)
                name = f"Ad#{i}"
                
                keywords_list.append(keywords)
                dest_urls.append(destination_url)
                names.append(name)

            return create_response(data, ads_list, keywords_list, dest_urls, names)
        else:
            return create_response(data)
