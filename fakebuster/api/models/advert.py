from typing import NamedTuple, List


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
    