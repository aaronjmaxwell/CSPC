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
tweet = tweepy.Cursor(api.search, q = cf['PANEL']['hashtag'], since = cf['DATE']['since'], until
    = cf['DATE']['until'], tweet_mode = "extended").items()
out = open(cf['PANEL']['file'], "w")
for i, t in enumerate(tweet):
    if ((i + 1) % 1000 == 0):
        for j in range(600):
            if (j % 60 == 0):
                print(j)
            time.sleep(1)

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
out.close()
