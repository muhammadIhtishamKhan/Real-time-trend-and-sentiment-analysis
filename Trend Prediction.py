import string
import pymongo
import csv
import json
import tweepy
from nltk.corpus import stopwords
from pymongo import MongoClient
import sys,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
from bson import json_util
import nltk
import datetime
import matplotlib.pyplot as plt

CONSUMER_KEY = "KMVnf0sl6m8Bwzw7RIGmwD1B0"
CONSUMER_SECRET = "26gNHbPlt0tdNwPuargNACQ9ZxoF3mPt6MEDH8yvy9knhG2fMM"
ACCESS_TOKEN = "529229540-5b28dYL4csa9HuNEf6tLUxtHyL6FkXh41Z2DMpMP"
ACCESS_TOKEN_SECRET = "zj0t9hvwyD01OdIgh8M0oWhtKPxUCCe6Cc0d28X7JP1iu"
client = MongoClient('localhost', 27017)
db = client['rawtweets']
coll = db['coronavirus']

i = 0
times = []
momentumAxis = []

for doc in db.coronavirus.find():
    tweetCreated = doc['created']
    times.append(tweetCreated)

originalTimes = times

initial = times[0]
windows = []
k = 7
temp = []

for t in times:
    x = (t-initial).seconds / 60
    if x < k:
        temp.append(t)
    else:
        initial = t;
        windows.append(temp)
        temp = []

#print("Total tweets divided in parts = " , len(windows))
'''***********************************************************************************'''
for timeWindow in windows:
    #print(timeWindow[0])
    times = timeWindow
    if len(times) < 1:
        continue
    initial = times[0]
    smallWindow = []
    k = 1
    temp = []

    for t in times:
        x = (t-initial).seconds / 60


        if x < k:
            temp.append(t)
        else:
            initial = t;
            smallWindow.append(temp)
            temp = []

    if len(temp) > 0:
        smallWindow.append(temp)

    n = len(smallWindow)    # last window
    i = n - k + 1
    frequencyOfKeywordInWindow = 0
    MAnks = 0

    if n < k:
        for i in range(n):
            frequencyOfKeywordInWindow += len(smallWindow[i])

        MAnks = frequencyOfKeywordInWindow / k

    else:
        i = 1
        for i in range(n):
            frequencyOfKeywordInWindow += len(smallWindow[i])

        MAnks = frequencyOfKeywordInWindow / n

   # print("MAnks = ", MAnks)
    '''***********************************************************************************'''

    initial = times[0]
    bigWindow = []
    k = 2
    temp = []

    for t in times:
        x = (t-initial).seconds / 60

        if x < k:
            temp.append(t)
        else:
            initial = t;
            bigWindow.append(temp)
            temp = []

    if len(temp) > 0:
        bigWindow.append(temp)

    n = len(bigWindow)    # last window
    i = n - k + 1
    frequencyOfKeywordInWindow = 0
    MAnkl = 0

    if n < k:
        for i in range(n):
            frequencyOfKeywordInWindow += len(bigWindow[i])

        MAnkl = frequencyOfKeywordInWindow / k

    else:
        i = 1
        for i in range(n):
            frequencyOfKeywordInWindow += len(bigWindow[i])

        MAnkl = frequencyOfKeywordInWindow / n

  #  print("MAnkl = ", MAnkl)
    '''***********************************************************************************'''

    alpha = 0.75
    MAnkl = pow(MAnkl, alpha)
    #print("MAnkl power alpha = ", MAnkl)
    trendMomentum = MAnks - MAnkl

    momentumAxis.append(int(trendMomentum))

    '''********************************END FOR LOOP***************************************************'''

for tm in momentumAxis:
    print(tm)

print("y axis len = ", len(momentumAxis))
# x axis values
timeAxis = [0]

i = 1
for i in range(len(momentumAxis)-1):
    i = i + 7
    timeAxis.append(i)

print("x axis len = ", len(timeAxis))
# plotting the points
plt.plot(timeAxis, momentumAxis)

# naming the x axis
plt.xlabel('Time - axis')
# naming the y axis
plt.ylabel('Momentum - axis')

# giving a title to my graph
plt.title('Trend Momentum of corona virus')
plt.show()