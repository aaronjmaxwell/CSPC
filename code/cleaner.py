import sys
import json as js
import datetime as dt
import numpy as np
import pandas as pd


def to_date(row):
    return str(row.month) + "/" + str(row.day) + "/20" + str(row.year)
def to_time(row):
    if row.pm == "AM" or row.hour == 12:
        return "{:02d}:{:02d}:{:02d}".format(row.hour, row.minute, row.second)
    else:
        return "{:02d}:{:02d}:{:02d}".format(row.hour + 12, row.minute, row.second)


def hashtag(file_):
    """Extract-Transform-Load the Tweet data."""
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year = np.cumsum(days)

    df = pd.read_csv(file_, names=["month", "day", "year", "hour", "minute", "second", "pm",
                                   "handle", "likes", "retweets", "O", "E"])

    with open("./data/followers.json", "r") as fp:
        f = js.load(fp)
    for row in df[~df["O"]].itertuples(): 
        if row.handle.lower() in f: 
            if row.E != "sciencepolicy": 
                if "external" in f[row.handle.lower()]: 
                    f[row.handle.lower()]["external"] += 1 
                else: 
                    f[row.handle.lower()]["external"] = 1 
            else: 
                if "cspc" in f[row.handle.lower()]: 
                    f[row.handle.lower()]["cspc"] += 1 
                else: 
                    f[row.handle.lower()]["cspc"] = 1  
        else: 
            if row.E != "sciencepolicy": 
                f[row.handle.lower()] = {"cspc": 1} 
            else: 
                f[row.handle.lower()] = {"external": 1} 
    with open("./data/followers.json", "w") as fp:
        js.dump(f, fp, indent=1)

    df = df[df.O == True].copy()
    df["date"] = df[["month", "day", "year"]].apply(lambda row: to_date(row), axis=1)
    df["time"] = df[["hour", "minute", "second", "pm"]].apply(lambda row: to_time(row), axis=1)
    df["handle"] = df["handle"].map(lambda x: 1)
    df["Date"] = pd.to_datetime(df[["date", "time"]].apply(lambda row: row.date + "T" + row.time,
                                                          axis=1), utc=True)
    df["Date"] = [x.astimezone("america/toronto") for x in df["Date"]]
    df.drop(['date', 'time', 'month', 'day', 'year', 'hour', 'minute', 'second', 'pm', 'O', 'E'],
            axis = 1, inplace = True)
    df.set_index('Date', inplace=True)
    df.rename({"handle": "T", "likes": "F", "retweets": "RT"}, axis=1, inplace=True)
    df = df.resample("1D").sum()
    df.reset_index(inplace=True)
    df["Date"] = pd.to_datetime(["{}-{}-{}".format(x.year, x.month, x.day) for x in df["Date"]])

    DF = pd.read_csv("./data/hashtag.csv")
    DF["Date"] = pd.to_datetime(DF["Date"])
    DF = pd.concat((DF, df), ignore_index=True)
    DF.set_index("Date", inplace=True)
    DF.to_csv("./data/hashtag.csv")


def activity(file_):
    df = pd.read_csv(file_)
    df.drop(["engagement rate", "permalink clicks", "app opens", "app installs", "email tweet",
             "dial phone", "media engagements", "promoted impressions", "promoted engagements",
             "promoted engagement rate", "promoted retweets", "promoted replies", "promoted likes",
             "promoted user profile clicks", "promoted url clicks", "promoted hashtag clicks",
             "promoted detail expands", "promoted permalink clicks", "promoted app opens",
             "promoted app installs", "promoted follows", "promoted email tweet",
             "promoted dial phone", "promoted media views", "promoted media engagements"],
             axis = 1, inplace = True)
    df.rename(index = str, columns = {"Date": "Date", "Tweets published": "Tweets",
                                      "impressions": 'Impressions', "engagements": "Engagements",
                                      "retweets": "Retweets", "replies": "Replies",
                                      "likes": "Likes", "user profile clicks": "Profile",
                                      "url clicks": "URL", "hashtag clicks": "Hashtag",
                                      "detail expands": "Details", "follows": "Follows",
                                      "media views": "Media"}, inplace = True)
    df["Date"] = pd.to_datetime(df["Date"])
    for c in df.columns[1:]:
        df[c] = df[c].map(lambda x: int(x))
    
    DF = pd.read_csv("./data/activity.csv")
    DF["Date"] = pd.to_datetime(DF["Date"])
    DF = pd.concat((DF, df), ignore_index=True)
    DF.set_index("Date", inplace=True)
    DF.to_csv("./data/activity.csv")


if __name__ == "__main__":
    if sys.argv[1] == "hashtag":
        hashtag(sys.argv[2])
    elif sys.argv[1] == "activity":
        activity(sys.argv[2])
    else:
        raise ValueError("{} command not recognized".format(sys.argv[1]))
