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


class Crawler:
    def __init__(self):
        self.consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        self.access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
        self.client = oauth.Client(self.consumer, self.access_token)
        self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_KEY, ACCESS_SECRET) 
        self.api = tweepy.API(self.auth,wait_on_rate_limit=True)

    
    def get_tweets(self,query_string):
        tweets,locations=[],[]
        for _c in range(random.randrange(10,16)):
            fetched_tweets = self.api.search(q = query_string, count = 200)
            tweets.extend(list(map(lambda x:x.text,fetched_tweets)))
            locations.extend(list(map(lambda x:x.user.location,fetched_tweets)))
        
        return {"tweet":tweets,"location":locations}