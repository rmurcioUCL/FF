import urllib, json
import sqlite3
from sqlite3 import Error
import pandas as pd

conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")


#f = open(outfile,"w+")
df = pd.read_csv('/Users/casa/Documents/FF/locpairs.csv')
for i in range(0,df.shape[0]):
    outfile = '/Users/casa/Documents/FF/routes//'
    s1 = df.loc[i,'s1']
    s2 = df.loc[i,'s2']
    print(str(s1)+"-"+str(s2))
    sql="select distinct(location) as location,lat,lon from locations where location in ("+str(s1)+","+str(s2)+");"
    dfr=pd.read_sql(sql,conn)
    lats1=str(dfr.loc[dfr['location'] == int(s1), 'lat'].tolist()[0])
    lons1=str(dfr.loc[dfr['location'] == int(s1), 'lon'].tolist()[0])
    lats2=str(dfr.loc[dfr['location'] == int(s2), 'lat'].tolist()[0])
    lons2=str(dfr.loc[dfr['location'] == int(s2), 'lon'].tolist()[0])
    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+lats1+","+lons1+"&destination="+lats2+","+lons2+"&mode=walking&key=AIzaSyAoNoGOHuDlewJkNJ5XUBjOm9nUqEs5ZWQ"
    response = urllib.urlopen(url)
    data =  json.loads(response.read())
    outfile=outfile+str(s1)+"_"+str(s2)+".json"
    with open(outfile, 'w') as joutfile:
        json.dump(data, joutfile)

#https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script

