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

colors = {'black': '#0b100d', 'blue': '#00beef', 'red': '#b00b00', 'pink': '#d15ea5',
          'teal': '#c0ffee', 'gold': '#bada55', 'green': '#00b011'}


def tweets(dat):
    dat = dat.sort_values('TWT')
    dat = dat[dat.TWT > 0]
    fig, ax = plt.subplots(2, figsize = (8, 5), sharex = True)
    l = ['Likes', 'Retweets']
    yl = [50, 25]
    label = r'm: {:.2f} $\pm$ {:.2f}, $\sigma$: {:.2f}, $R^2$: {:.2f}'
    # altlabel = r'm: {:.2f} $\pm$ {:.2f}, $\sigma$: {:.2f}, $b$ {:.2f}, $\mu$: {:.2f} $\pm$ {:.2f}'

    for i, c in enumerate(['F', 'RT']):
        z = []
        x, y = dat.TWT.values, dat[c].values
        for j in range(dat.TWT.max()):
            z.append(dat[dat.TWT == j + 1][c].values)
        m, b, r, __, s = stats.linregress(x, y)
        y_hat = m * x + b
        std = np.sqrt(np.sum((y - y_hat) ** 2) / (len(y) - 2))

        ax[i].boxplot(z, whiskerprops={'color': colors['teal']}, capprops={'color': colors['blue']},
                      boxprops={'color': colors['teal']}, medianprops={'color': colors['pink']})
        ax[i].plot(x, y, '.', color = colors['red'], mew = 0)
        ax[i].plot(x, y_hat, color = colors['green'], label = label.format(m, s, std, r))

        ax[i].legend(fontsize = 6)

        ax[i].set_xlim(0, dat.TWT.max() + 1)
        ax[i].set_ylim(0, yl[i])
        ax[i].set_ylabel(l[i])
        for t in ax[i].get_xticklabels():
            t.set_fontsize(8)
        for t in ax[i].get_yticklabels():
            t.set_fontsize(8)
        ax[i].patch.set_alpha(0.25)
        ax[i].grid(axis = 'y', color = colors['gold'], alpha = 0.25)
        ax[i].set_axisbelow(True)

    ax[0].set_title('#' + cf['CONF']['hashtag'] + ': Impact per Number of Daily Tweets',
                    fontdict = {'fontsize': 10, 'fontweight': 100, 'verticalalignment': 'bottom'},
                    color = colors['black'])
    ax[1].set_xlabel('Tweets', color = colors['black'])

    fig.patch.set_alpha(0.25)
    plt.savefig('images/Hashtag_Activity.png', dpi = 300)
    plt.clf()
    plt.close()


def impressions(dat):
    """Plot impression rate."""
    fig, ax = plt.subplots(2, 1, figsize = (8, 5))
    kw = dict(color = colors['red'], edgecolor = 'none', align = 'edge')

    ax[0].bar(dat.Days.values, dat.Rate.values, 1, **kw)
    ax[0].set_ylabel(r'($\heartsuit$' + ' + RT) / TWT', color = colors['black'])
    ax[0].patch.set_alpha(0.25)
    for t in ax[0].get_xticklabels():
        t.set_fontsize(8)
    for t in ax[0].get_yticklabels():
        t.set_fontsize(8)

    ax[0].set_ylim(0, 25.0)
    # ax[0].text(227, 4, '#CSPC2017', fontsize = 6, rotation = 90)

    # Impression Rate
    ax[0].grid(color = colors['gold'], alpha = 0.25)
    ax[1].grid(color = colors['gold'], alpha = 0.25)

    y = sci.stats.gaussian_kde(dat[dat.TWT > 0].Rate.values, bw_method = 0.1)
    x = np.linspace(0, 25, np.round(25 / 0.05).astype(np.int))
    z = y.evaluate(x)

    xt = ax[0].get_xticks()
    xl = [t if isinstance(t, str) else dater[t.month] + ' ' + str(t.day) for t in [
        df.index[int(t)].date() if ((t >= 0) and (t <= (len(df) - 1))) else '' for t in xt]]
    ax[0].set_xticklabels(xl)
    ax[0].set_xticklabels(xl)
    ax[0].set_xlabel('Days', color = colors['black'])
    ax[0].set_title('#' + cf['CONF']['hashtag'], color = colors['blue'])

    ax[1].fill_between(x, z * 100., 0, edgecolor = 'none', facecolor = colors['green'])
    ax[1].set_xlim(0, 25.0)
    ax[1].set_ylim((0, 20))
    ax[1].set_yticks([4 * i for i in range(6)])
    ax[1].set_xlabel('Impressions', color = colors['black'])
    ax[1].set_ylabel('Frequency', color = colors['black'])
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


def weekly_tweets(dat):
    fig, ax = plt.subplots(3, 1, figsize = (8, 5), sharex = True)
    col = ['blue', 'red', 'green']
    columns = ['TWT', 'F', 'RT']
    labels = ['TWT', r'$\heartsuit$', 'RT']
    x = np.arange(len(dat))
    m, d = dat.loc[:'2019-11-12'].max(), dat.loc['2018-11-16':].max()

    ax[0].set_ylim(0, 40)
    ax[0].set_yticks([i * 5 for i in range(9)])
    ax[1].set_ylim(0, 125)
    ax[1].set_yticks([i * 25 for i in range(6)])
    ax[2].set_ylim(0, 40)
    ax[2].set_yticks([i * 5 for i in range(9)])
    kw = dict(facecolor = '', edgecolor = colors['teal'], linewidth = 1, align = 'edge')

    for i in range(3):
        kw['facecolor'] = colors[col[i]]
        ax[i].bar(x, dat[columns[i]].values, 1, **kw)
        ax[i].set_ylabel(labels[i], color = colors['black'])
        ax[i].patch.set_alpha(0.25)
        ax[i].set_xticks(x)
        ax[i].xaxis.set_major_locator(ticker.FixedLocator(np.arange(len(dat)) + 0.5))
        ax[i].xaxis.set_minor_locator(ticker.FixedLocator(np.arange(len(dat) - 1) + 1))
        # ax[i].text(39.25, m[columns[i]] / 2, str(df.loc['2018-11-07'][columns[i]].astype(int)),
        #    fontsize = 6, rotation = 90, color = 'green')

        ax[i].grid(axis = 'y', color = colors['gold'], alpha = 0.25)
        ax[i].set_axisbelow(True)

        for t in ax[i].get_xticklabels():
            t.set_fontsize(8)
        for t in ax[i].get_yticklabels():
            t.set_fontsize(8)

    ax[2].xaxis.set_tick_params(pad = -1)

    ax[2].set_xticklabels([str(d.date())[5:] for d in dat.index], rotation = 90, fontdict
                          = {'size': 6, 'weight': 700}, color = colors['black'])

    for i in range(3):
        for major in ax[i].xaxis.get_majorticklines():
            major.set_visible(False)

    ax[0].set_title('#' + cf['CONF']['hashtag'], fontdict = {'fontsize': 10, 'fontweight': 300,
                                                             'verticalalignment': 'bottom'},
                    color = colors['black'])
    ax[0].set_position((0.08, 0.68, 0.9, 0.28))
    ax[1].set_position((0.08, 0.38, 0.9, 0.28))
    ax[2].set_position((0.08, 0.08, 0.9, 0.28))
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
    yl = [125, 40, 160, 12]
    label = r'm: {:.2f} $\pm$ {:.2f}'+'\n'+r'$\sigma$: {:.2f}, $R^2$: {:.2f}'
    alt=r'm: {:.2f} $\pm$ {:.2f}, $\sigma$: {:.2f}'+'\n'+r'$b$ {:.2f}, $\mu$: {:.2f} $\pm$ {:.2f}'

    for i in range(4):
        j, k = i // 2, i % 2
        x, y = dat.TWT.values, dat[c[i]].values
        m, b, r, __, s = stats.linregress(x, y)
        y_hat = m * x + b
        std = np.sqrt(np.sum((y - y_hat) ** 2) / (len(y) - 2))
        ax[j, k].plot(x, y, 'o', mfc = 'none', ms = 5, mew = 1, mec = colors['blue'])
        if (i < 3):
            ax[j, k].plot(x, y_hat, label = label.format(m, s, std, r), color = colors['red'])
        else:
            ax[j, k].plot(x, y_hat, label = alt.format(m, s, std, b, y.mean(), y.std()),
                          color = colors['red'])

        ax[j, k].legend(fontsize = 6)

        ax[j, k].set_xlim(0, 35)
        ax[j, k].set_ylim(0, yl[i])
        ax[j, k].set_xticks([5 * i for i in range(8)])
        if j == 1:
            ax[j, k].set_xlabel('Tweets', color = colors['black'])
        ax[j, k].set_ylabel(l[i])
        for t in ax[j, k].get_xticklabels():
            t.set_fontsize(8)
        for t in ax[j, k].get_yticklabels():
            t.set_fontsize(8)
        ax[j, k].patch.set_alpha(0.25)
        ax[j, k].grid(color = colors['gold'])
    ax[0, 0].text(27, 130, 'Weekly #' + cf['CONF']['hashtag'] + ' Usage', fontdict
                  = {'fontsize': 10, 'fontweight': 300, 'verticalalignment': 'bottom'},
                  color = colors['black'])
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
    df = df.loc['2019-01-01':'2019-11-07'].append(df.loc['2019-11-16':])
    # Tweets
    tweets(df)
    # Impression Rate
    impressions(df)
    # Grouping into weeks
    df.drop(['Days'], axis = 1, inplace = True)
    df = df.groupby(pd.Grouper(freq = '7D')).sum()
    df['Imp'] = df.F + df.RT
    df['Rate'] = df.Imp / df.TWT
    df.fillna(0.0, inplace = True)
    weekly_tweets(df)
    targets(df)
    print(df.tail())
    print('Max\n---')
    print('Likes:', df.F.max())
    print('Retweets:', df.RT.max())
    print('Total:', df.Imp.max())
    print('Rate:', df.Rate.max())
