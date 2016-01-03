#The name of the account you're tweeting to.
TWEET_ACCOUNT = ""  # REQUIRED

# Configuration
# import a non-committed secret_env.py instead. 
# because hardcoding environment variables is bad, mmkay?
from secret_env import *



# DEFAULTS

#how closely do you want this to hew to sensical? 1 is low and 3 is high.
ORDER = 2 

# False #Set this to False to start Tweeting live
DEBUG = True 

#Set this to True if you want to test Markov generation from a static file instead of the API.
STATIC_TEST = False 

#The name of a text file of a string-ified list for testing. To avoid unnecessarily hitting Twitter API.
TEST_SOURCE = "" 

# As not to overload the twitter API, we will limit our API stuffs
PAGE_SIZE=200 #how many tweets to get per page
PAGES=2 # how many pages to get
