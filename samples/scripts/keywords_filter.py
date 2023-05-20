import os
import pandas
import spacy 

nlp = spacy.load('pl_core_news_lg')

phrases_test = ["Wędkarstwo"]
path_test = os.path.join("..", "data", "learn_fake_data.csv")
ads_frame = pandas.read_csv(path_test)
ads_test = ads_frame['content']

def keywords_filter(phrases: list, ads_text: list):
    counter = 0
    #print(str(counter)+" / "+str(len(ads_text)), end='\r')
    query = " ".join(phrases)
    for ad_text in ads_text:
        doc1 = nlp(ad_text)
        doc2 = nlp(query)
        similarity_value = doc1.similarity(doc2) * 100
        if similarity_value >= 30:
            counter = counter +1
            #print(str(counter)+" / "+str(len(ads_text)), end='\r')
            print("\nPHRASE: " + query)
            print("AD_TEXT: " + ad_text)
            print("Ad similar in " + str(similarity_value) + " percent.")
    
    print(str(counter)+" / "+str(len(ads_text)))

keywords_filter(phrases_test, ads_test)
