import configparser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams
import scipy as sci
from scipy import stats

from cleaner import cleaner

cf = configparser.ConfigParser()
cf.read('cspc.ini')

dater = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
         10: 'Oct', 11: 'Nov', 12: 'Dec'}

rcParams['axes.titlepad'] = 0

COLORS = {'black': '#0b100d', 'blue': '#00beef', 'red': '#b00b00', 'pink': '#d15ea5',
          'teal': '#c0ffee', 'gold': '#bada55', 'green': '#00b011'}


def feed(dat, ks, lab, name):
    dat = dat.sort_values('Tweet')
    dat = dat[dat.Tweet > 0]
    fig, ax = plt.subplots(2, figsize = (8, 5), sharex = True)
    yl = [50, 25]
    label = r'm: {:.2f} $\pm$ {:.2f}, $\sigma$: {:.2f}, $R^2$: {:.2f}'
    kw = {'linewidth': 0.5, 'alpha': 0.6, 'markeredgewidth': 0.5}

    for i, c in enumerate(ks):
        z = []
        x, y = dat.Tweet.values, dat[c].values
        for j in range(dat.Tweet.max()):
            z.append(dat[dat.Tweet == j + 1][c].values)
        m, b, r, __, s = stats.linregress(x, y)
        y_hat = m * x + b
        std = np.sqrt(np.sum((y - y_hat) ** 2) / (len(y) - 2))

        ax[i].boxplot(z, whiskerprops = {**{'color': COLORS['teal']}, **kw},
                      capprops = {**{'color': COLORS['blue']}, **kw},
                      boxprops = {**{'color': COLORS['teal']}, **kw},
                      medianprops = {**{'color': COLORS['pink']}, **kw},
                      flierprops = {**{'color': COLORS['red']}, **kw})
        ax[i].plot(x, y, '.', color = COLORS['red'], mew = 0, alpha = 0.45, ms = 3)
        ax[i].plot(x, y_hat, color = COLORS['green'], ls = '--', label = label.format(m, s, std, r))

        ax[i].legend(fontsize = 6)

        ax[i].set_xlim(0, dat.Tweet.max() + 1)
        ax[i].set_ylim(0, yl[i])
        ax[i].set_ylabel(lab[i])
        for t in ax[i].get_xticklabels():
            t.set_fontsize(8)
        for t in ax[i].get_yticklabels():
            t.set_fontsize(8)
        ax[i].patch.set_alpha(0.25)
        ax[i].grid(axis = 'y', color = COLORS['gold'], alpha = 0.25)
        ax[i].set_axisbelow(True)

    ax[0].set_title('@sciencepolicy: Impact per Number of Daily Tweets',
                    fontdict = {'fontsize': 10, 'fontweight': 100, 'verticalalignment': 'bottom'},
                    color = COLORS['black'])
    ax[1].set_xlabel('Tweets', color = COLORS['black'])

    fig.patch.set_alpha(0.25)
    plt.savefig(name, dpi = 300)
    plt.clf()
    plt.close()


def engagements(data, f = None):
    col = ['Likes', 'Retweets', 'Details', 'URL', 'Media', 'Profile', 'Other']
    c = ['red', 'blue', 'green', 'gold', 'teal', 'pink', 'black']
    kw = dict(width = 0.8, align = 'edge', lw = 0)

    if f is not None:
        if not isinstance(f, int):
            raise TypeError('f must be an `int`')

        data = data.resample(str(f) + 'D').sum()
        kw['width'] += f - 1
        data.Days = (data.index - data.index[0]).days
    else:
        f = 1

    data['Other'] = data[['Replies', 'Follows', 'Hashtag']].sum(axis = 1)

    fig, ax = plt.subplots(2, figsize = (8, 5))
    p, q = np.zeros(len(data)), np.zeros(len(data))

    for i, j in zip(col, c):
        y = data[i].values
        z = np.zeros(len(y))
        idx = np.where(data.Engagements.values > 0)
        z[idx] = y[idx] / data.Engagements.values[idx]
        ax[0].bar(data.Days.values, y, bottom = p, color = COLORS[j], label = i, **kw)
        ax[1].bar(data.Days.values, z, bottom = q, color = COLORS[j], label = i, **kw)

        p += y
        q += z

    ax[0].set_xlim(0, f * len(data))
    ax[0].set_ylim(0, 200)
    ax[1].set_xlim(0, f * len(data))
    ax[1].set_ylim(0, 1)
    xt = ax[0].get_xticks()
    xl = [dater[t.month] + ' ' + str(t.day) for t in [df.iloc[int(t // f)].name.date() for t in xt
                                                      if (t <= f * (len(data) - 1))]]

    ax[0].tick_params(axis = 'x', which = 'both', bottom = 'off', labelbottom = 'off')
    ax[1].set_xticklabels(xl, fontdict = {'size': 6, 'weight': 700}, color = COLORS['black'])
    ax[1].set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax[1].set_yticklabels(['0', '20', '40', '60', '80', ''], fontdict = {'size': 6, 'weight': 700},
                          color = COLORS['black'])
    ax[1].set_xlabel('Days', color = COLORS['black'])
    ax[0].set_title('@sciencepolicy',  fontdict = {'fontsize': 10, 'fontweight': 300,
                                                   'verticalalignment': 'bottom'},
                    color = COLORS['black'])
    ax[0].set_ylabel('Engagements', color = COLORS['black'])
    ax[1].set_ylabel('Engagements (%)', color = COLORS['black'])

    ax[0].legend(ncol = 1, fontsize = 8, loc = (1.003, 0.4))
    for i in range(2):
        for t in ax[i].get_xticklabels():
            t.set_fontsize(8)
        for t in ax[i].get_yticklabels():
            t.set_fontsize(8)
        ax[i].patch.set_alpha(0.25)

    ax[0].set_position((0.08, 0.45, 0.8, 0.5))
    ax[1].set_position((0.08, 0.1, 0.8, 0.345))

    fig.patch.set_alpha(0.25)
    plt.savefig('images/Feed_Engagements.png', dpi = 300)
    plt.clf()
    plt.close()


def impressions(data):
    """Plot impression rate."""
    fig, ax = plt.subplots(2, 1, figsize = (8, 5))
    kw = dict(width = 1, align = 'edge', lw = 0, color = COLORS['black'], edgecolor = 'none')
    ax[0].bar(data.Days.values, data.Rate.values, label = 'Impression Rate', **kw)
    # ax[0].text(227, 4, '#CSPC2017', fontsize = 6, rotation = 90)
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
    x = np.arange(len(df))
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

    # ax[2].text(32.25, 600, '#CSPC2017', fontsize = 6, rotation = 90)

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
    df['Time'] = pd.to_datetime(df['Time'], utc = True)
    df.set_index('Time', inplace = True, drop = True)
    df['Tweet'] = 1
    # Sum all occurrences per day, replacing non-entry days with NaN which we fill with 0.0
    df = df.groupby(pd.Grouper(freq = 'D')).sum()
    df['Rate'] = df['Engagements'] / df['Impressions'] * 100.
    df.fillna(0.0, inplace = True)
    df['Days'] = (df.index - df.index[0]).days
    # df = df.loc['2017-03-20':'2017-10-29'].append(df.loc['2017-11-06':])

    keys, labels = ['Likes', 'Retweets'], [r'$\heartsuit$', 'Retweets']
    feed(df, keys, labels, 'images/Feed_Activity.png')
    keys, labels = ['URL', 'Media'], ['URL Clicks', 'Media Views']
    feed(df, keys, labels, 'images/Feed_Clicks.png')
    keys, labels = ['Details', 'Profile'], ['Detail Expands', 'Profile Views']
    feed(df, keys, labels, 'images/Feed_Details.png')
    impressions(df)
    engagements(df, f=4)

    # Grouping into weeks
    # df.drop(['Days'], axis = 1, inplace = True)
    # df = df.groupby(pd.Grouper(freq = '7D')).sum()
    # kwarg = dict(facecolor = '', edgecolor = 'cyan', linewidth = 1, align = 'edge', alpha = 1)
    # weekly(df, kwarg)
