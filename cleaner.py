import numpy as np
import pandas as pd
import datetime as dt

def cleaner(file_):
    """Extract-Transform-Load the Tweet data."""
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # grab the data
    df = pd.read_csv(file_)
    # reset to 24 clock
    idx = df[df.pm == 'PM'].index
    df.loc[idx, 'h'] += 12
    # move GMT to EST
    df.h -= 4
    idx = df[df.h < 0].index
    df.loc[idx, 'h'] += 24
    df.loc[idx, 'D'] -= 1
    # fix if twts move to previous month
    for m in range(2,12,1):
        idx = df[(df.D == 0) & (df.M == m)].index
        df.loc[idx, 'D'] = days[m - 1]
        df.loc[idx, 'M'] = int(m - 1)
    # we do not need the hourly data anymore
    df['Date'] = pd.to_datetime(dict(year = df['Y'] + 2000, month = df['M'], day = df['D'], hour
        = df['h'], minute = df['m'], second = df['s']))
    df.set_index('Date', inplace = True)
    df.drop(['Y', 'M', 'D', 'h', 'm', 's', 'pm'], axis = 1, inplace = True)
    return df

if __name__ == "__main__":
    import sys
    df = pd.read_csv(sys.argv[1])
    df.drop(['Tweet id', 'Tweet permalink', 'Tweet text', 'engagement rate', 'permalink clicks',
        'app opens', 'app installs', 'email tweet', 'dial phone', 'media engagements',
        'promoted impressions', 'promoted engagements', 'promoted engagement rate',
        'promoted retweets', 'promoted replies', 'promoted likes', 'promoted user profile clicks',
        'promoted url clicks', 'promoted hashtag clicks', 'promoted detail expands',
        'promoted permalink clicks', 'promoted app opens', 'promoted app installs',
        'promoted follows', 'promoted email tweet', 'promoted dial phone', 'promoted media views',
        'promoted media engagements'], axis = 1, inplace = True)
    df.rename(index = str, columns = {'time': 'Time', 'impressions': 'Impressions', 
        'engagements': 'Engagements', 'retweets': 'Retweets', 'replies': 'Replies',
        'likes': 'Likes', 'user profile clicks': 'Profile', 'url clicks': 'URL',
        'hashtag clicks': 'Hashtag', 'detail expands': 'Details', 'follows': 'Follows',
        'media views': 'Media'}, inplace = True)
    df.Time = pd.to_datetime(df.Time)
    for c in df.columns[1:]:
        df[c] = df[c].map(lambda x: int(x))
    df.to_csv('activity.out', index = False, header = False)
