import numpy as np
import pandas as pd
import datetime as dt

def cleaner(file_):
    """Extract-Transform-Load the Tweet data."""
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year = np.cumsum(days)
    # Grab the file, only use original tweets, and drop the Entity column.
    df = pd.read_csv(file_)
    df = df[df.O == True]
    # reset to 24 clock
    idx = (df.h == 12) & (df.pm == 'AM')
    df.loc[idx, 'h'] = 0
    idx = (df.pm == 'PM')
    df.loc[idx, 'h'] += 12
    # move GMT to EST - Need daylight savings UTC in tuple (month, day, hour)
    spring, fall = (3, 11, 8), (11, 4, 7)
    df['days'] = df.M.map(lambda x: year[(x-1)]) + df.D + df.h / 24.
    idx = ((df.days >= (year[spring[0]-2] + spring[1] + spring[2] / 24))
        & (df.days <= (year[fall[0]-2] + fall[1] + fall[2] / 24.)))
    df.loc[idx, 'h'] -= 4
    df.loc[~idx, 'h'] -= 5
    idx = df[df.h < 0].index
    df.loc[idx, 'h'] += 24
    df.loc[idx, 'D'] -= 1
    # fix if twts move to previous month
    for m in range(1, 12, 1):
        idx = df[(df.D == 0) & (df.M == m)].index
        df.loc[idx, 'D'] = days[m - 2]
        df.loc[idx, 'M'] = int(m - 1)
    # we do not need the hourly data anymore
    df['Date'] = pd.to_datetime(dict(year = df['Y'] + 2000, month = df['M'], day = df['D'], hour
        = df['h'], minute = df['m'], second = df['s']))
    df.set_index('Date', inplace = True)
    df.drop(['E', 'O', 'Y', 'M', 'D', 'h', 'm', 's', 'pm', 'days'], axis = 1, inplace = True)
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
