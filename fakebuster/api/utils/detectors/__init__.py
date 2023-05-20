from enum import Enum


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
    for i, key, value in enumerate(_domains.items()):
        if domain.startswith(key):
            return value
    else:
        return DetectionType.INFO_DEFAULT
