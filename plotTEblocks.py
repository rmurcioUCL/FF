import pandas as pd
df = pd.read_csv('/Users/casa/Documents/FF/routeScoreFinal.csv',names=['s1','s2','score','dist'])
print(df.shape)
print(df.head())
dfp = pd.read_csv('/Users/casa/Documents/FF/teF.csv')
print(dfp.shape)
print(dfp.head())
new_df = pd.merge(dfp, df,  how='left', left_on=['s1','s2'], right_on = ['s1','s2'])
print(new_df.shape)
print(new_df.head(20))

df = pd.read_csv('/Users/casa/Documents/FF/teF.csv')
#df.sort_values(by=['timestamp'],ascending=True)
df['uindex']=df['s1'].astype(str)+"_"+df['s2'].astype(str)
#str(df['s1'])#+'-'+str(df['s2'])
print(df.shape)
df['timestamp'] = pd.to_datetime(df['timestamp'],format="%d/%m/%Y")
df['timestamp'] = [time.date() for time in df['timestamp']]
tdf = df[df['uindex']=='125_98']
idx = pd.DatetimeIndex(tdf.timestamp)
series = pd.Series(tdf.direction.values,index=idx)

print(series.head())

uvalues = df['uindex'].unique().tolist()

ff = pd.DataFrame({'uindex':[],'timestamp':[],'direction':[]})
for row in uvalues:
    #print(row)
    tdf = df[df['uindex']==row]
    idx = pd.DatetimeIndex(tdf.timestamp)
    series = pd.Series(tdf.direction.values,index=idx)
    a=series.resample('D').mean()
    a = a.reset_index(name='direction')
    ndf = pd.DataFrame(data=a)
    ndf['uindex']=row
    ff=ff.append(ndf)
    
#tmp=newdf[newdf['uindex']=='106_11']
print(ff.tail())

p = ff.pivot_table(index='uindex',columns='timestamp',values='direction',fill_value=-1)
#p.to_csv('/Users/casa/Documents/FF/pivot.csv')
p.iloc[0:2,0:2]

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plts
plt.rcParams['figure.figsize']=(36,10)
plt.rcParams["axes.labelsize"] = 20
plt.imshow(p.iloc[127:153,0:30],cmap="Greys")
#locations 144:153
#p.iloc[144:153,151:181]
ax=sns.heatmap(p.iloc[144:153,185:215],cmap="YlGn")
#ax=sns.heatmap(p[p.index=='84_2'],cmap="YlGn",xticklabels=range(1,32),yticklabels=range(1,10),cbar=False)
#ax=sns.heatmap(p[p.index=='84_2'].iloc[0,0:30],cmap="YlGn",cbar=False)
ax.set(xlabel='June',ylabel="Locations")
'''for tick in ax.yaxis.get_major_ticks():
      tick.label.set_fontsize(17)
for tick in ax.xaxis.get_major_ticks():
      tick.label.set_fontsize(15)'''

#plt.savefig('/Users/casa/Documents/FF/img/decemberTE.png', dpi=200)

#sns.heatmap(p.iloc[144:153,185:215],cmap="YlGn")

#sns.heatmap(p.iloc[144:153,334:365],cmap="YlGn")'

