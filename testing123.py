from tweepy import Stream
from tweepy import OAuthHandler
from pymongo import MongoClient
import tweepy
import pymongo
import json


client = MongoClient('localhost', 27017)
db = client['rawtweets']
coll = db['alpha']
CONSUMER_KEY = "KMVnf0sl6m8Bwzw7RIGmwD1B0"
CONSUMER_SECRET = "26gNHbPlt0tdNwPuargNACQ9ZxoF3mPt6MEDH8yvy9knhG2fMM"
ACCESS_TOKEN = "529229540-5b28dYL4csa9HuNEf6tLUxtHyL6FkXh41Z2DMpMP"
ACCESS_TOKEN_SECRET = "zj0t9hvwyD01OdIgh8M0oWhtKPxUCCe6Cc0d28X7JP1iu"