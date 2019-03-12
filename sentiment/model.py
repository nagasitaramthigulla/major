from keras.models import Sequential
from keras.layers import Dense,Embedding,LSTM,SpatialDropout1D,Input
import ipdb

def get_model()->Sequential:
    # ipdb.set_trace()
    model=Sequential()
    model.add(Embedding(20000,32,input_length=60))
    model.add(LSTM(100))
    model.add(Dense(2,activation='sigmoid'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

def get_model2()->Sequential:
    embed_dim=64
    lstm_out=100
    model=Sequential()
    model.add(Embedding(50000,embed_dim,input_length=60))
    model.add(SpatialDropout1D(.4))
    model.add(LSTM(lstm_out))
    model.add(Dense(2,activation='sigmoid'))
    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['acc'])
    
    return model