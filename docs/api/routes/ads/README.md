# Route: Ads

## **Description:**

Implementation of fastAPI router to handle advertisement endpoints : `/api/ads`.

---

## **Endpoints:**

## **`/api/ads/detect`**

### Method: **`POST`**

### **Requests:**

#### **DefaultRequest**

``` json
{
    "url": "string",
    "query": "string",
    "user_agent": "string",
    "context": "string"
}
```

#### **SearchRequest**

``` json
{
    "url": "string",
    "query": "string",
    "search": "string",
    "user_agent": "string",
    "context": "string"
}
```

### **Responses:**

#### **SUCCESS**

``` json
{
    "url": "string",
    "user_agent": "string",
    "context": "string",
    "ads": [
        {
            "name": "string",
            "destination_url": [
                "string"
                ],
            "words": [
                "string"
                ],
            "screenshot_ads": "string"
        }
    ]
}
```

#### **FAILURE**

``` json
{
    "detail": "string",
    "code": int
}
```

### **Workflow:**

source code: *`routes.py`*

#### **1. URL serialization:**

Get request field `url` and parse it into `AddressModel` object.
Serialization function raises ValueError if regex matching does not return any match result, so then API returns `HTTP 400 Bad Request Error`.

``` python
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
```

#### **2. Adds detection**

Get detected advertisements list with using function explained in `api/utils`.
Firstly, there is being detected webservice type (google, bing, onet) by its domain and run appropriate detection script accordingly with its type.

``` python
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
```

#### **3. Response build**

Fullfill `AdvertModel` attributes with auxillary utils scripts.

First of all, there is getting text from image source with OCR alghorithm.

Nextly, with NLTK module keywords are being retrieved and ad is being filtered from result set according to query request param.

If keywords suited to query or query is None, redirection urls are being collected with Python `requests` module with header `referer` field included.

At the end, there is response creating to normalize collected data to appropriate form of `ResponseModel`.

``` python
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
            ad.destination_url = get_destination_urls(ad.url, data.user_agent, f'{address.protocol}://{address.domain}')
            
            print('    - Unique ad name generating...', file=sys.stderr)
            ad.name = f"Ad#{i}"
            
            ads_list.append(ad.to_dict)
        
        return create_response(data, ads_list)
```

---
