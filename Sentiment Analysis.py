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



class SentimentAnalysis:


    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def getData(self):
        global emoticons
        global emoji_pattern
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        global emoticons_happy
        emoticons_happy = set([
            ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
            ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
            '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
            'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
            '<3'
        ])
        global emoticons_sad
        emoticons_sad = set([
            ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
            ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
            ':c', ':{', '>:\\', ';('
        ])
        CONSUMER_KEY = "KMVnf0sl6m8Bwzw7RIGmwD1B0"
        CONSUMER_SECRET = "26gNHbPlt0tdNwPuargNACQ9ZxoF3mPt6MEDH8yvy9knhG2fMM"
        ACCESS_TOKEN = "529229540-5b28dYL4csa9HuNEf6tLUxtHyL6FkXh41Z2DMpMP"
        ACCESS_TOKEN_SECRET = "zj0t9hvwyD01OdIgh8M0oWhtKPxUCCe6Cc0d28X7JP1iu"
        client = MongoClient('localhost', 27017)
        db = client['rawtweets']
        coll = db['brexit']
        file = open('test12345.csv', 'a+')

        csvWriter = csv.writer(file)


        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0
        counter=0



        # combine sad and happy emoticons
        emoticons = emoticons_happy.union(emoticons_sad)
        NoOfTerms=coll.count()
        print ("total tweets: ",NoOfTerms)
        for doc in db.brexit.find():
            counter=counter+1
            print("Original Tweet: ", doc['text'])
            cleanT=self.clean_Tweet(doc['text'])
            cleanT=self.cleanTweet(cleanT)
            self.tweetText.append(doc['text'].encode('utf-8'))
            #cleanT=str(cleanT)
            print("Clean Tweet: ", cleanT)
            analysis = TextBlob(cleanT)
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral =neutral+ 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.5):
                wpositive =wpositive+ 1
            elif (analysis.sentiment.polarity > 0.5 and analysis.sentiment.polarity <= 1):
                spositive =spositive+ 1
            elif (analysis.sentiment.polarity > -0.5 and analysis.sentiment.polarity <= 0):
                wnegative =wnegative+ 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.5):
                snegative =snegative + 1


            # Write to csv and close csv file

        csvWriter.writerow(self.tweetText)
        file.close()

            # finding average of how people are reacting
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

            # finding average reaction
        polarity = polarity / NoOfTerms
        print("How people are reacting on Brexit by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("Detailed Report: ")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")
        searchTerm="Imran Khan"
        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)
    def cleanTweet(self, tweet):

        stop_words = set(stopwords.words('english'))
        word_tokens = nltk.word_tokenize(tweet)
        # after tweepy preprocessing the colon symbol left remain after      #removing mentions
        tweet = re.sub(r':', '', tweet)
        tweet = re.sub(r'‚Ä¶', '', tweet)
        # replace consecutive non-ASCII characters with a space
        tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)
        # remove emojis from tweet
        tweet = emoji_pattern.sub(r'', tweet)
        # filter using NLTK library append it to a string
        filtered_tweet = [w for w in word_tokens if not w in stop_words]
        filtered_tweet = []
        # looping through conditions
        for w in word_tokens:
            # check tokens against stop words , emoticons and punctuations
            if w not in stop_words and w not in emoticons and w not in string.punctuation:
                filtered_tweet.append(w)
        return ' '.join(filtered_tweet)

    def clean_Tweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

        # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * (float(part) / float(whole))
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm,
                         noOfSearchTerms):
        labels = ['Strongly Positive [' + str(spositive) + '%]','Weakly Positive [' + str(wpositive) + '%]',
                       'Neutral [' + str(neutral) + '%]',
                      'Weakly Negative [' + str(wnegative) + '%]',
                      'Strongly Negative [' + str(snegative) + '%]']
        sizes = [spositive, wpositive, neutral, wnegative, snegative]
        colors = ['darkgreen', 'lightgreen', 'gold','pink', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on brexit'  + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.getData()