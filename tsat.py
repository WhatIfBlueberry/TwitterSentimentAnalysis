from textblob import TextBlob
import tweepy
from pick import pick
from tqdm import tqdm
import pandas as pd
import webbrowser
import os
from art import *
from dotenv import load_dotenv

load_dotenv()

# Tweepy authentication
auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'])
client = tweepy.API(auth, wait_on_rate_limit=True)


def query():
    os.system('clear')
    tprint("TSAT")
    global keyword, numberOfTweets, sinceDate
    keyword = input("Enter keyword/hashtag to search about: ")
    numberOfTweets = int(input("Enter how many tweets to analyze: "))
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

# scrapes and analyzes tweets using Tweepy and TextBlob


def scrape(keyword, numberOfTweets, sinceDate='2022-01-01'):

    # Empty DataFrame to store the scraped tweets
    collectedTweets.drop(collectedTweets.index, axis=0, inplace=True)

    # loading bar
    barTweepy = tqdm(total=numberOfTweets, desc='fetching tweets')

    # Collecting tweets using tweepy
    list_tweets = []

    tweets = tweepy.Cursor(client.search_tweets,
                                keyword, lang="en",
                                tweet_mode='extended',
                                since_id=sinceDate).items(numberOfTweets)
    for tweet in tweets:
        list_tweets.append(tweet)
        barTweepy.update(1)

    # we will iterate over each tweet in the
    # list for extracting information about each tweet

    barBlob = tqdm(total=numberOfTweets, desc='analyzing tweets')

    for tweet in list_tweets:
        barBlob.update(1)

        # sentiment analysis with TextBlob
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
    barTweepy.close()
    barBlob.close()
    os.system('clear')
    return collectedTweets


def printSummary():
    os.system('clear')
    polarity = sum(collectedTweets['sentiment'])/numberOfTweets
    positiveTweets = collectedTweets[collectedTweets['sentiment'] > 0]
    negativeTweets = collectedTweets[collectedTweets['sentiment'] < 0]
    neutralTweets = collectedTweets[collectedTweets['sentiment'] == 0]

    print("How people are reacting on " + keyword +
          " by analyzing " + str(numberOfTweets) + " Tweets.")
    print("=====================================================================================================")

    print("Positive Tweets: ", positiveTweets.shape[0])
    print("Negative Tweets: ", negativeTweets.shape[0])
    print("Neutral Tweets: ", neutralTweets.shape[0])
    print("Result: People seem to have a",
          sentimentInHumanLanguage(polarity), "opinion on", keyword)

    print("=====================================================================================================")

    input("Press Enter to continue...")
    os.system('clear')
    mainMenu()


def sentimentInHumanLanguage(polarity):
    if (polarity == 0):
        return "Neutral"
    if (polarity > 0 and polarity <= 0.3):
        return "Weakly Positive"
    if (polarity > 0.3 and polarity <= 0.6):
        return "Positive"
    if (polarity > 0.6 and polarity <= 1):
        return "Strongly Positive"
    if (polarity > -0.3 and polarity <= 0):
        return "Weakly Negative"
    if (polarity > -0.6 and polarity <= -0.3):
        return "Negative"
    if (polarity > -1 and polarity <= -0.6):
        return "Strongly Negative"

def mainMenu():
    title = 'Please choose which Information you want to see: '
    options =['Top 10 most frequent hashtags', 'Top 10 Users with most Tweets', 'Summary', 'Enter new Query', 'Exit']
    option = pick(options, title)

    if (option[0] == 'Top 10 most frequent hashtags'):
        printTop10Hashtags()
    if (option[0] == 'Top 10 Users with most Tweets'):
        printTop10Users()
    if (option[0] == 'Summary'):
        printSummary()
    if (option[0] == 'Enter new Query'):
        query()
    if (option[0] == 'Exit'):
        print("Goodbye!")
        exit();

def printTop10Hashtags():
    hashtags = collectedTweets['hashtags'].value_counts()[:10]
    print("Top 10 most frequent hashtags: \n{}. \n".format(hashtags))
    input("Press Enter to continue...")
    os.system('clear')
    mainMenu()

def printTop10Users(numUsers=10):
    title = 'Select User to Inspect'
    options = []
    topUser = collectedTweets['username'].value_counts()[:numUsers]
    for idx,name in enumerate(topUser.index.tolist()):
        offset = 20 - len(name)
        spaces = ' ' * offset
        string = 'Name: ' + name + spaces + 'Counts: ' + str(topUser[idx])
        options.append(string)
    if (numUsers < len(collectedTweets['username'].value_counts())):
        options.append('Show me more!')
    options.append('Return to Main Menu')
    option = pick(options, title)
    if (option[0] == 'Return to Main Menu'):
        mainMenu()
    if (option[0] == 'Show me more!'):
        printTop10Users(numUsers + 10)
    selectedUser = topUser.index.tolist()[option[1]]
    userActions(selectedUser)
   
def userActions(selectedUser):
    baseUrl = 'https://twitter.com/'
    title = 'User: ' + selectedUser + '\nPlease choose what you want to do: '
    options =['Show Followers (Browser)', 'Show User Profile (Browser)', 'Show User Information', 'Show Tweet(s)', 'Return to User Selection']
    option = pick(options, title)
    if (option[0] == 'Show Followers (Browser)'):
        followersEnding = '/followers'
        url = baseUrl + selectedUser + followersEnding
        webbrowser.open(url)
        os.system('clear')
        userActions(selectedUser)
    if (option[0] == 'Show User Profile (Browser)'):
        webbrowser.open(baseUrl + selectedUser)
        os.system('clear')
        userActions(selectedUser)
    if (option[0] == 'Show User Information'):
        tweets = collectedTweets.loc[collectedTweets['username'] == selectedUser]
        os.system('clear')
        print(tweets)
        input("Press Enter to return...")
        os.system('clear')
        userActions(selectedUser)
    if (option[0] == 'Show Tweet(s)'):
        showTweetText(selectedUser)
    if (option[0] == 'Return to User Selection'):
        printTop10Users()

def showTweetText(selectedUser):
    tweets = collectedTweets.loc[collectedTweets['username'] == selectedUser]
    title = 'Select Tweet to Inspect in Browser'
    options = []
    for text in enumerate(tweets['text']):
        options.append(text)
    options.append('Return to User Selection')
    options = pick(options, title)
    if (options[0] != 'Return to User Selection'):
        tweetId = tweets['id'].iloc[options[1]]
        url = 'https://twitter.com/' + selectedUser + '/status/' + str(tweetId)
        webbrowser.open(url)
        os.system('clear')
    userActions(selectedUser)

## Main - start of the program

query()
