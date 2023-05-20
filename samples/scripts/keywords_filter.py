import os
import pandas
from fuzzywuzzy import fuzz 

phrases_test = ["cryptocurrency", "bitcoin", "money", "investments"]
path_test = os.path.join("..", "data", "learn_fake_data.csv")
ads_frame = pandas.read_csv(path_test)
ads_test = ads_frame['content']

def keywords_filter(phrases: list, ads_text: list):
    query = " ".join(phrases)
    for ad_text in ads_text:
        similarity_value = fuzz.ratio(query, ad_text)
        print("\nPHRASE: " + query)
        print("AD_TEXT: " + ad_text)
        print("Ad similar in " + str(similarity_value) + " percent.")

keywords_filter(phrases_test, ads_test)
