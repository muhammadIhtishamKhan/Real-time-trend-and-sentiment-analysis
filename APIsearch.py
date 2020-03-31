import tweepy
import pymongo
import json
from tweepy import Stream
from tweepy import OAuthHandler
from pymongo import MongoClient
from tweepy.streaming import StreamListener
import datetime

def get_tweets(query):
    # call twitter api to fetch tweets
    q = str(query)
    a = str(q + " donald trump")
    language = ['en']

    # parsing tweets one by one
    for data in tweepy.Cursor(api.search,q='Donald Trump',since='2019-15-01',until='2019-20-03',lang='en').items(200):
    #fetched_tweets = api.search(a, count=150000)
    #for data in fetched_tweets:
        print(data)
        t = json.loads(data)

        # Pull important data from the tweet to store in the database.
        tweet_id = t['id_str']  # The Tweet ID from Twitter in string format
        username = t['user']['screen_name']  # The username of the Tweet author
        followers = t['user']['followers_count']  # The number of followers the Tweet author has
        text = t['text']  # The entire body of the Tweet
        hashtags = t['entities']['hashtags']  # Any hashtags used in the Tweet
        dt = t['created_at']  # The timestamp of when the Tweet was created
        language = t['lang']  # The language of the Tweet

        # Convert the timestamp string given by Twitter to a date object called "created". This is more easily manipulated in MongoDB.
        created = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')

        # Load all of the extracted Tweet data into the variable "tweet" that will be stored into the database
        tweet = {'id': tweet_id, 'username': username, 'followers': followers, 'text': text, 'hashtags': hashtags,
                 'language': language, 'created': created}

        # Save the refined Tweet data to MongoDB
        coll.save(tweet)
if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client['rawtweets']
    coll = db['coronavirus']
    CONSUMER_KEY = "KMVnf0sl6m8Bwzw7RIGmwD1B0"
    CONSUMER_SECRET = "26gNHbPlt0tdNwPuargNACQ9ZxoF3mPt6MEDH8yvy9knhG2fMM"
    ACCESS_TOKEN = "529229540-5b28dYL4csa9HuNEf6tLUxtHyL6FkXh41Z2DMpMP"
    ACCESS_TOKEN_SECRET = "zj0t9hvwyD01OdIgh8M0oWhtKPxUCCe6Cc0d28X7JP1iu"
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    print("I reached")
    get_tweets("")
