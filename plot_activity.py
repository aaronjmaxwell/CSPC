import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy as sci
from scipy import interpolate
from scipy import stats

from cleaner import cleaner

dater = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
    10: 'Oct', 11: 'Nov', 12: 'Dec'}

kwarg = dict(color = '', linewidths = 0.75, s = 10, facecolor = 'none')
#kwarg = dict(color = '', lw = 0.5, ls = ':', marker = 'o', ms = 2, mew = 0.75, mfc = 'none')

def PlotTweets(cax, x, y, kwarg, label, interpolate=True):
    """Plot the raw data with an optional interpolated line."""
    if interpolate:
        X = np.linspace(0, x.max(), 10 * (x.max() + 1))
        Y = sci.interpolate.interp1d(x, y, kind = 'cubic')
        cax.plot(X, Y(X), alpha = 0.6, color = kwarg['color'], lw = 0.5, ls = ':')
        cax.scatter(x, y, label = label, **kwarg)
    else:
        cax.plot(x, y, **kwarg)

def Engagements(df, kwarg):
    fig, ax = plt.subplots(figsize = (8, 5))
    kwarg['color'] = 'black'
    PlotTweets(ax, df.Days.values, df.Tweet.values, kwarg, 'Tweets', interpolate = True)
    
    kwarg['color'] = 'red'
    PlotTweets(ax, df.Days.values, df.Likes.values, kwarg, r'$\heartsuit$', interpolate = True)
    
    kwarg['color'] = 'blue'
    PlotTweets(ax, df.Days.values, df.Retweets.values, kwarg, 'Retweets', interpolate = True)
    
    kwarg['color'] = 'green'
    PlotTweets(ax, df.Days.values, df.Engagements.values, kwarg, 'Engagements', interpolate = True)
    
    kwarg['color'] = 'goldenrod'
    PlotTweets(ax, df.Days.values, df.Engagements.values, kwarg, 'Details', interpolate = True)
    
    #ax[2].text(227, 220, '#CSPC2017', fontsize = 6, rotation = 90)
    xt = ax.get_xticks()
    xl = [t if isinstance(t, str) else dater[t.month] + ' ' + str(t.day) for t in [
        df.index[int(t)].date() if ((t >= 0) and (t <= (len(df) - 1))) else '' for t in xt]]
    
    ax.set_xticklabels(xl, fontsize = 9)
    ax.set_xlabel('Days', color = 'black')
    ax.set_title('@sciencepolicy', color = 'black')
    ax.set_ylabel('Daily Count', color = 'black')

    for t in ax.get_xticklabels():
        t.set_fontsize(9)
    for t in ax.get_yticklabels():
        t.set_fontsize(9)
    
    ax.legend()
    ax.patch.set_alpha(0)
    fig.patch.set_alpha(0)
    plt.savefig('images/Feed_Activity.png', dpi = 300)
    plt.clf()
    plt.close()

def Clicks(df, kwarg):
    fig, ax = plt.subplots(figsize = (8, 5))
    kwarg['color'] = 'black'
    PlotTweets(ax, df.Days.values, df.Tweet.values, kwarg, 'Tweets', interpolate = True)
    
    kwarg['color'] = 'red'
    PlotTweets(ax, df.Days.values, df.Profile.values, kwarg, 'Profile', interpolate = True)
    
    kwarg['color'] = 'blue'
    PlotTweets(ax, df.Days.values, df.URL.values, kwarg, 'URL', interpolate = True)
    
    kwarg['color'] = 'green'
    PlotTweets(ax, df.Days.values, df.Hashtag.values, kwarg, 'Hashtag', interpolate = True)
    
    kwarg['color'] = 'goldenrod'
    PlotTweets(ax, df.Days.values, df.Hashtag.values, kwarg, 'Follows', interpolate = True)
    
    kwarg['color'] = 'violet'
    PlotTweets(ax, df.Days.values, df.Hashtag.values, kwarg, 'Media', interpolate = True)
    
    #ax[2].text(227, 220, '#CSPC2017', fontsize = 6, rotation = 90)
    xt = ax.get_xticks()
    xl = [t if isinstance(t, str) else dater[t.month] + ' ' + str(t.day) for t in [
        df.index[int(t)].date() if ((t >= 0) and (t <= (len(df) - 1))) else '' for t in xt]]
    
    ax.set_xticklabels(xl, fontsize = 9)
    ax.set_xlabel('Days', color = 'black')
    ax.set_title('@sciencepolicy', color = 'black')
    ax.set_ylabel('Daily Count', color = 'black')

    for t in ax.get_xticklabels():
        t.set_fontsize(9)
    for t in ax.get_yticklabels():
        t.set_fontsize(9)
    
    ax.legend()
    ax.patch.set_alpha(0)
    fig.patch.set_alpha(0)
    plt.savefig('images/Feed_Clicks.png', dpi = 300)
    plt.clf()
    plt.close()

def Impressions(df, kwarg):
    """Plot impression rate."""
    fig, ax = plt.subplots(2, 1, figsize = (8, 5))
    kwarg['color'] = 'black'
    
    PlotTweets(ax[0], df.Days, df.Rate, kwarg, 'Impression Rate', interpolate = True)
    #ax[0].text(227, 4, '#CSPC2017', fontsize = 6, rotation = 90)
    ax[0].grid(color = 'black', alpha = 0.25)
    xlim = ax[0].get_xlim()
    ylim = ax[0].get_ylim()
    Y = sci.stats.gaussian_kde(df.Rate.values, bw_method = 0.1)
    X = np.linspace(ylim[0], ylim[1], np.round((ylim[1] - ylim[0]) / 0.01))
    Z = Y.evaluate(X)
    Z = Z / Z.max()
    kw = dict(edgecolor = 'none', facecolor = 'green')
    ax[0].fill_between(Z + xlim[0], X, 0, alpha = 0.6, **kw)
    ax[0].set_xlim(xlim)
    ax[0].set_ylim(0, np.max(ylim))
    xt = ax[0].get_xticks()
    xl = [t if isinstance(t, str) else dater[t.month] + ' ' + str(t.day) for t in [
        df.index[int(t)].date() if ((t >= 0) and (t <= (len(df) - 1))) else '' for t in xt]]
    ax[0].set_xticklabels(xl)
    ax[0].set_xticklabels(xl)
    ax[0].set_title('@sciencepolicy', color = 'black')
    ax[0].set_ylabel('Impression Rate (%)')

    ax[1].fill_between(X, Z * 100., 0, **kw)
    ax[1].set_xlim(0, ylim[1])
    #ax[1].set_ylim((0, 105))
    ax[1].set_xlabel('Impression Rate (%)', color = 'k')
    ax[1].set_ylabel('Peak Frequency (%)', color = 'k')
    ax[1].set_position((0.125, 0.1, 0.775, 0.35))
    for t in ax[1].get_xticklabels():
        t.set_fontsize(9)
    for t in ax[1].get_yticklabels():
        t.set_fontsize(9)
    
    ax[0].patch.set_alpha(0)
    ax[1].patch.set_alpha(0)
    fig.patch.set_alpha(0)
    plt.savefig('images/Feed_Impressions.png', dpi = 300)
    plt.clf()
    plt.close()

def WeeklyTweets(df, kwarg):
    fig, ax = plt.subplots(3, 1, figsize = (8, 5), sharex = True)
    colors = ['black', 'red', 'blue']
    columns = ['TWT', 'F', 'RT']
    labels = ['TWT', r'$\heartsuit$', 'RT']
    x = np.arange(len(df))
    for i in range(3):
        kwarg['facecolor'] = colors[i]
        kwarg['alpha'] = 0.6
        ax[i].bar(x, df[columns[i]].values, 1, **kwarg)
        kwarg['facecolor'] = 'none'
        kwarg['alpha'] = 1
        ax[i].bar(x, df[columns[i]].values, 1, **kwarg)
        ax[i].set_ylabel(labels[i])
        ax[i].patch.set_alpha(0.0)
        ax[i].set_xticks(x)
        for t in ax[i].get_xticklabels():
            t.set_fontsize(9)
        for t in ax[i].get_yticklabels():
            t.set_fontsize(11)
    
    ax[2].text(32.25, 600, '#CSPC2017', fontsize = 6, rotation = 90)

    ax[2].xaxis.set_tick_params(pad = -1)
    ax[2].set_xticklabels([str(d.date())[5:] for d in df.index], fontsize = 6, rotation = 40)
    
    for i in range(3):
        for major in ax[i].xaxis.get_majorticklines():
            major.set_visible(False)

    ax[0].set_title('#CSPC2017', color = 'black')
    fig.patch.set_alpha(0.0)
    plt.savefig('images/Feed_Weekly.png', dpi = 300)
    plt.clf()
    plt.close()

df = pd.read_csv('activity.csv')
df['Time'] = pd.to_datetime(df['Time'])
df.set_index('Time', inplace = True, drop = True)
df['Tweet'] = 1
# Sum all occurrences per day, replacing non-entry days with NaN which we fill with 0.0
df = df.groupby(pd.Grouper(freq = 'D')).sum()
df['Rate'] = df['Engagements'] / df['Impressions'] * 100.
df.fillna(0.0, inplace = True)
df['Days'] = (df.index - df.index[0]).days
#df = df.loc['2017-03-20':'2017-10-29'].append(df.loc['2017-11-06':])
# Tweets
Engagements(df, kwarg)
Clicks(df, kwarg)
Impressions(df, kwarg)
# Grouping into weeks
#df.drop(['Days'], axis = 1, inplace = True)
#df = df.groupby(pd.Grouper(freq = '7D')).sum()
#kwarg = dict(facecolor = '', edgecolor = 'cyan', linewidth = 1, align = 'edge', alpha = 1)
#WeeklyTweets(df, kwarg)
