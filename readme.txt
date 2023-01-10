Twitter Sentiment Analysis Tool (tsat)
Data Science Project by Dylan Rau
January 2023

1) Installing required dependencies 
Inside this folder you'll find a 'requirements.txt' file, which contains libraries and their versions used in this Project
You should be able to install all of them at once with the following bash command: 'pip install -r requirements.txt' 
(make sure you navigate to this folder first, or provide full path before 'requirements.txt')

2) If you are installing from GitHub, make sure to create an .env file with the required Tokens, which can be aquired from your Twitter dev account.
Elevated access is required.

3) Using Tsat
Tsat offers a terminal based UI, which is easy to use and should be straight forward. To start execute the 'tsat.py' file the way you prefer.
Example: Open Bash in this folder and type 'python3 tsat.py'

Your Terminal should be cleared and you are shown 3 Prompts after each other:

1) 'Enter keyword/hashtag to search about:'
	- e.g Andor (Disney Star Wars Show)
2) 'Enter how many tweets to analyze:'
	- Small Note: Speed varies, but roughly speaking 1000 tweets take 15-30 seconds
3) 'Enter since date (yyyy-mm-dd):
	- can be left empty, default since date will be set to 01.01.2022

Following these prompts the tweets will be fetched and analyzed, you should see a loading bar for each.
When this is done you automatically enter the main menu, which looks like this: 

Please choose which Information you want to see:

 * Top 10 most frequent hashtags
   Top 10 Users with most Tweets
   Summary
   Enter new Query
   Exit

Navigate using the arrow keys, confirm with enter.

All following menus should be self explanatory and will not be explained in detail, here is a list of what tsat is capable of:
 - List most frequently used hashtags in the fetched dataset
 - Show Users with most Tweets in the Dataset. (10 is default, can be increased by clicking on 'Show me more!') For each User you can:
	- Show User Follower (Browser)
	- Show User Profile (Browser)
	- Show User Information (Name, description, location, hashtags, id, sentiment ..)
	- Show Tweets
 - Summary: count of positive, neutral and negative Tweets.
 - Enter new Query and start over
 - Also: All fetched Tweets are stored in 'tweets.csv' automatically

4) Questions
If you have any question reach out to me at dylan.rau@st.oth-regensburg.de

Have a nice day!



