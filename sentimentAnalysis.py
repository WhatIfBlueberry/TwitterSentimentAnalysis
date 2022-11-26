from textblob import TextBlob
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

bearer_token = "AAAAAAAAAAAAAAAAAAAAAJpEjgEAAAAAz59A4vaDIvB%2BpD4%2FAT%2FELPPIOTA%3D5IS7B9X1KUsq9rk9nABmNJ8VrD4BenjpsjuRUUKwucYaoLRJrN"

client = tweepy.Client(bearer_token=bearer_token)


keyword = input("Enter keyword/hashtag to search about: ")
noOfTweet = int(input ("Enter how many tweets to analyze: "))

positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []

def percentage(part,whole):
 return 100 * float(part)/float(whole)

# Replace the limit=1000 with the maximum number of Tweets you want
# Using Paginator because the search endpoint only allows 100 Tweets per request
for tweet in tweepy.Paginator(client.search_recent_tweets, query=keyword,
                              tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=noOfTweet):
 tweet_list.append(tweet.text)
 analysis = TextBlob(tweet.text)
 score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
 neg = score['neg']
 neu = score['neu']
 pos = score['pos']
 comp = score['compound']
 polarity += analysis.sentiment.polarity
 
 if neg > pos:
    negative_list.append(tweet.text)
    negative += 1
 
 elif pos > neg:
    positive_list.append(tweet.text)
    positive += 1
 
 elif pos == neg:
    neutral_list.append(tweet.text)
    neutral += 1
 
positive = percentage(positive, noOfTweet)
negative = percentage(negative, noOfTweet)
neutral = percentage(neutral, noOfTweet)
polarity = percentage(polarity, noOfTweet)
positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')

#Number of Tweets (Total, Positive, Negative, Neutral)tweet_list = pd.DataFrame(tweet_list)
neutral_list = pd.DataFrame(neutral_list)
negative_list = pd.DataFrame(negative_list)
positive_list = pd.DataFrame(positive_list)
print("total number: ",len(tweet_list))
print("positive number: ",len(positive_list))
print("negative number: ", len(negative_list))
print("neutral number: ",len(neutral_list))