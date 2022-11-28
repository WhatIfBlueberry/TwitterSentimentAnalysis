from textblob import TextBlob
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

consumer_key = "61qV0OFGhRtDH0qnHFDsd35Zh"
consumer_secret = "sMmlv7QZAKjNURXjSh3lqyRpbJrs0s4ZS3fw5OaCLrKyoBauoT"
access_key = "1035676027-kBiem3UOVUg093irulINLfSIPBg9DKnkWzES0vz"
access_secret = "sn7yv4tnTGnTQLKPugY2arrnwm8xxIC16k6smLqO7YoA4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
client = tweepy.API(auth)


def printResults(keyword, numberOfTweets, polarity, collectedTweets):
    print("How people are reacting on " + keyword + " by analyzing " + str(numberOfTweets) + " Tweets.")
    print("=====================================================================================================")
    sentimentResult = ""
    if (polarity == 0):
        sentimentResult = "Neutral"
    elif (polarity > 0 and polarity <= 0.3):
        sentimentResult = "Weakly Positive"
    elif (polarity > 0.3 and polarity <= 0.6):
        sentimentResult = "Positive"
    elif (polarity > 0.6 and polarity <= 1):
        sentimentResult = "Strongly Positive"
    elif (polarity > -0.3 and polarity <= 0):
        sentimentResult = "Weakly Negative"
    elif (polarity > -0.6 and polarity <= -0.3):
        sentimentResult = "Negative"
    elif (polarity > -1 and polarity <= -0.6):
        sentimentResult = "Strongly Negative"

    # Number of Tweets with a positive sentiment
    print("Positive tweets percentage: {} %".format(100*len(collectedTweets[collectedTweets['sentiment'] > 0]) / len(collectedTweets['sentiment'])))
    # Number of Tweets with a neutral sentiment
    print("Neutral tweets percentage: {} %".format(100*len(collectedTweets[collectedTweets['sentiment'] == 0]) / len(collectedTweets['sentiment'])))
    # Number of Tweets with a negative sentiment
    print("Negative tweets percentage: {} %".format(100*len(collectedTweets[collectedTweets['sentiment'] < 0]) / len(collectedTweets['sentiment'])))

    # print results
    print("Result: People seem to have a", sentimentResult, "opinion on", keyword)

    print("=====================================================================================================")

    # Top 10 most frequent hashtags
    hashtags = collectedTweets['hashtags'].value_counts()[:10]
    print("Top 10 most frequent hashtags: \n{}. \n".format(hashtags))

    # Top 10 Users with most Tweets
    users = collectedTweets['username'].value_counts()[:10]
    print("Top 10 Users with most Tweets: \n{}. \n".format(users))
    


def scrape(keyword, numberOfTweets):

    # Creating DataFrame using pandas
    collectedTweets = pd.DataFrame(columns=['username',
                                            'description',
                                            'location',
                                            'following',
                                            'followers',
                                            'totaltweets',
                                            'retweetcount',
                                            'text',
                                            'hashtags',
                                            'sentiment'])
    # Collecting tweets using tweepy
    tweets = tweepy.Cursor(client.search_tweets,
                                keyword, lang="en",
                                tweet_mode='extended').items(numberOfTweets)

    # .Cursor() returns an iterable object. Each item in
    # the iterator has various attributes
    # that you can access to
    # get information about each tweet
    list_tweets = [tweet for tweet in tweets]

    # we will iterate over each tweet in the
    # list for extracting information about each tweet
    for tweet in list_tweets:

        analysis = TextBlob(tweet.full_text)
        
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']
        sentiment = analysis.sentiment.polarity

        try:
                text = tweet.retweeted_status.full_text
        except AttributeError:
                text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
                hashtext.append(hashtags[j]['text'])


        ith_tweet = [username, description,
                    location, following,
                    followers, totaltweets,
                    retweetcount, text, hashtext, sentiment]
        collectedTweets.loc[len(collectedTweets)] = ith_tweet
    
    return collectedTweets
 

keyword = input("Enter keyword/hashtag to search about: ")
numberOfTweets = int(input ("Enter how many tweets to analyze: "))

collectedTweets = scrape(keyword, numberOfTweets)

polarity = sum(collectedTweets['sentiment'])/numberOfTweets
printResults(keyword, numberOfTweets, polarity, collectedTweets)

