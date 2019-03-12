from sentiment.model import get_model

import theano

theano.config.cxx=''


import numpy as np
import keras as K
import pandas as pd
import os

model = get_model()
mp = "imdb_model20000.h5"
model.load_weights(mp)
d = K.datasets.imdb.get_word_index()
x=input('enter text:')
while len((x))>2:
    review = x
    words = review.split()
    review = []
    for word in words:
        if word not in d: 
            review.append(2)
        elif d[word]+3<20000:
            review.append(d[word]+3)

    print(review)

    review = K.preprocessing.sequence.pad_sequences([review],truncating='pre', padding='pre', maxlen=60)

    prediction=model.predict(review)

    print(prediction)
    x=input('enter text:')
