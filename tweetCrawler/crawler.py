import oauth2 as oauth
import json
from .config import *
import random
from twitterscraper import query
import pandas as pd
import requests
from urllib.parse import urlencode
import tweepy
from tweepy import OAuthHandler 

async def get_country(user,session):
    location=user.get("location","")
    id=user['id_str']
    try:
        async with session.get("https://photon.komoot.de/api/?lang=en&limit=5&q={}".format(location)) as response:
            res=json.loads(response.read())
            return id,res['features'][0]['properties']['country']
    except:
        return id,""

class Crawler:
    def __init__(self):
        self.consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        self.access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
        self.client = oauth.Client(self.consumer, self.access_token)
        self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET) 
        self.api = tweepy.API(self.auth,wait_on_rate_limit=True)

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


    def get_tweets2(self,query_string):
        tweets=[]
        locations=[]
        res=query.query_tweets(query_string,limit=random.randrange(1000,1500),poolsize=10,lang="en")
        tweets=[tweet.text for tweet in res]
        print(len(tweets))
        uids=list(set([tweet.user for tweet in res]))
        uids=[uids[i:i+95] for i in range(0,len(uids),95)]
        users={}
        for uid in uids:
            uid=",".join(uid)
            resp=self.client.request("https://api.twitter.com/1.1/users/lookup.json",method="POST",body=urlencode({"user_id":uid,"include_entities":"false"}))
            usersdata=json.loads(resp[1])
            for u in usersdata:
                users[u['id_str']]=u.get("location","")
        locations=[users[tweet.user] for tweet in res]
        return {"tweet":tweets,"location":locations}

    def get_tweets(self,query_string):
        tweets,locations=[],[]
        for _c in range(random.randrange(10,16)):
            fetched_tweets = self.api.search(q = query_string, count = 200)
            tweets.extend(list(map(lambda x:x.text,fetched_tweets)))
            locations.extend(list(map(lambda x:x.user.location,fetched_tweets)))
        
        return {"tweet":tweets,"location":locations}