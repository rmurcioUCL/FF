import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set()

conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")
#sql='select s1,s2,value,quad,max(pquad) as qmax from scoresAgg group by s1,s2 having max(pquad) >=50.0;'
#sql='select cast(value as float) as v1,corr from scores;'
#sql='select timew,avg(corre) as corre from results group by strftime(\'%d\',timestamp),timew;'
sql='select timew,corre from results where dweek<6;'
#sql='select s1,s2,timew,corre as corre from results where (timew>=60 and timew<=300) and (corre>=0.5 and corre<=0.95) and dweek < 6'
 #\ group by s1,s2,timew'
dfp = pd.read_sql(sql,conn)

def main():
   #dfp.hist(column='timew')
   '''sns.jointplot(x="value", y="", data=dfp, size=8, alpha=.25,
             color='k', marker='.')
   plt.tight_layout()
   plt.show()'''

   dfp.plot.scatter(x='timew',y='corre',c='red')
   #dfp['quad'].hist(bins=4,grid=False) 
   plt.grid(True,axis='y',color='black')
   plt.title('')
   plt.xlabel("Time",fontsize=25)
   plt.ylabel("Correlation",fontsize=25)
   plt.rcParams["figure.figsize"] = (600,400)
   ax = plt.gca()
   
   #ax.xaxis.set_major_locator(plt.MaxNLocator(20))
   plt.show()
   ax.set_facecolor('white')
   fig = plt.gcf()

   fig.set_size_inches(25.5, 10.5)
   #fig.savefig('/Users/casa/Documents/FF/img/corrNavg_4.png', dpi=100)

if __name__ == '__main__':
    main()