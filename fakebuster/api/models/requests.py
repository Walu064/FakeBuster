from pydantic import BaseModel


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
