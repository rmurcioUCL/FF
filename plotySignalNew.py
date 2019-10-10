import sqlite3
from sqlite3 import Error
import pandas as pd
import seaborn as sns
sns.set(style="darkgrid")
import matplotlib.pyplot as plt
import numpy as np



conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")
#cluster 4w:191; 1w: 78; 1sun: 78; 7w 270; 1sun 270;
sql='select avg(adjusted_local+counts_global)*24 as total from counts where location=106 and \
      (timestamp>=\'2017-05-01\' and timestamp<=\'2017-06-31\') and dweek<6 group by strftime(\'%H\',timestamp) order by strftime(\'%H\',timestamp)'
print (sql)
df = pd.read_sql(sql,conn)
#print(df.H.head(20))
#df.total = df.total.astype(float)
#fmri = sns.load_dataset("fmri")
#sns.lineplot(data=df)     
plt.style.use('seaborn-white')
plt.rcParams['figure.figsize']=(20,7)
plt.rcParams["axes.labelsize"] = 20

plt.grid(False)
styles=['ys-']
ax = sns.lineplot(data=df,legend=False,color="coral", linewidth=2.5,markers=True)
ax.grid( axis='y')
ax.set(xlabel='Hours', ylabel='FF volume') 
for tick in ax.xaxis.get_major_ticks():
      tick.label.set_fontsize(18)
for tick in ax.yaxis.get_major_ticks():
      tick.label.set_fontsize(18)
#locs, labels = plt.xticks()
#plt.xticks(np.arange(250, 3000, step=250))
#plt.xticks(np.arange(150, 2500, step=300), ('Sun', 'Mon 25th', 'Tue', 'Wed', 'Thu','Fri', 'Sat', 'Sun 31st   '))
plt.xticks(np.arange(0, 24, step=1))
#plt.show()
fig = plt.gcf()
fig.savefig('/Users/casa/Documents/FF/img/FFtotten.png', dpi=200)