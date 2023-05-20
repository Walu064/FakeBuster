import os
import sys

cwd = os.path.dirname(os.path.realpath(__file__))
api_dir = os.path.dirname(os.path.dirname(os.path.dirname(cwd)))
sys.path.append(api_dir)

from models import AdvertModel, DefaultRequestModel


def facebook_detect(data : DefaultRequestModel) -> list[AdvertModel]:
    raise NotImplementedError()


def linkedin_detect(data : DefaultRequestModel) -> list[AdvertModel]:
    raise NotImplementedError()


def youtube_detect(data : DefaultRequestModel) -> list[AdvertModel]:
    raise NotImplementedError()
