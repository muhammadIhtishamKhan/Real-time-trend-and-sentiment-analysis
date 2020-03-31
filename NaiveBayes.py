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
import numpy as np
import pandas as pd
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split







if __name__== "__main__":
    dataset = pd.read_csv('train_corpus.csv', delimiter=',')
    corpus = []
    #y=dataset.iloc[:, 1].values
    #print(y)

    for index,row in dataset.iterrows():
        review = re.sub('[^a-zA-Z]', ' ', row['TweetText'])
        review = review.lower()
        review = review.split()
        ps = PorterStemmer()
        review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.append(review)

    cv = CountVectorizer(max_features=6500)
    X = cv.fit_transform(corpus).toarray()
    y = dataset.iloc[:, 1].values

    # Splitting the dataset into the Training set and Test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)
    # Fitting Naive Bayes to the Training set
    classifier = GaussianNB()
    classifier.fit(X_train, y_train)
    # Predicting the Test set results
    y_pred = classifier.predict(X_test)

    # Making the Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print (cm)