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
ht = 'CSPC2018'
f = 'stream.out'
tweet = tweepy.Cursor(api.search, q = ht, since = cf['DATE']['s'], until = cf['DATE']['u']).items()
out = open(f, "w")
for i,t in enumerate(tweet):
    if ((i + 1) % 1000 == 0):
        for j in range(600):
            if (j % 60 == 0):
                print(j)
            time.sleep(1)
    rt = t.text.find('RT @')
    string = t.created_at
    string = string.strftime('%x,%r')
    string = string + ',' + t.author.screen_name
    string = string + ',' + str(t.favorite_count) + ',' + str(t.retweet_count)
    if (rt < 0):
        string = string + ',True,\n'
    else:
        txt = t.text[(rt + 4):t.text.find(':')]
        string = string + ',False,' + txt + '\n'
    out.write(string)
out.close()
