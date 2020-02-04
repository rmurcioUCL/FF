import urllib, json
import pandas as pd
from itertools import islice


#conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")


#f = open(outfile,"w+")
df = pd.read_csv('/Users/casa/2019/FF/msoaLondonCentroids.csv')
url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=51.51482,-0.09213&destinations="
outfile = '/Users/casa/2019/FF/odLondon/E02000001_12.json'
#for index, row in df.iterrows():
#    print row['ycoord'],row['xcoord']
#    url = url + row['ycoord'] + ',' + row['xcoord']
dest=''
for index, row in islice(df.iterrows(), 941, None):
    dest = str(row['ycoord']) + ',' + str(row['xcoord']) + '%7C'+dest
    if index==983:
        break
url = url+dest+"&mode=transit&key=AIzaSyAoNoGOHuDlewJkNJ5XUBjOm9nUqEs5ZWQ"
print(url)
#print(str(s1)+"-"+str(s2))
#url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+s1+","+s2+"&destinations="+lats2+","+lons2+"&mode=transits&key=AIzaSyAoNoGOHuDlewJkNJ5XUBjOm9nUqEs5ZWQ"
response = urllib.request.urlopen(url)
data =  json.loads(response.read())
#outfile=outfile+str(s1)+"_"+str(s2)+".json"
with open(outfile, 'w') as joutfile:
    json.dump(data, joutfile)

#https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script