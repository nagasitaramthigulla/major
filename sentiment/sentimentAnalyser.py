import numpy as np
import keras as K
import os
from keras.preprocessing.text import Tokenizer
import pickle

import ipdb

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def processtweet(tweet,d):
    words = tweet.split()
    tweet = []
    for word in words:
        if word not in d: 
            tweet.append(2)
        elif d[word]+3<20000:
            tweet.append(d[word]+3)
    return tweet

class SentimentAnalyser:
    def __init__(self,model):
        self.model=model
        self.model.load_weights(os.environ['CWD']+'\model.h5')
        self.d = K.datasets.imdb.get_word_index()
        with open('tokenizer.pkl','rb') as f:
            self.tokenizer=pickle.load(f)

    def performAnalysis(self,tweets):
        processedtweets = K.preprocessing.sequence.pad_sequences(self.tokenizer.texts_to_sequences(tweets),truncating='pre', padding='pre', maxlen=60)
        # ipdb.set_trace()
        prediction = self.model.predict(processedtweets)
        return prediction

