import configparser
import tweepy
import time
T = time.monotonic()

cf = configparser.ConfigParser()
cf.read('cspc.ini')
# get authorization
auth = tweepy.OAuthHandler(cf['AUTH']['CONSUMER_KEY'], cf['AUTH']['CONSUMER_SECRET'])
auth.set_access_token(cf['AUTH']['OAUTH_TOKEN'], cf['AUTH']['OAUTH_TOKEN_SECRET'])
# launch api
api = tweepy.API(auth)
tweet = tweepy.Cursor(api.search, q = cf['CONF']['hashtag'], since = "2018-11-09", until
    = "2018-11-10", tweet_mode = "extended").items()
out = open("conference-11-09.csv", "w")
try:
    for i, t in enumerate(tweet):
        if ((i + 1) % 100 == 0):
            time.sleep(2)
            print('{0:4d}: {1:2.3f}'.format((i + 1), time.monotonic() - T))
        if (t.full_text.find('RT @') < 0):
            txt = t.full_text.encode(encoding = 'ascii', errors='ignore').decode("utf-8")
            s = t.created_at
            s = s.strftime('%x|%r')
            s = s + '|' + t.author.screen_name
            s = s + '|' + str(t.favorite_count) + '|' + str(t.retweet_count)
            s = s + '|' + txt.replace("\n","").replace("\r","").replace("\t","") + "\n"
            out.write(s)
except Exception as error:
    print(__name__, error)
out.close()
