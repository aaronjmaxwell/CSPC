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
tweet = tweepy.Cursor(api.search, q = cf['PANEL']['hashtag'], since = cf['DATE']['since'], until
    = cf['DATE']['until'], tweet_mode = "extended").items()
out = open(cf['PANEL']['file'], "w")
try:
    for i, t in enumerate(tweet):
        if ((i + 1) % 200 == 0):
            time.sleep(5)
            print('{0:4d}: {1:2.3f}'.format((i + 1), time.monotonic() - T))

        if ((t.author.screen_name == 'sciencepolicy') & (len(t.entities['user_mentions']) > 0) &
        (t.full_text.find('RT @') < 0)):

            string = t.created_at
            string = string.strftime('%x,%r')
            string = string + ',' + str(t.favorite_count) + ',' + str(t.retweet_count)
            handle = {key['id_str']: key['screen_name'] for key in t.entities['user_mentions']}
            for screen_name in handle.values():
                string = string + ',' + screen_name
            string = string + '\n'
            out.write(string)
except Exception as error:
    print(__name__, error)
out.close()
