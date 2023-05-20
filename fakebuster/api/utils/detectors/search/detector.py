import os
import sys

cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(os.path.dirname(os.path.dirname(cwd)))
sys.path.append(api_dir)

from models import AdvertModel, SearchRequestModel


def bing_detect(data : SearchRequestModel) -> list[AdvertModel]:
    raise NotImplementedError()


def google_detect(data : SearchRequestModel) -> list[AdvertModel]:
    raise NotImplementedError()

