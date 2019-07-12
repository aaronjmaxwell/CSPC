import configparser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sci
from scipy import stats

from cleaner import cleaner

cf = configparser.ConfigParser()
cf.read('cspc.ini')

dater = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
         10: 'Oct', 11: 'Nov', 12: 'Dec'}


def tweets(dat, kw):
    dat = dat.sort_values('TWT')
    dat = dat[dat.TWT > 0]
    fig, ax = plt.subplots(2, figsize = (8, 5), sharex = True)
    l = ['Likes', 'Retweets']
    yl = [40, 25]
    label = r'm: {:.2f} $\pm$ {:.2f}, $\sigma$: {:.2f}, $R^2$: {:.2f}'
    altlabel = r'm: {:.2f} $\pm$ {:.2f}, $\sigma$: {:.2f}, $b$ {:.2f}, $\mu$: {:.2f} $\pm$ {:.2f}'

    for i, c in enumerate(['F', 'RT']):
        z = []
        x, y = dat.TWT.values, dat[c].values
        for j in range(dat.TWT.max()):
            z.append(dat[dat.TWT == j + 1][c].values)
        m, b, r, __, s = stats.linregress(x, y)
        y_hat = m * x + b
        std = np.sqrt(np.sum((y - y_hat) ** 2) / (len(y) - 2))

        ax[i].plot(x, y, '.', color = 'r', mew = 0)
        ax[i].plot(x, y_hat, label = label.format(m, s, std, r))
        ax[i].boxplot(z)

        ax[i].legend(fontsize = 6)

        ax[i].set_xlim(0, 6)
        ax[i].set_ylim(0, yl[i])
        #ax[i].set_xticks([i for i in range(7)])
        ax[i].set_ylabel(l[i])
        for t in ax[i].get_xticklabels():
            t.set_fontsize(8)
        for t in ax[i].get_yticklabels():
            t.set_fontsize(8)
        ax[i].patch.set_alpha(0.25)
        ax[i].grid()

    ax[1].set_xlabel('Tweets')

    fig.patch.set_alpha(0.25)
    plt.savefig('images/Hashtag_Activity.png', dpi = 300)
    plt.clf()
    plt.close()


def impressions(dat, kw):
    """Plot impression rate."""
    fig, ax = plt.subplots(2, 1, figsize = (8, 5))
    kwarg['color'] = 'black'

    ax[0].bar(dat.Days.values, dat.Rate.values, 1, **kw)
    ax[0].set_ylabel(r'($\heartsuit$' + ' + RT) / TWT', color = 'black')
    ax[0].patch.set_alpha(0.25)
    for t in ax[0].get_xticklabels():
        t.set_fontsize(8)
    for t in ax[0].get_yticklabels():
        t.set_fontsize(8)

    ax[0].set_ylim(0, dat.Rate.max())
    # ax[0].text(227, 4, '#CSPC2017', fontsize = 6, rotation = 90)

    # Impression Rate
    ax[0].grid(color = 'black', alpha = 0.25)
    ylim = ax[0].get_ylim()

    y = sci.stats.gaussian_kde(dat[dat.TWT > 0].Rate.values, bw_method = 0.1)
    x = np.linspace(ylim[0], ylim[1], np.round((ylim[1] - ylim[0]) / 0.05))
    z = y.evaluate(x)

    xt = ax[0].get_xticks()
    xl = [t if isinstance(t, str) else dater[t.month] + ' ' + str(t.day) for t in [
        df.index[int(t)].date() if ((t >= 0) and (t <= (len(df) - 1))) else '' for t in xt]]
    ax[0].set_xticklabels(xl)
    ax[0].set_xticklabels(xl)
    ax[0].set_xlabel('Days', color = 'black')
    ax[0].set_title('#' + cf['CONF']['hashtag'], color = 'black')

    ax[1].fill_between(x, z * 100., 0, edgecolor = 'none', facecolor = 'green')
    ax[1].set_xlim(0, ylim[1])
    ax[1].set_ylim((0, 20))
    ax[1].set_xlabel('Impressions', color = 'k')
    ax[1].set_ylabel('Frequency', color = 'k')
    ax[1].patch.set_alpha(0.25)
    ax[1].set_position((0.125, 0.1, 0.775, 0.35))
    for t in ax[1].get_xticklabels():
        t.set_fontsize(8)
    for t in ax[1].get_yticklabels():
        t.set_fontsize(8)

    fig.patch.set_alpha(0.25)
    plt.savefig('images/Hashtag_Impressions.png', dpi = 300)
    plt.clf()
    plt.close()


def weekly_tweets(dat, kw):
    fig, ax = plt.subplots(3, 1, figsize = (8, 5), sharex = True)
    colors = ['black', 'red', 'blue']
    columns = ['TWT', 'F', 'RT']
    labels = ['TWT', r'$\heartsuit$', 'RT']
    x = np.arange(len(dat))
    m, d = dat.loc[:'2019-11-12'].max(), dat.loc['2018-11-16':].max()
    for i in range(3):
        kw['facecolor'] = colors[i]
        kw['alpha'] = 0.6
        ax[i].bar(x, dat[columns[i]].values, 1, **kw)
        kw['facecolor'] = 'none'
        kw['alpha'] = 1
        ax[i].bar(x, dat[columns[i]].values, 1, **kw)
        ax[i].set_ylabel(labels[i])
        ax[i].patch.set_alpha(0.25)
        ax[i].set_xticks(x)
        ax[i].set_ylim(0, max(m[columns[i]], d[columns[i]]) + 5)
        # ax[i].text(39.25, m[columns[i]] / 2, str(df.loc['2018-11-07'][columns[i]].astype(int)),
        #    fontsize = 6, rotation = 90, color = 'green')
        for t in ax[i].get_xticklabels():
            t.set_fontsize(8)
        for t in ax[i].get_yticklabels():
            t.set_fontsize(8)

    ax[2].xaxis.set_tick_params(pad = -1)
    ax[2].set_xticklabels([str(d.date())[5:] for d in dat.index], fontsize = 6, rotation = 40)

    for i in range(3):
        for major in ax[i].xaxis.get_majorticklines():
            major.set_visible(False)

    ax[0].set_title('#' + cf['CONF']['hashtag'], color = 'black')
    fig.patch.set_alpha(0.25)
    plt.savefig('images/Hashtag_Weekly.png', dpi = 300)
    plt.clf()
    plt.close()


def targets(dat):
    dat = dat.sort_values('TWT')
    fig, ax = plt.subplots(2, 2, figsize = (8, 5), sharex = True)
    c = ['F', 'RT', 'Imp', 'Rate']
    l = ['Likes', 'Retweets', 'Total', 'Rate']
    # yl = [350, 125, 450, 12]
    yl = [100, 50, 100, 12]
    label = r'm: {:.2f} $\pm$ {:.2f}, $\sigma$: {:.2f}, $R^2$: {:.2f}'
    altlabel = r'm: {:.2f} $\pm$ {:.2f}, $\sigma$: {:.2f}, $b$ {:.2f}, $\mu$: {:.2f} $\pm$ {:.2f}'

    for i in range(4):
        j, k = i // 2, i % 2
        x, y = dat.TWT.values, dat[c[i]].values
        m, b, r, __, s = stats.linregress(x, y)
        y_hat = m * x + b
        std = np.sqrt(np.sum((y - y_hat) ** 2) / (len(y) - 2))
        ax[j, k].plot(x, y, 'o', mfc = 'none', ms = 5, mew = 1)
        if (i < 3):
            ax[j, k].plot(x, y_hat, label = label.format(m, s, std, r))
        else:
            ax[j, k].plot(x, y_hat, label = altlabel.format(m, s, std, b, y.mean(), y.std()))

        ax[j, k].legend(fontsize = 6)

        ax[j, k].set_xlim(0, 20)
        ax[j, k].set_ylim(0, yl[i])
        ax[j, k].set_xticks([2 * i for i in range(10)])
        if j == 1:
            ax[j, k].set_xlabel('Tweets')
        ax[j, k].set_ylabel(l[i])
        for t in ax[j, k].get_xticklabels():
            t.set_fontsize(8)
        for t in ax[j, k].get_yticklabels():
            t.set_fontsize(8)
        ax[j, k].patch.set_alpha(0.25)
        ax[j, k].grid()
    fig.patch.set_alpha(0.25)
    plt.savefig('images/Hashtag_Impact.png', dpi = 300)
    plt.clf()
    plt.close()


if __name__ == "__main__":
    kwarg = dict(color = '', edgecolor = 'none')
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
    # df = df.loc['2017-03-20':'2017-10-29'].append(df.loc['2017-11-06':])
    # Tweets
    tweets(df, kwarg)
    # Impression Rate
    impressions(df, kwarg)
    # Grouping into weeks
    df.drop(['Days'], axis = 1, inplace = True)
    df = df.groupby(pd.Grouper(freq = '7D')).sum()
    df['Imp'] = df.F + df.RT
    df['Rate'] = df.Imp / df.TWT
    df.fillna(0.0, inplace = True)
    kwarg = dict(facecolor = '', edgecolor = 'cyan', linewidth = 1, align = 'edge', alpha = 1)
    weekly_tweets(df, kwarg)
    print(df.tail())
    print('Max\n---')
    print('Likes:', df.F.max())
    print('Retweets:', df.RT.max())
    print('Total:', df.Imp.max())
    print('Rate:', df.Rate.max())
    targets(df)
