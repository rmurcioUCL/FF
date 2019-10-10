import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy
from scipy.stats import lognorm

#x = np.arange(10)
size = 843
x = scipy.arange(size)
df = pd.read_csv('/Users/casa/Documents/FF/routeScore3.csv')
'''dist_name = 'lognorm'
dist = getattr(scipy.stats, dist_name)  §§
param = dist.fit(df['score'][7:])

pdf_fitted = dist.pdf(x, *param[:-2], loc=param[-2], scale=param[-1]) * size
plt.plot(pdf_fitted, label=dist_name)
plt.xlim(0,47)
plt.legend(loc='upper right')
plt.show()'''
ax = sns.distplot(df['score'],
                  bins=100,
                  kde=True,
                  color='blue',
                  hist_kws={"linewidth": 20,'alpha':1,"color": "gray"})
ax.set(xlabel='Distribution ', ylabel='Frequency')
#df['score'][5:].hist(bins=35,grid=False,xrot=30.0,xlabelsize=20,ylabelsize=20)
fig = plt.gcf()
fig.set_size_inches(25.5, 10.5)
#fig.savefig('/Users/casa/Documents/FF/img/scoreroutePlaw.png', dpi=100)
cmap = sns.cubehelix_palette(rot=-.2, as_cmap=True)
sns.scatterplot(x="score", y="distance",
                palette=cmap,
                sizes=(1, 8), linewidth=0,
                data=df)
fig.savefig('/Users/casa/Documents/FF/img/scoreroute3S.png', dpi=100)

'''for i in range(1,9):
    df.loc[df['SunClust']==i,'freq'].hist(bins=9,grid=False,xrot=30.0,xlabelsize=20,ylabelsize=20)
    #['freq'].hist(bins=9,grid=False,xrot=30.0,xlabelsize=20,ylabelsize=20)
    plt.title('')
    #plt.xlabel("Type street",fontsize=20)
    plt.ylabel("Frequency",fontsize=20)
    plt.rcParams["figure.figsize"] = (600,400)
    plt.xticks(x, ('','primary', 'secondary', 'tertiary', 'cycleway','pedestrian', 'residential', 'service', 'trunk',''))
    fig = plt.gcf()
    fig.set_size_inches(25.5, 10.5)
    fig.savefig('/Users/casa/Documents/FF/img/typeStreetSunday'+str(i)+'.png', dpi=100)
    plt.close(fig)'''