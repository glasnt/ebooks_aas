import random
import re
import sys
import twitter
import markov
from htmlentitydefs import name2codepoint as n2c
from local_settings import *
from secret_env import *

def connect():
    api = twitter.Api(consumer_key=MY_CONSUMER_KEY,
                          consumer_secret=MY_CONSUMER_SECRET,
                          access_token_key=MY_ACCESS_TOKEN_KEY,
                          access_token_secret=MY_ACCESS_TOKEN_SECRET)
    return api

def entity(text):
    if text[:2] == "&#":
        try:
            if text[:3] == "&#x":
                return unichr(int(text[3:-1], 16))
            else:
                return unichr(int(text[2:-1]))
        except ValueError:
            pass
    else:
        guess = text[1:-1]
        numero = n2c[guess]
        try:
            text = unichr(numero)
        except KeyError:
            pass    
    return text

def filter_tweet(tweet):
    tweet.text = re.sub(r'\b(RT|MT) .+','',tweet.text) #take out anything after RT or MT
    tweet.text = re.sub(r'(\#|@|(h\/t)|(http))\S+','',tweet.text) #Take out URLs, hashtags, hts, etc.
    tweet.text = re.sub(r'\n','', tweet.text) #take out new lines.
    tweet.text = re.sub(r'\"|\(|\)', '', tweet.text) #take out quotes.
    htmlsents = re.findall(r'&\w+;', tweet.text)
    if len(htmlsents) > 0 :
        for item in htmlsents:
            tweet.text = re.sub(item, entity(item), tweet.text)    
    tweet.text = re.sub(r'\xe9', 'e', tweet.text) #take out accented e
    return tweet.text
                     
                     
                                                    
def grab_tweets(api, max_id=None):
    source_tweets=[]
    user_tweets = api.GetUserTimeline(screen_name=user, count=PAGE_SIZE, max_id=max_id, include_rts=True, trim_user=True, exclude_replies=True)
  
    # cancel out if we tried to get too many tweets, and the result is empty
    if len(user_tweets) == 0:
      return [], None

    max_id = user_tweets[len(user_tweets)-1].id-1
    for tweet in user_tweets:
        tweet.text = filter_tweet(tweet)
        if len(tweet.text) != 0:
            source_tweets.append(tweet.text)
    return source_tweets, max_id

def get_friends():
    api=connect()
    friends = api.GetFriends()
    return [u.screen_name for u in friends]


if __name__=="__main__":
    if STATIC_TEST==True:
        file = TEST_SOURCE
        print ">>> Generating from {0}".format(file)
        source_tweets = open(file).read().splitlines()
    else:
        source_tweets = []

        # we get a live list of source accounts based on who the TWEET_ACCOUNT follows
        friends = get_friends()
        for handle in friends:
            user=handle
            api=connect()
            max_id=None
           
            # Get PAGE_SIZE * PAGES of tweets per account 
            for x in range(PAGES+1)[1:]:
                source_tweets_iter, max_id = grab_tweets(api,max_id)

                # grab_tweets will return max_id==None if there's no more to get. This is ok.
                if max_id is None:
                  break
                source_tweets += source_tweets_iter
            print "Running total: {0} tweets. Added more from {1}".format(len(source_tweets), handle)

            if len(source_tweets) == 0:
                print "Error fetching tweets from Twitter. Aborting."
                sys.exit()

    mine = markov.MarkovChainer(ORDER)

    for tweet in source_tweets:
        tweet+="."
        mine.add_text(tweet)
        
    for x in range(0,10):
        ebook_tweet = mine.generate_sentence()

    #randomly drop the last word, as Horse_ebooks appears to do.
    if random.randint(0,4) == 0 and re.search(r'(in|to|from|for|with|by|our|of|your|around|under|beyond)\s\w+$', ebook_tweet) != None: 
       print "Losing last word randomly"
       ebook_tweet = re.sub(r'\s\w+.$','',ebook_tweet) 
       print ebook_tweet

    #if a tweet is very short, this will randomly add a second sentence to it.
    if ebook_tweet != None and len(ebook_tweet) < 40:
        rando = random.randint(0,10)
        if rando == 0 or rando == 7: 
            print "Short tweet. Adding another sentence randomly"
            newer_tweet = mine.generate_sentence()
            if newer_tweet != None:
                ebook_tweet += " " + mine.generate_sentence()
            else:
                ebook_tweet = ebook_tweet
        elif rando == 1:
            #say something crazy/prophetic in all caps
            print "ALL THE THINGS"
            ebook_tweet = ebook_tweet.upper()

    
    # hard truncate if it's too long
    if len(ebook_tweet) > 140:
        ebook_tweet = ebook_tweet[:110]

    # Do not tweet if too similar 
    for tweet in source_tweets:
        if ebook_tweet[:-1] not in tweet:
            continue
        else: 
            print "EXACT MATCH. NOT TWEETING: " + ebook_tweet
            sys.exit()
                  
    if DEBUG == False:
        status = api.PostUpdate(ebook_tweet)
        print status.text.encode('utf-8')
    else:
        print "T>>> %s" % ebook_tweet

