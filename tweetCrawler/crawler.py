import oauth2 as oauth
import json
from .config import *
import random
from twitterscraper import query
import pandas as pd
import requests
from urllib.parse import urlencode

class Crawler:
    def __init__(self):
        self.consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        self.access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
        self.client = oauth.Client(self.consumer, self.access_token)

    def tweet_stream(self,base_url='https://api.twitter.com/1.1/search/tweets.json', query=None):
        base_query=query
        for _c in range(random.randrange(40,100)):
            if query == None:
                print(_c,base_query,1)
                return
            url, query = base_url + query, None
            response = self.client.request(url)
            if response[0]['status']!="200":
                print(_c,base_query,response[0]['status'])
                return
            result = json.loads(response[1])
            yield result['statuses']
            if 'next_results' not in result['search_metadata']:
                print(_c,base_query,3)
                return
            query = result['search_metadata']['next_results']


    def get_tweets(self,query_string):
        tweets=[]
        locations=[]
        res=query.query_tweets(query_string,limit=random.randrange(1000,1500),poolsize=4,lang="en")
        tweets=[tweet.text for tweet in res]
        uids=list(set([tweet.user for tweet in res]))
        uids=[uids[i:i+95] for i in range(0,len(uids),95)]
        users={}
        for uid in uids:
            uid=",".join(uid)
            resp=self.client.request("https://api.twitter.com/1.1/users/lookup.json",method="POST",body=urlencode({"user_id":uid,"include_entities":"false"}))
            for u in json.loads(resp[1]):
                users[u['id_str']]=u.get("location","")
        locations=[users[tweet.user] for tweet in res]
        return {"tweet":tweets,"location":locations}
