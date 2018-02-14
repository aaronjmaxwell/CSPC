import configparser
import tweepy
import time

cf = configparser.ConfigParser()
cf.read('cspc.ini')
# get authorization
auth = tweepy.OAuthHandler(cf['AUTH']['CONSUMER_KEY'], cf['AUTH']['CONSUMER_SECRET'])
auth.set_access_token(cf['AUTH']['OAUTH_TOKEN'], cf['AUTH']['OAUTH_TOKEN_SECRET'])
# launch api
api = tweepy.API(auth)
ht = 'CSPC2017'
f = 'stream.out'
tweet = tweepy.Cursor(api.search, q = ht, since = cf['DATE']['s'], until = cf['DATE']['u']).items()
out = open(f, "w")
for i,t in enumerate(tweet):
    if ((i + 1) % 1000 == 0):
        for j in range(600):
            if (j % 60 == 0):
                print(j)
            time.sleep(1)
    string = t.created_at
    string = string.strftime('%x,%r')
    string = string + ',' + t.author.screen_name
    string = string + ',' + str(t.favorite_count) + ',' + str(t.retweet_count)
    string = string + '\n'
    out.write(string)
out.close()
