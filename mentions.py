import pandas as pd

exec(open('handles.py').read())
df = pd.read_csv('./data/promotion.csv')

col_to_drop = list()
for c in df.columns:
    if not df[c].any():
        col_to_drop.append(c)

if (len(col_to_drop) > 0):
    df.drop(col_to_drop, axis = 1, inplace = True)

col = list(df.columns)
for c in ['M', 'D', 'Y', 'h', 'm', 's', 'pm', 'F', 'RT', 'H1']:
    col.remove(c)

df['H1'] = df['H1'].map(lambda x: x.lower())
DF = df['H1'].value_counts().to_frame(name = 'H1')
for c in col:
    df[c] = df[c].map(lambda x: x.lower() if isinstance(x, str) else x)
    DF = DF.join(df[c].value_counts().to_frame(name = c), how = 'outer')

mentions = DF.sum(axis = 1)
mentions.index.name = 'Handle'
mentions.name = 'Mentions'
mentions = mentions.to_frame()
mentions['Mentions'] = mentions['Mentions'].map(int)
mentions['Panel'] = mentions.index.map(lambda x: panel[x.lower()] if (set(panel.keys()).intersection({x.lower()})) else 'None')
mentions['Panel'] = mentions['Panel'].map(lambda x: x[0] + " & " + x[1] if isinstance(x, list) else x)
mentions.sort_values(['Mentions'], ascending = False).to_csv('./data/mentions.csv')
