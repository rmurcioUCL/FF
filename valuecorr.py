import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np

df = pd.read_csv('/Users/casa/Documents/FF/scorevalue.csv')
for i in range(0,df.shape[0]):
    s1 = df.loc[i,'s1']
    s2 = df.loc[i,'s2']
    sumcount=df.loc[(df['s1'] == s1) & (df['s2'] == s2), 'countq'].sum()
    
'''sum_df = df.groupby(['s1','s2']).agg({'countq': 'sum'})

i=sum_df.loc[sum_df['s1'] == 6, 'countq']
print(str(i))'''
