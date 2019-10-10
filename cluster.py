from sklearn.cluster import KMeans
import pandas as pd
import numpy as np


outfile = '/Users/casa/Documents/FF/routesCluster3.csv'
#f = open(outfile,"w+")
df = pd.read_csv('/Users/casa/Documents/FF/routeScore3.csv')
#x = np.random.random(1000)
x=df['score'].values
loc1=df['s1'].values
loc2=df['s2'].values
print(x[1:10])
kmeans = KMeans(n_clusters=16)
kmeans.fit(x.reshape(-1,1))  # -1 will be calculated to be 13876 here
y_kmeans = kmeans.predict(x.reshape(-1,1))
print(kmeans.cluster_centers_)
print(y_kmeans[1:10])
#y_kmeans=str(y_kmeans).replace("[","")
#y_kmeans=str(y_kmeans).replace("]","")
i=0
with open(outfile, 'w') as f:
    for item in y_kmeans:
        r=str(loc1[i])+","+str(loc2[i])+","+str(item)
        f.write("%s\n" % r)
        i=i+1
#f.write("%s\n" % str(y_kmeans))
