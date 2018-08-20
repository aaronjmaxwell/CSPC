import pandas as pd
df = pd.read_csv('data/hashtag.csv')
df.drop(['M', 'D', 'Y', 'h', 'm', 's', 'pm'], axis = 1, inplace = True)

DF = df[df.O].groupby('handle').sum()
DF.rename(mapper = {'O': 'Tweets', 'RT': 'Retweets', 'F': 'Likes'}, inplace = True, axis = 1)
DF['Tweets'] = DF['Tweets'].map(lambda x: int(x))

X = df[~df.O].groupby('handle').count().drop(['F', 'RT', 'O'], axis = 1).rename(mapper = {'E': 'Retweeted'}, axis = 1)
X = X[X.Retweeted >= 5]

DF = DF.join(X, how = 'outer').fillna(value = 0)

for c in DF.columns:
    DF[c] = DF[c].map(lambda x: int(x))

DF.sort_values(['Retweets', 'Likes', 'Tweets'], ascending = [False, False, True]).to_csv('data/communicators.csv')
