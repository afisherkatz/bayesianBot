import sys
import twitter
import random
from twitterCredentials import consumer_key, consumer_secret, access_token_key, access_token_secret


class MarkovBot(object):

    """
        Class which creates api connection to twitter in order to gather tweets from a hashtag, which are then used
        to create a dictionary of markov chains that can create fake tweets charactaristic of that hashtag
    """

    def __init__(self, **hashtag):
        
        """
            Initialize class object with blank dictionary and word list. Create api connection from credentials
            in twitterCredentials (NOTE: DO NOT PUSH twitterCredentials.py EVER!!).

            Optional hashtag specification, if given will generate dictionary and word list for hashtag
        """
        
        self.dictionary = {}
        self.words = {}
        self.api = self.getAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
        if ('hashtag' in hashtag):
            self.getTweets(hashtag['hashtag'])

    def getAPI(self, c_key, c_secret, a_token_key, a_token_secret):
        
        """
            Log in to api with credentials, or raise exception
        """

        api = twitter.Api(consumer_key = c_key, consumer_secret = c_secret, access_token_key = a_token_key, access_token_secret = a_token_secret)

        try:
            api.VerifyCredentials()
        except:
            sys.exit("Invalid twitter credentials")

        return api

    def getTweets(self, hashtag, num = 100):

        """
            Get tweets from a hashtag and generate markov dictionary and word list

            TODO: API limits tweet queries to returning 100 results. To increase this number, need to create seperate tweet 
            query function
        """

        results = [results.text for results in self.api.GetSearch(raw_query = "q=%23" + hashtag + "&count=" + str(num))]
        
        # Append top word list if hashtag already created
        if hashtag in self.words:
            self.words[hashtag].append([word for result in results for word in result.split(" ")])
        else:
            self.words[hashtag] = [word for result in results for word in result.split(" ")]

        tweets = [tweet.split(" ") for tweet in results]
        self.dictionary[hashtag] = {}
        self.makeDictionary(tweets, hashtag)

    def makeDictionary(self, tweets, hashtag):

        """
            Create Markov chain dictionary by creating a structure that creates a list of every set of three consecutive
            words, which are then turned into a dictionary with the key being the tuple of each two beginning words.

            EXAMPLE: "this is a dictionary entry it is a good one" would produce 
                {
                    ('this', 'is'): 'a', 
                    ('is', 'a'): ['dictionary', 'good'], 
                    ('a', 'dictionary'): 'entry',
                    ('dictionary', 'entry'): 'it',
                    ('entry', 'it'): 'is',
                    ('it', 'is'): 'a',
                    ('a', 'good'), 'one'
                }
        """

        threes = [list(zip(a[0:-2], a[1:-1], a[2:])) for a in tweets]
        for tweet in threes:    
            for w1, w2, w3 in tweet:
                key = (w1, w2)
                if key in self.dictionary[hashtag]:
                    self.dictionary[hashtag][key].append(w3)
                else:
                    self.dictionary[hashtag][key] = [w3]

    def markov_tweet(self, hashtag, length=20):
        tweet = ''
        if hashtag in self.dictionary:
            seed = random.randint(0, len(self.words[hashtag]) - 3)
            w1, w2 = self.words[hashtag][seed], self.words[hashtag][seed + 1]
            tweet = w1 + " " + w2
            for i in range(0, length):
                if (w1, w2) in self.dictionary[hashtag]:
                    w1, w2 = w2, random.choice(self.dictionary[hashtag][(w1, w2)])
                    tweet += " " + w2
                else:
                    return tweet
            return tweet
        else:
            self.getTweets(hashtag)
            return "No tweet data, dictionary updated"
