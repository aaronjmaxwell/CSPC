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
