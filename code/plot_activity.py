import configparser
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats

from cleaner import cleaner
dater = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
         10: 'Oct', 11: 'Nov', 12: 'Dec'}

cf = configparser.ConfigParser()
cf.read('cspc.ini')

kwarg = dict(color = '', edgecolor = 'none')


def tweets(cax, x, y, kw, label):
    """Plot the raw data with an optional interpolated line."""
    cax.bar(x, y, np.append(np.diff(x), 1), **kw)

    cax.set_ylabel(label)
    cax.patch.set_alpha(0.0)
    for t in cax.get_xticklabels():
        t.set_fontsize(8)
    for t in cax.get_yticklabels():
        t.set_fontsize(8)


def feed(data, kw, col, key, lab, name):
    fig, ax = plt.subplots(2, 2, figsize = (8, 5), sharex = True)

    for i in range(4):
        kw['color'] = col[i]
        tweets(ax[i // 2, i % 2], data.Days, data[key[i]], kw, lab[i])

    #ax[2].text(227, 220, '#CSPC2017', fontsize = 6, rotation = 90)
    xt = ax[1, 0].get_xticks()
    xl = [t if isinstance(t, str) else dater[t.month] + ' ' + str(t.day) for t in [
        df.index[int(t)].date() if ((t >= 0) and (t <= (len(data) - 1))) else '' for t in xt]]

    for i in range(2):
        ax[1, i].set_xticklabels(xl)
        ax[1, i].set_xlabel('Days', color = 'black')
        ax[0, i].set_title('@sciencepolicy', color = 'black')

        for t in ax[1, i].get_xticklabels():
            t.set_fontsize(8)
        for t in ax[1, i].get_yticklabels():
            t.set_fontsize(8)

    fig.patch.set_alpha(0.25)
    plt.savefig(name, dpi = 300)
    plt.clf()
    plt.close()


def engagements(data, f = None):
    col = ['Likes', 'Retweets', 'Details', 'URL', 'Media', 'Profile', 'Other']
    c = ['red', 'blue', 'green', 'goldenrod', 'cyan', 'magenta', 'black']
    kw = dict(width = 0.8, align = 'edge', lw = 0)

    if f is not None:
        if not isinstance(f, int):
            raise TypeError('f must be an `int`')

        data = data.resample(str(f) + 'D').sum()
        kw['width'] += f - 1
        data.Days = (data.index - data.index.values[0]).days
    else:
        f = 1

    data['Other'] = data[['Replies', 'Follows', 'Hashtag']].sum(axis = 1)

    fig, ax = plt.subplots(2, figsize = (8, 5))
    p, q = np.zeros(len(data)), np.zeros(len(data))

    for i in range(len(col)):
        y = data[col[i]].values
        z = np.zeros(len(y))
        idx = np.where(data.Engagements.values > 0)
        z[idx] = y[idx] / data.Engagements.values[idx]
        ax[0].bar(data.Days.values, y, bottom = p, color = c[i], label = col[i], **kw)
        ax[1].bar(data.Days.values, z, bottom = q, color = c[i], label = col[i], **kw)

        p += y
        q += z

    ax[0].set_xlim(0, f * len(data))
    ax[1].set_xlim(0, f * len(data))
    ax[1].set_ylim(0, 1)
    xt = ax[0].get_xticks()
    xl = [dater[t.month] + ' ' + str(t.day) for t in [df.iloc[int(t // f)].name.date() for t in xt
                                                      if (t <= f * (len(data) - 1))]]

    ax[0].tick_params(axis = 'x', which = 'both', bottom = 'off', labelbottom = 'off')
    ax[1].set_xticklabels(xl)
    ax[1].set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[1].set_yticklabels(['0', '20', '40', '60', '80', ''])
    ax[1].set_xlabel('Days', color = 'black')
    ax[0].set_title('@sciencepolicy', color = 'black')
    ax[0].set_ylabel('Engagements', color = 'black')
    ax[1].set_ylabel('Engagements (%)', color = 'black')

    ax[0].legend(ncol = 2, fontsize = 8)
    for i in range(2):
        for t in ax[i].get_xticklabels():
            t.set_fontsize(8)
        for t in ax[i].get_yticklabels():
            t.set_fontsize(8)
        ax[i].patch.set_alpha(0.25)

    ax[0].set_position((0.1, 0.45, 0.85, 0.5))
    ax[1].set_position((0.1, 0.1, 0.85, 0.345))

    fig.patch.set_alpha(0.25)
    plt.savefig('images/Feed_Engagements.png', dpi = 300)
    plt.clf()
    plt.close()


def impressions(data, kw):
    """Plot impression rate."""
    fig, ax = plt.subplots(2, 1, figsize = (8, 5))
    kw['color'] = 'black'

    tweets(ax[0], data.Days, data.Rate, kw, 'Impression Rate')
    #ax[0].text(227, 4, '#CSPC2017', fontsize = 6, rotation = 90)
    ax[0].grid(color = 'black', alpha = 0.25)
    xlim = ax[0].get_xlim()
    ylim = ax[0].get_ylim()
    y = stats.gaussian_kde(data[data.Tweet > 0].Rate.values, bw_method = 0.1)
    x = np.linspace(ylim[0], ylim[1], np.around((ylim[1] - ylim[0]) / 0.01))
    z = y.evaluate(x)
    z = z / z.max()
    kw = dict(edgecolor = 'none', facecolor = 'green')
    ax[0].set_xlim(xlim)
    ax[0].set_ylim(0, max(ylim))
    xt = ax[0].get_xticks()
    xl = [t if isinstance(t, str) else dater[t.month] + ' ' + str(t.day) for t in [
        df.index[int(t)].date() if ((t >= 0) and (t <= (len(data) - 1))) else '' for t in xt]]
    ax[0].set_xticklabels(xl)
    ax[0].set_title('@sciencepolicy')
    ax[0].set_ylabel('Impression Rate (%)')
    for t in ax[0].get_xticklabels():
        t.set_fontsize(8)
    for t in ax[0].get_yticklabels():
        t.set_fontsize(8)

    ax[1].fill_between(x, z * 100., 0, **kw)
    ax[1].set_xlim(0, ylim[1])
    ax[1].set_ylim((0, 105))
    ax[1].set_xlabel('Impression Rate (%)')
    ax[1].set_ylabel('Peak Frequency (%)')
    ax[1].set_position((0.125, 0.1, 0.775, 0.35))
    for t in ax[1].get_xticklabels():
        t.set_fontsize(8)
    for t in ax[1].get_yticklabels():
        t.set_fontsize(8)

    ax[0].patch.set_alpha(0.25)
    ax[1].patch.set_alpha(0.25)
    fig.patch.set_alpha(0.25)
    plt.savefig('images/Feed_Impressions.png', dpi = 300)
    plt.clf()
    plt.close()


def weekly(data, kw):
    fig, ax = plt.subplots(3, 1, figsize = (8, 5), sharex = True)
    c = ['black', 'red', 'blue']
    col = ['TWT', 'F', 'RT']
    lab = ['TWT', r'$\heartsuit$', 'RT']
    x = sp.arange(len(df))
    for i in range(3):
        kw['facecolor'] = c[i]
        kw['alpha'] = 0.6
        ax[i].bar(x, df[col[i]].values, 1, **kw)
        kw['facecolor'] = 'none'
        kw['alpha'] = 1
        ax[i].bar(x, df[col[i]].values, 1, **kw)
        ax[i].set_ylabel(lab[i])
        ax[i].patch.set_alpha(0.25)
        ax[i].set_xticks(x)
        for t in ax[i].get_xticklabels():
            t.set_fontsize(8)
        for t in ax[i].get_yticklabels():
            t.set_fontsize(8)

    #ax[2].text(32.25, 600, '#CSPC2017', fontsize = 6, rotation = 90)

    ax[2].xaxis.set_tick_params(pad = -1)
    ax[2].set_xticklabels([str(d.date())[5:] for d in data.index], fontsize = 6, rotation = 40)

    for i in range(3):
        for major in ax[i].xaxis.get_majorticklines():
            major.set_visible(False)

    ax[0].set_title('#' + cf['INFO']['hashtag'], color = 'black')
    fig.patch.set_alpha(0.25)
    plt.savefig('images/Feed_Weekly.png', dpi = 300)
    plt.clf()
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv('data/activity.csv')
    df['Time'] = pd.to_datetime(df['Time'])
    df.set_index('Time', inplace = True, drop = True)
    df['Tweet'] = 1
    # Sum all occurrences per day, replacing non-entry days with NaN which we fill with 0.0
    df = df.groupby(pd.Grouper(freq = 'D')).sum()
    df['Rate'] = df['Engagements'] / df['Impressions'] * 100.
    df.fillna(0.0, inplace = True)
    df['Days'] = (df.index - df.index[0]).days
    #df = df.loc['2017-03-20':'2017-10-29'].append(df.loc['2017-11-06':])

    colors = ['slateblue', 'r', 'b', 'g']
    keys = ['Tweet', 'Likes', 'Retweets', 'Details']
    labels = ['Tweets', r'$\heartsuit$', 'Retweets', 'Detail Expands']
    feed(df, kwarg, colors, keys, labels, 'images/Feed_Activity.png')

    colors = ['c', 'm', 'y', 'k']
    keys = ['Profile', 'URL', 'Hashtag', 'Media']
    labels = ['Clicks: ' + k for k in keys]
    feed(df, kwarg, colors, keys, labels, 'images/Feed_Clicks.png')
    impressions(df, kwarg)
    engagements(df, f=4)

    # Grouping into weeks
    #df.drop(['Days'], axis = 1, inplace = True)
    #df = df.groupby(pd.Grouper(freq = '7D')).sum()
    #kwarg = dict(facecolor = '', edgecolor = 'cyan', linewidth = 1, align = 'edge', alpha = 1)
    #weekly(df, kwarg)
