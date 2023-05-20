from typing import NamedTuple, List


class AdvertModel(NamedTuple):
    name : str
    destination_url : List[str]
    words : List[str]
    screenshot_ads : str
    