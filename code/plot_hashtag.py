import configparser
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy as sci
from scipy import interpolate
from scipy import stats

from cleaner import cleaner

cf = configparser.ConfigParser()
cf.read('cspc.ini')

dater = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
    10: 'Oct', 11: 'Nov', 12: 'Dec'}

kwarg = dict(color = '', edgecolor = 'none')

def PlotTweets(cax, x, y, kwarg, label):
    """Plot the raw data with an optional interpolated line."""
    
    cax.bar(x, y, np.append(np.diff(x), 1), **kwarg)
    cax.set_ylabel(label, color = 'black')
    cax.set_ylim(0, y.max())
    cax.patch.set_alpha(0.0)
    for t in cax.get_xticklabels():
        t.set_fontsize(8)
    for t in cax.get_yticklabels():
        t.set_fontsize(8)


def Tweets(df, kwarg):
    fig, ax = plt.subplots(3, 1, figsize = (8, 5), sharex = True)
    kwarg['color'] = 'black'
    PlotTweets(ax[0], df.Days.values, df.TWT.values, kwarg, 'TWT')
# interpolate favourites
    kwarg['color'] = 'red'
    PlotTweets(ax[1], df.Days.values, df.F.values, kwarg, r'$\heartsuit$')
# interpolate retweets
    kwarg['color'] = 'blue'
    PlotTweets(ax[2], df.Days.values, df.RT.values, kwarg, 'RT')
    #ax[2].text(227, 220, '#' + cf['CONF']['hashtag'], fontsize = 6, rotation = 90)
# finish
    xt = ax[2].get_xticks()
    xl = [t if isinstance(t, str) else dater[t.month] + ' ' + str(t.day) for t in [
        df.index[int(t)].date() if ((t >= 0) and (t <= (len(df) - 1))) else '' for t in xt]]
    ax[2].set_xticklabels(xl, fontsize = 8)
    ax[2].set_xlabel('Days', color = 'black')
    ax[0].set_title('#' + cf['CONF']['hashtag'], color = 'black')
    fig.patch.set_alpha(0.0)
    plt.savefig('images/Hashtag_Activity.png', dpi = 300)
    plt.clf()
    plt.close()


def Impressions(df, kwarg):
    """Plot impression rate."""
    fig, ax = plt.subplots(2, 1, figsize = (8, 5))
    kwarg['color'] = 'black'

    PlotTweets(ax[0], df.Days, df.Rate, kwarg, 'Impressions\n(' + r'$\heartsuit$' + ' + RT) / TWT')

    ax[0].set_ylim(0, df.Rate.max())
    #ax[0].text(227, 4, '#CSPC2017', fontsize = 6, rotation = 90)

    # Impression Rate
    ax[0].grid(color = 'black', alpha = 0.25)
    xlim = ax[0].get_xlim()
    ylim = ax[0].get_ylim()

    Y = sci.stats.gaussian_kde(df.Rate.values, bw_method = 0.1)
    X = np.linspace(ylim[0], ylim[1], np.round((ylim[1] - ylim[0]) / 0.05))
    Z = Y.evaluate(X)
    Z = Z / Z.max()

    kw = dict(edgecolor = 'none', facecolor = 'green')

    xt = ax[0].get_xticks()
    xl = [t if isinstance(t, str) else dater[t.month] + ' ' + str(t.day) for t in [
        df.index[int(t)].date() if ((t >= 0) and (t <= (len(df) - 1))) else '' for t in xt]]
    ax[0].set_xticklabels(xl)
    ax[0].set_xticklabels(xl)
    ax[0].set_xlabel('Days', color = 'black')
    ax[0].set_title('#' + cf['CONF']['hashtag'], color = 'black')

    ax[1].fill_between(X, Z * 100., 0, **kw)
    ax[1].set_xlim(0, ylim[1])
    ax[1].set_ylim((0, 105))
    ax[1].set_xlabel('Impressions', color = 'k')
    ax[1].set_ylabel('Peak Frequency (%)', color = 'k')
    ax[1].patch.set_alpha(0.0)
    ax[1].set_position((0.125, 0.1, 0.775, 0.35))
    for t in ax[1].get_xticklabels():
        t.set_fontsize(8)
    for t in ax[1].get_yticklabels():
        t.set_fontsize(8)

    fig.patch.set_alpha(0.0)
    plt.savefig('images/Hashtag_Impressions.png', dpi = 300)
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
            t.set_fontsize(8)
        for t in ax[i].get_yticklabels():
            t.set_fontsize(8)

    #ax[2].text(32.25, 600, '#' + cf['CONF']['hashtag'], fontsize = 6, rotation = 90)

    ax[2].xaxis.set_tick_params(pad = -1)
    ax[2].set_xticklabels([str(d.date())[5:] for d in df.index], fontsize = 6, rotation = 40)

    for i in range(3):
        for major in ax[i].xaxis.get_majorticklines():
            major.set_visible(False)

    ax[0].set_title('#' + cf['CONF']['hashtag'], color = 'black')
    fig.patch.set_alpha(0.0)
    plt.savefig('images/Hashtag_Weekly.png', dpi = 300)
    plt.clf()
    plt.close()


def Targets(df):
    df = df.sort_values('TWT')
    fig, ax = plt.subplots(2, 2, figsize = (8, 5), sharex = True)
    c = ['F', 'RT', 'Imp', 'Rate']
    l = ['Likes', 'Retweets', 'Total', 'Rate']
    yl = [250, 125, 400, 12]
    label = r'm: {:.2f} $\pm$ {:.2f}, $\sigma$: {:.2f}, $R^2$: {:.2f}'
    altlabel = r'm: {:.2f} $\pm$ {:.2f}, $\sigma$: {:.2f}, $b$ {:.2f}, $\mu$: {:.2f} $\pm$ {:.2f}'
    for i in range(4):
        j, k = i // 2, i % 2
        x, y = df.TWT.values, df[c[i]].values
        m, b, r, __, s  = stats.linregress(x, y)
        y_hat = m * x + b
        std = np.sqrt(np.sum((y - y_hat)**2) / (len(y) - 2))
        ax[j, k].plot(x, y, 'o', mfc = 'none', ms = 5, mew = 1)
        if (i < 3):
            ax[j, k].plot(x, y_hat, label = label.format(m, s, std, r))
        else:
            ax[j, k].plot(x, y_hat, label = altlabel.format(m, s, std, b, y.mean(), y.std()))
        
        ax[j, k].legend(fontsize = 6)

        ax[j, k].set_xlim(0, 55)
        ax[j, k].set_ylim(0, yl[i])
        ax[j, k].set_xticks([i * 5 for i in range(12)])
        if (j == 1):
            ax[j, k].set_xlabel('Tweets')
        ax[j, k].set_ylabel(l[i])
        for t in ax[j, k].get_xticklabels():
            t.set_fontsize(8)
        for t in ax[j, k].get_yticklabels():
            t.set_fontsize(8)
        ax[j, k].patch.set_alpha(0)
        ax[j, k].grid()
    fig.patch.set_alpha(0)
    plt.savefig('images/Hashtag_Impact.png', dpi = 300)
    plt.clf()
    plt.close()

if __name__ == "__main__":
    df = cleaner('data/hashtag.csv')
    df['TWT'] = 1
    # Sum all occurrences per day, replacing non-entry days with NaN which we fill with 0.0
    df = df.groupby(pd.Grouper(freq = 'D')).sum()
    df.fillna(0.0, inplace = True)
    # Only way to measure impact, and a proxy of Twitters Impression Rate
    df['Imp'] = df.F + df.RT
    df['Rate'] = df.Imp / df.TWT
    df.fillna(0.0, inplace = True)
    df['Days'] = (df.index - df.index[0]).days
    #df = df.loc['2017-03-20':'2017-10-29'].append(df.loc['2017-11-06':])
    # Tweets
    Tweets(df, kwarg)
    # Impression Rate
    Impressions(df, kwarg)
    # Grouping into weeks
    df.drop(['Days'], axis = 1, inplace = True)
    df = df.groupby(pd.Grouper(freq = '7D')).sum()
    df['Imp'] = df.F + df.RT
    df['Rate'] = df.Imp / df.TWT
    df.fillna(0.0, inplace = True)
    kwarg = dict(facecolor = '', edgecolor = 'cyan', linewidth = 1, align = 'edge', alpha = 1)
    WeeklyTweets(df, kwarg)
    print(df.tail())
    Targets(df)
