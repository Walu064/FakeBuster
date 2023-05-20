import os
import sys

cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(os.path.dirname(os.path.dirname(cwd)))
sys.path.append(api_dir)

from models import AdvertModel, SearchRequestModel
from conf.config import SCREENSHOTS_DIR


# AdvertModel object attrs to fullfuill:
#   - url : advertisement url
#   - words (partially : raw div text)
#   - screenshot_ads : copy img source to SCREENSHOT_DIR and store path
# 
# Other attrs:
#   - name : str = ""
#   - words : list[str] = []
#   - destination_url : list[str] = []

def bing_detect(data : SearchRequestModel) -> list[AdvertModel]:
    # TODO: Bing search engine ads detection
    raise NotImplementedError()


def google_detect(data : SearchRequestModel) -> list[AdvertModel]:
    # TODO: Google search engine ads detection
    raise NotImplementedError()
