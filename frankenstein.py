from textblob import TextBlob
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pick import pick
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import webbrowser
import os

consumer_key = "61qV0OFGhRtDH0qnHFDsd35Zh"
consumer_secret = "sMmlv7QZAKjNURXjSh3lqyRpbJrs0s4ZS3fw5OaCLrKyoBauoT"
access_key = "1035676027-kBiem3UOVUg093irulINLfSIPBg9DKnkWzES0vz"
access_secret = "sn7yv4tnTGnTQLKPugY2arrnwm8xxIC16k6smLqO7YoA4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
client = tweepy.API(auth)


def query():
    os.system('clear')
    keyword = input("Enter keyword/hashtag to search about: ")
    numberOfTweets = int(input ("Enter how many tweets to analyze: "))
    sinceDate = input("Enter since date (yyyy-mm-dd): ")

    global collectedTweets
    collectedTweets = pd.DataFrame(columns=['username',
                                            'description',
                                            'location',
                                            'following',
                                            'followers',
                                            'totaltweets',
                                            'retweetcount',
                                            'text',
                                            'hashtags',
                                            'id',
                                            'sentiment'])
    collectedTweets = scrape(keyword, numberOfTweets, sinceDate)
    collectedTweets.to_csv('tweets.csv')

    mainMenu()


def scrape(keyword, numberOfTweets, sinceDate='2022-01-01'):

    # Creating DataFrame using pandas
    collectedTweets.drop(collectedTweets.index, axis=0, inplace=True)
    
    # Collecting tweets using tweepy
    tweets = tweepy.Cursor(client.search_tweets,
                                keyword, lang="en",
                                tweet_mode='extended',
                                since_id=sinceDate).items(numberOfTweets)

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
        id = tweet.id
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
                    retweetcount, text, hashtext, id, sentiment]
        collectedTweets.loc[len(collectedTweets)] = ith_tweet
    
    return collectedTweets

def printSummary():
    polarity = sum(collectedTweets['sentiment'])/numberOfTweets
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

def mainMenu():
    title = 'Please choose which Information you want to see: '
    options =['Top 10 most frequent hashtags', 'Top 10 Users with most Tweets', 'Summary', 'Enter new Query', 'Exit']
    option = pick(options, title)

    if (option[0] == 'Top 10 most frequent hashtags'):
        printTop10Hashtags()
    elif (option[0] == 'Top 10 Users with most Tweets'):
        printTop10Users()
    elif (option[0] == 'Summary'):
        printSummary()
    elif (option[0] == 'Enter new Query'):
        query()
    elif (option[0] == 'Exit'):
        print("Goodbye!")
        exit();

def printTop10Hashtags():
    hashtags = collectedTweets['hashtags'].value_counts()[:10]
    print("Top 10 most frequent hashtags: \n{}. \n".format(hashtags))

def printTop10Users():
    title = 'Select User to Inspect'
    options = []
    topUser = collectedTweets['username'].value_counts()[:10]
    for idx,name in enumerate(topUser.index.tolist()):
        offset = 20 - len(name)
        spaces = ' ' * offset
        string = 'Name: ' + name + spaces + 'Counts: ' + str(topUser[idx])
        options.append(string)
    options.append('Return to Main Menu')
    option = pick(options, title)
    if (option[0] == 'Return to Main Menu'):
        mainMenu()
    selectedUser = topUser.index.tolist()[option[1]]
    userActions(selectedUser)
   
def userActions(selectedUser):
    baseUrl = 'https://twitter.com/'
    user = client.get_user(screen_name = selectedUser)
    title = 'User: ' + selectedUser + '\nPlease choose what you want to do: '
    options =['Show Followers', 'Show User Profile', 'Show User Information', 'Show Tweet(s)', 'Return to User Selection']
    option = pick(options, title)
    if (option[0] == 'Show Followers'):
        followersEnding = '/followers'
        url = baseUrl + selectedUser + followersEnding
        webbrowser.open(url)
    elif (option[0] == 'Show User Profile'):
        webbrowser.open(baseUrl + selectedUser)
    elif (option[0] == 'Show User Information'):
        tweets = collectedTweets.loc[collectedTweets['username'] == selectedUser]
        os.system('clear')
        print(tweets)
        input("Press Enter to return...")
        userActions(selectedUser)
    elif (option[0] == 'Show Tweet(s)'):
        showTweetText(selectedUser)
        tweets = collectedTweets.loc[collectedTweets['username'] == selectedUser]
        print(tweets)
        for i in range(len(tweets)):
            url = baseUrl + selectedUser + '/status/' + str(tweets.loc[i, 'id'])
            webbrowser.open(url)
    elif (option[0] == 'Return to User Selection'):
        printTop10Users()

def showTweetText(selectedUser):
    tweets = collectedTweets.loc[collectedTweets['username'] == selectedUser]['text']
    options = []
    for tweet in tweets:
        parsedTweet = tweet.replace('\n', '\n')
        options.append((parsedTweet, True))
    title = 'Tweet(s). Press enter to return to User Actions'
    pick(options, title)
    userActions(selectedUser)



## Main

query()
