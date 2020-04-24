import configparser
import tweepy
import time
T = time.monotonic()

cf = configparser.ConfigParser()
cf.read("cspc.ini")
# get authorization
auth = tweepy.OAuthHandler(cf["AUTH"]["CONSUMER_KEY"], cf["AUTH"]["CONSUMER_SECRET"])
auth.set_access_token(cf["AUTH"]["OAUTH_TOKEN"], cf["AUTH"]["OAUTH_TOKEN_SECRET"])
# launch api
api = tweepy.API(auth)
tweet = tweepy.Cursor(api.search, q=cf["C19Q"]["hashtag"], since=cf["DATE"]["since"],
                      until=cf["DATE"]["until"]).items()
out = open(cf["C19Q"]["file"], "w")
try:
    for i, t in enumerate(tweet):
        if (i + 1) % 200 == 0:
            time.sleep(10)
            print("{0:4d}: {1:2.3f}".format((i + 1), time.monotonic() - T))
        rt = t.text.find("RT")
        if rt < 0:
            x = {**t._json}
            s = x["created_at"] + "," + x["id_str"] + "," + x["user"]["screen_name"] + ","
            s += x["user"]["id_str"] + "," + str(x["favorite_count"]) + ","
            s += str(x["retweet_count"]) + ","
            txt = [y["screen_name"] + "|" for y in x["entities"]["user_mentions"]]
            txt = "".join([y["screen_name"] + "|" for y in x["entities"]["user_mentions"]])[:-1]
            s += txt + "\n"
            out.write(s)
except Exception as error:
    print(__name__, error)
out.close()
