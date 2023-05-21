# Utils

## *Description:*

Core functionalities of FakeBuster solution.

Contains various advertisement detection scripts depends on its webservice type (google, bing, youtube, onet...).

Here is also OCR implementation, filtering text by keywords.

---

## *Content:*

- ### [**Detectors**](https://github.com/Walu064/FakeBuster/tree/master/docs/api/utils/detectors)

- ### [**Text Processing**](https://github.com/Walu064/FakeBuster/tree/master/docs/api/utils/text_processing)

---

## *Source*

### File: *`url_serial.py`*

URL serialization - parsing url string into `AddressModel` object using REGEX implementation for further works.

``` python
def __serialize(url : str) -> AddressModel:
    line = url
    isWWW = False
    prot = ""
    domain = ""
    theme = ""
    tail = ""
    query_params = []
    
    # URL normalization for regex check
    if url.count('/') == 2:
        url += '/'
    elif url.count('/') > 2:
        if url.count('?') == 0:
            if url[-1] != '/':
                url += '/?'
            else:
                url += '?'
    
    regex = r"^(?P<protocol>.+):\/\/(www\.){0,1}(?P<domain>.+?\/){1}(?P<rest>.*?)$"
    result = re.match(regex, url)
    
    if result:
        prot = result.group('protocol')
        domain = result.group('domain')
        rest = result.group('rest')
        
        if ((prot.__eq__('http')) or (prot.__eq__('https'))):
            isWWW = True
            
        if len(rest) > 0:
            try:
                theme = rest.split('?', 1)[0]
                tail = rest.split('?', 1)[1]
                
                if len(tail) > 0:
                    try:
                        params = tail.split('&')
                        for param in params:
                            name = param.split('=', 1)[0]
                            
                            try:
                                value = param.split('=', 1)[1]
                            except IndexError:
                                value = True
                                
                            query_params.append(QueryParamModel(name, value))
                            
                    except IndexError:
                        tail = ""
                
            except IndexError:
                theme = rest
                tail = ""
                
        else:
            theme = ""
            tail = ""
        
    else:
        raise ValueError(f'Url Validation: `{url}` does not match {regex}')
    
    return AddressModel(line, isWWW, prot, domain, theme, tail, query_params)
    

def url_serialize(url : str) -> AddressModel:
    try:
        address = __serialize(url)
        return address
    
    except ValueError:
        raise

```

---

### File: *`detect.py`*

Advertisement detect main entrypoint : There is webservice type detection and appropriate detection script call.

Webservice entrypoint is being determined by its domain.

``` python
class DetectionType(Enum):
    INFO_DEFAULT    = 1
    SEARCH_GOOGLE   = 2
    SEARCH_BING     = 3
    SOCIAL_FACEBOOK = 4
    SOCIAL_LINKEDIN = 5
    SOCIAL_YOUTUBE  = 6


_domains = {
    'google'    : DetectionType.SEARCH_GOOGLE,
    'bing'      : DetectionType.SEARCH_BING,
    'facebook'  : DetectionType.SOCIAL_FACEBOOK,
    'linkedin'  : DetectionType.SOCIAL_LINKEDIN,
    'youtube'   : DetectionType.SOCIAL_YOUTUBE,
}


def get_detection_type(domain : str) -> DetectionType:
    for key, value in _domains.items():
        if domain.startswith(key):
            return value
    else:
        return DetectionType.INFO_DEFAULT


def adds_detect(data : DefaultRequestModel | SearchRequestModel, address : AddressModel):
    adds_list : list[AdvertModel]
    
    print('   - Recognizing webservice type...', file=sys.stderr)
    det_type = get_detection_type(address.domain)
    
    print('   - Main detect job...', file=sys.stderr)
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
        case _:
            adds_list = info_detector.info_detect(data)

    return adds_list
```

---

### File: *`redirections.py`*

Redirection chain get function with Python `requests` module. 

Firstly, the http session is being established with updated header field `referer` and `User-Agent`.

Nextly, the response history is being browsed and all urls are being collected to specified list.

``` python
import requests


def get_destination_urls(url : str, user_agent : str, referer : str) -> list[str]:
    with requests.Session() as session:
        session.headers.update({
            "User-Agent" : user_agent,
            "referer" : referer,
        })
        r = session.get(url)
        
        if r.status_code != 200:
            raise requests.exceptions.HTTPError(f"Invalid HTTP status: GET {url} --> {r.status_code}")
        
        dest_urls : list[str] = []
        
        if r.history:
            for step in r.history:
                dest_urls.append(step.url)
        
        dest_urls.append(r.url)
        
        return dest_urls[::-1]
```
