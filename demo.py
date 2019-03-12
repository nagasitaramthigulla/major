import os
from tweetCrawler.crawler import Crawler
print(os.curdir)
crawler = Crawler()

search_key = input()
query = "?q=%s"%(search_key)
base_url = 'https://api.twitter.com/1.1/search/tweets.json'

res = []

i=0
for batch in crawler.tweet_stream(base_url,query):
    i+=1
    print("batch #%d"%i)
    res.extend(batch)

print("Total batches %d\n Total Tweets %d"%(i,len(res)))
