from queue import Queue

from threading import Thread,Lock,Condition

from sentiment.sentimentAnalyser import SentimentAnalyser

import matplotlib.pyplot as plt

from sentiment.model import get_model2 as get_model
import numpy as np
import asyncio
from tweetCrawler.crawler import Crawler #,get_tweets
import os,time

CWD=os.environ['CWD']

import tensorflow as tf

import keras.backend as K

import ipdb

import datetime

import time
import json
import re
from wordcloud import  WordCloud
from textblob import TextBlob 

def preprocess(text):
    text=str(text).lower()
    text=re.sub('[^a-zA-Z0-9\s]',"",text)
    return text

class Worker(Thread):
    def __init__(self,tasks:Queue,lock:Lock,condition:Condition,id:int):
        Thread.__init__(self)
        self.tasks=tasks
        self.lock=lock
        self.condition=condition
        self.graph=tf.get_default_graph()
        self.id=id
        self.sentimentAnalyser=SentimentAnalyser(get_model())
        self.crawler=Crawler()
        self.daemon=True
        self.start()

    def run(self):
        while True:

            self.condition.acquire()
            while self.tasks.empty():
                print("waiting:",self.id)
                self.condition.wait()
            try:
                search_key,client,socketio = self.tasks.get()
                self.tasks.task_done()
                print("key:",search_key,"thread:",self.id)
            except:
                self.condition.release()
                continue
            self.condition.release()

            if os.path.exists(CWD+'\\results\\'+search_key+'.json'):
                self.lock.acquire()
                socketio.emit('result',{'id':search_key},room=client)
                self.lock.release()
                continue

            df = self.crawler.get_tweets(search_key)

            df['location']=list(map(lambda x:x.split(',')[-1].lower(),df['location']))
            df['tweet']=list(map(preprocess,df['tweet']))

            wordCloudText=" ".join(df['tweet'])

            with self.graph.as_default():
                # prediction = np.array(list(map(lambda x:x,self.sentimentAnalyser.performAnalysis(df['tweet']))))
                prediction = np.array(list(map(lambda x:list(x).index(max(x)),self.sentimentAnalyser.performAnalysis(df['tweet']))))
                pass
            
            maps={0:{},1:{}}

            for i in range(len(df['location'])):
                maps[prediction[i]][df['location'][i]]=maps[prediction[i]].get(df['location'][i],0)+1
            map_loc=[]
            for i in maps:
                map_loc.extend([[location,int(i),int(count)] for location,count in maps[i].items()])
            map_loc.sort(key=lambda x:x[-1],reverse=True)
            map_loc=[['Location','Polarity','Count']]+map_loc
            res=np.unique(prediction,return_counts=True)
            res_d={}
            for i in range(len(res[0])):
                res_d[res[0][i]]=res[1][i]
            counts=[["Polarity","Count"],["negative",int(res_d.get(0,0))],['positive',int(res_d.get(1,0))]]

            with open(CWD+'\\results\\'+search_key+".json",'w') as f:
                json.dump({'search_key':search_key,'map':map_loc,'counts':counts},f)

            print(res)

            self.lock.acquire()


            wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(wordCloudText)

            plt.figure(figsize=(10, 7))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis('off')
            plt.savefig(CWD+'\images\{}.png'.format(search_key))
            socketio.emit('result',{'id':search_key},room=client)
            self.lock.release()
            continue

            self.lock.acquire()

            plt.pie(res[1],labels=res[0],colors=['red','green'])

            my_circle=plt.Circle( (0,0), 0.7, color='white')
            p=plt.gcf()
            p.gca().add_artist(my_circle)
            file_name = "{}{}".format(str(search_key),datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            plt.savefig(CWD+'\images\pie\{}.png'.format(file_name))
            plt.clf()
            socketio.emit('result',{'id':file_name},room=client)
            self.lock.release()


class ThreadPool:
    def __init__(self,num_threads:int):
        self.num_threads=num_threads
        self.tasks=Queue()
        self.lock=Lock()
        self.condition=Condition()
        self.workers=[Worker(self.tasks,self.lock,self.condition,i+1) for i in range(num_threads)]

    def put(self,task):
        self.tasks.put(task)

class CleanerThread(Thread):
    
    def run(self):
        while True:
            path=CWD+"\\images"
            now=time.time()
            for f in os.listdir(path):
                f = os.path.join(path, f)
                if os.stat(f).st_mtime<now-86400:
                    os.remove(f)
            path=CWD+"\\results"
            for f in os.listdir(path):
                f=os.path.join(path, f)
                if os.stat(f).st_mtime<now-86400:
                    os.remove(f)
            time.sleep(3600)
            
