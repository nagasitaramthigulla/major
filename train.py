from sentiment.model import get_model

import theano

theano.config.cxx=''


import numpy as np
import keras as K
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
(train_x, train_y), (test_x, test_y) = \
    K.datasets.imdb.load_data(seed=1, num_words=20000)
max_review_len = 60
train_x = K.preprocessing.sequence.pad_sequences(train_x,truncating='pre', padding='pre', maxlen=max_review_len)  # pad and chop!
test_x = K.preprocessing.sequence.pad_sequences(test_x,truncating='pre', padding='pre', maxlen=max_review_len)

train_y=pd.get_dummies(train_y).values

test_y=pd.get_dummies(test_y).values

model = get_model()

model.fit(train_x,train_y,epochs=3,batch_size=32,shuffle=True,verbose=1)

loss_acc = model.evaluate(test_x, test_y, verbose=1)

print("Test data: loss = %0.6f  accuracy = %0.2f%% " % (loss_acc[0], loss_acc[1]*100))
mp = "imdb_model20000.h5"
model.save(mp) 
d = K.datasets.imdb.get_word_index()
x=input()
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

    review = K.preprocessing.sequence.pad_sequences([review],truncating='pre', padding='pre', maxlen=max_review_len)

    prediction=model.predict(review)

    print(prediction)
    x=input()
