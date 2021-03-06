#Implementing text cleaning(preprocessing) and mongodb
#1.Import from mongodb
#2. Clean the text
#3 Export to mongodb

import pymongo
import re
from multiprocessing import Pool
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

#define all document
client = pymongo.MongoClient("mongodb://admin:Bigdata123%23@194.233.64.254:27017")
twitterdb = client["twitter2"]
tweet_source = twitterdb["tweetbyuser"]
tweet_destination = twitterdb["tweetprocess2"]

#define abandon sentences
abondon_setences = ["just posted a photo","just posted a video"] 

#Sastrawi
stemmer = StemmerFactory().create_stemmer()
swremoval = StopWordRemoverFactory().create_stop_word_remover()

#Creating function to clean up all text
def preprocess(text):
    text = text.replace("\n"," ")
    textArr = text.split(" ")
    textArr.pop()
    for i,t in enumerate(textArr):
        t = t.lower()
        t = re.sub('[^A-Za-z0-9]+', '', t)
        textArr[i] = t
    if(len(textArr) < 4):
        return None
    textfix = " ".join(textArr)
    #textfix = stemmer.stem(" ".join(textArr))
    #textfix = swremoval.remove(textfix)
    return textfix

def preprocess_all(tweets):
    #Creating some kind of loading bar
    total_doc = tweet_source.estimated_document_count()
    progress = 0

    for tweet in tweets:
        tweet["text"] = preprocess(tweet["text"])
        if(tweet["text"] == None):
            continue
        if(tweet in abondon_setences):
            continue
        #tweet_destination.update_one({'_id': tweet["_id"]},{'$set': tweet}, upsert=True)
        progress = progress+1
        if(progress % 100 == 0):
            print("{} / {}".format(progress, total_doc))



# Get Sample data then pass it to function
tweets = tweet_source.find({},{'text':1,'tkey':1})
tweets_process =  []


print(type(tweets))

