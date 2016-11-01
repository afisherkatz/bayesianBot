import sys
import twitter
from twitterCredentials import consumer_key, consumer_secret, access_token_key, access_token_secret
import random

class MarkovBot(object):


    def __init__(self, hashtag):
        self.hashtag = hashtag
        self.api = self.getAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
         

    def getAPI(self, c_key, c_secret, a_token_key, a_token_secret):
        
        api = twitter.Api(consumer_key = c_key, consumer_secret = c_secret, access_token_key = a_token_key, access_token_secret = a_token_secret)

        try:
            api.VerifyCredentials()
        except:
            sys.exit("Invalid twitter credentials")

        return api

    def getTweets(self, hashtag = self.hastag):
        results = [str(result.text).encode('utf-8') for result in api.GetSearch(raw_query = "q=%23" + hashtag + "&count=" + num)]
        return results
