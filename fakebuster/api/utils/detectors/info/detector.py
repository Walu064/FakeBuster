import os
import sys

cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(os.path.dirname(os.path.dirname(cwd)))
sys.path.append(api_dir)

from models import AdvertModel, DefaultRequestModel
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

def info_detect(data : DefaultRequestModel) -> list[AdvertModel]:
    # TODO: Info Webservices ads detection
    raise NotImplementedError()
