'''
Local Settings for a heroku_ebooks account. #fill in the name of the account you're tweeting from here.
'''

#configuration
# Get these from the environment variables. Set these in heroku. 
import os

MY_CONSUMER_KEY = os.environ["MY_CONSUMER_KEY"]
MY_CONSUMER_SECRET = os.environ["MY_CONSUMER_SECRET"]
MY_ACCESS_TOKEN_KEY = os.environ["MY_ACCESS_TOKEN_KEY"]
MY_ACCESS_TOKEN_SECRET = os.environ["MY_ACCESS_TOKEN_SECRET"]

# SOURCE_ACCOUNTS  no longer used. Instead, sourcing from whoever the TWEET_ACCOUNT follows
ORDER = 2 #how closely do you want this to hew to sensical? 1 is low and 3 is high.
DEBUG = True # False #Set this to False to start Tweeting live
STATIC_TEST = False #Set this to True if you want to test Markov generation from a static file instead of the API.
TEST_SOURCE = "" #The name of a text file of a string-ified list for testing. To avoid unnecessarily hitting Twitter API.
TWEET_ACCOUNT = "" #The name of the account you're tweeting to.


# As not to overload the twitter API, we will limit our API stuffs
PAGE_SIZE=200 #how many tweets to get per page
PAGES=2 # how many pages to get
