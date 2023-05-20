import pandas
from fuzzywuzzy import fuzz

def keywords_filter(phrase : str, text : str):
    similarity = fuzz.partial_ratio(phrase, text)
    return similarity

test = keywords_filter("Big tits", "Hot moms area ! Enlarge your penis !")
print(test)

