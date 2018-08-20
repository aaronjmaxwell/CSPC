exec(open('handles.py').read())

import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

df = pd.read_csv('promotion.csv')

df = pd.melt(df, id_vars = ['M', 'D', 'Y', 'h', 'm', 's', 'pm', 'F', 'RT'], value_vars = ['H1',
    'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'], value_name = 'Handle').dropna()

df.drop('variable', axis = 1, inplace = True)

df['Handle'] = df['Handle'].map(lambda x: x.lower())

# Handles
DF = df.drop(['M', 'D', 'Y', 'h', 'm', 's', 'pm'], axis = 1).groupby('Handle').sum()
DF = DF.join(df.drop(['M', 'D', 'Y', 'h', 'm', 's', 'pm'], axis = 1).groupby('Handle').mean(),
    rsuffix = '_avg')
DF = DF.join(df.drop(['M', 'D', 'Y', 'h', 'm', 's', 'pm'], axis = 1).groupby('Handle').count(),
    rsuffix = '_total')

DF.drop('RT_total', axis = 1, inplace = True)
DF.columns = ['Fav', 'RT', 'Mean_Fav', 'Mean_RT', 'Total']
DF.to_csv('Handles.csv')

# Panels
df['Panel'] = df['Handle'].map(lambda x: panel[x] if set(panel.keys()).intersection({x}) else 'N/A')
DF = df[df['Panel'] != 'N/A'].copy()
DF.drop(['h', 'm', 's'], axis = 1, inplace = True)
DF = DF.groupby(['Y', 'M', 'D'], as_index = False).sum()
DF['Date'] = pd.to_datetime(dict(year = DF['Y'] + 2000, month = DF['M'], day = DF['D']))
DF.drop(['Y', 'M', 'D'], axis = 1, inplace = True)
