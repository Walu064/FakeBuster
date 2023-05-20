from fastapi import FastAPI

from .routes import adds_router
from ._meta import (TITLE,
                    DESCRIPTION,
                    VERSION,
                    TAGS_METADATA)


def init_api() -> FastAPI:
    api = FastAPI(
        title=TITLE,
        description=DESCRIPTION,
        version=VERSION,
        openapi_tags=TAGS_METADATA
    )
    
    api.include_router(adds_router)
    
    return api
