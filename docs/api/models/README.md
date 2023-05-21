# Models

## **Description:**

Directory contains datamodels used as request, response sheet.

---

## **Data Models:**

### **Requests**

#### **DefaultRequestModel**

Default request sheet:

``` json
{
    "url": "https://onet.pl",
    "query": "Inwestycje w złoto",
    "user_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "context": ""
}
```

#### **SearchRequestModel**

Request model used with searchengines:

``` json
{
    "url": "https://www.google.com/search?q=baltic+pipe",
    "search": "baltic pipe",
    "query": "Dochód pasywny",
    "user_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "context": ""
}
```

File: *`requests.py`*

``` python
class DefaultRequestModel(BaseModel):
    url : str
    query : str
    user_agent : str
    context : str

    class Config:
        schema_extra = {
            "example" : {
                "url" : "https://onet.pl",
                "query" : "Inwestycje w złoto",
                "user_agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
                "context" : "",
            },
        }


class SearchRequestModel(BaseModel):
    url : str
    search : str
    query : str
    user_agent : str
    context : str

    class Config:
        schema_extra = {
            "example" : {
                "url" : "https://www.google.com/search?q=baltic+pipe",
                "search" : "baltic pipe",
                "query" : "Dochód pasywny",
                "user_agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
                "context" : "",
            },
        }
```

---

### **Responses**

#### **ResponseModel**

Successful response sheet:

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

#### **ErrorResponseModel**

Error response model:

``` json
{
    "detail": "string",
    "code": 0
}
```

File: *`responses.py`*

``` python
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
```

### **Advertisements**

Named tuple class model for advertisement processing and data storage.

File: *`advert.py`*

``` python
class AdvertModel(NamedTuple):
    url : str
    name : str
    destination_url : List[str]
    words : List[str]
    screenshot_ads : str
    
    def to_dict(self) -> dict:
        return {
                "name" : self.name,
                "destination_url" : self.destination_url,
                "words" : self.words,
                "screenshot_ads" : self.screenshot_ads
            }
```

### **Address**

Named tuple class model used for url serialization and storage information about website protocol, domain, params etc.

File: *`address.py`*

``` python
class QueryParamModel(NamedTuple):
    name : str
    value : any
    

class AddressModel(NamedTuple):
    line : str
    isWWW : bool
    protocol : str
    domain : str
    theme : str
    tail : str
    query_params : list[QueryParamModel]
```
