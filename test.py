import tweepy
import pymongo
import json
from tweepy import Stream
from tweepy import OAuthHandler
from pymongo import MongoClient
from tweepy.streaming import StreamListener
import datetime
global max_tweets
# The MongoDB connection info.
client = MongoClient('localhost', 27017)
db = client['rawtweets']
coll = db['coronavirus']
CONSUMER_KEY = "KMVnf0sl6m8Bwzw7RIGmwD1B0"
CONSUMER_SECRET = "26gNHbPlt0tdNwPuargNACQ9ZxoF3mPt6MEDH8yvy9knhG2fMM"
ACCESS_TOKEN = "529229540-5b28dYL4csa9HuNEf6tLUxtHyL6FkXh41Z2DMpMP"
ACCESS_TOKEN_SECRET = "zj0t9hvwyD01OdIgh8M0oWhtKPxUCCe6Cc0d28X7JP1iu"
# Add the keywords you want to track. They can be cashtags, hashtags, or words.
keywords = ['coronavirus']

# Optional - Only grab tweets of specific language
language = ['en']

class StdOutListener(StreamListener):

   # def __init__(self, api=None):
    #    self.counter = 0

    def on_data(self, data):

        # Load the Tweet into the variable "t"
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
        tweet = {'id':tweet_id, 'username':username, 'followers':followers, 'text':text, 'hashtags':hashtags, 'language':language, 'created':created}
        print(tweet)
        # Save the refined Tweet data to MongoDB
        coll.save(tweet)
        # Optional - Print the username and text of each Tweet to your console in realtime as they are pulled from the stream
        #print (username + ':' + ' ' + text)
        #if self.counter >= max_tweets:
         #   stream.disconnect()
        return True


if __name__ == '__main__':
    #max_tweets = int(input("Enter max Number of tweets"))
    l = StdOutListener()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    stream = Stream(auth, l)
    stream.filter(track=keywords, languages=language)