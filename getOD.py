import urllib, json
import pandas as pd
from itertools import islice


#conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")


#f = open(outfile,"w+")
path='D:/FF/FF-master/FF-master/data/odLondon/'
#path='/Users/casa/2019/FF/'
df = pd.read_csv(path+'msoaLondonCentroids.csv')
url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=51.51482,-0.09213&destinations="
outfile = path+'E02000001_11.json'
#for index, row in df.iterrows():
#    print row['ycoord'],row['xcoord']
#    url = url + row['ycoord'] + ',' + row['xcoord']
dest=''
x=900
y=984
for index, row in islice(df.iterrows(), x,y):
    dest = str(row['ycoord']) + ',' + str(row['xcoord']) + '%7C'+dest
url = url+dest+"&mode=transit&key=AIzaSyBkWClmNEXtBPzaPoYwgzFe89l8TYeUVdc"
print(url)
#print(str(s1)+"-"+str(s2))
#url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+s1+","+s2+"&destinations="+lats2+","+lons2+"&mode=transits&key=AIzaSyAoNoGOHuDlewJkNJ5XUBjOm9nUqEs5ZWQ"
response = urllib.request.urlopen(url)
print('Success')
data =  json.loads(response.read())
#outfile=outfile+str(s1)+"_"+str(s2)+".json"
with open(outfile, 'w') as joutfile:
    json.dump(data, joutfile)

#https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script