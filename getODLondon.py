import urllib, json
import pandas as pd
from itertools import islice


#conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")


#f = open(outfile,"w+")
path='D:/FF/FF-master/FF-master/data/odLondon/'
#path='/Users/casa/2019/FF/'
outfile = path+'tmp'
df = pd.read_csv(path+'msoaLondonCentroids.csv')
url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=51.58827,0.13948&destinations="
gcoords = df['ycoord'].astype(str) + ',' +df['xcoord'].astype(str)
s='%7C'.join(gcoords)
indexp = [i for i, ltr in enumerate(s) if ltr == '%']
dest=''
step=4
inits=2213
for i in range(0,12):
	if i==0:
		dest=s[:inits]
	elif i==1:
		inits=inits+step
		dest=s[inits:indexp[180]]
	elif i==2:
		inits=inits+step
		dest=s[inits:indexp[270]]
	elif i==3:
		inits=inits+step
		dest=s[inits:indexp[360]]
	elif i==4:
		inits=inits+step
		dest=s[inits:indexp[450]]
	elif i==5:
		inits=inits+step
		dest=s[inits:indexp[540]]
	elif i==6:
		inits=inits+step
		dest=s[inits:indexp[630]]
	elif i==7:
		inits=inits+step
		dest=s[inits:indexp[720]]
	elif i==8:
		inits=inits+step
		dest=s[inits:indexp[810]]
	elif i==9:
		inits=inits+step
		dest=s[inits:indexp[900]]
	else:
		inits=inits+step
		dest=s[inits:]												

	url = url+dest+"&mode=transit&key=AIzaSyBkWClmNEXtBPzaPoYwgzFe89l8TYeUVdc"
	response = urllib.request.urlopen(url)
	data =  json.loads(response.read())
	with open(outfile+str(i)+'.json', 'w') as joutfile:
	    json.dump(data, joutfile)
	f = open(outfile,"w+")
	with open('outfile'+str(i)+'.json') as json_file:
        data = json.load(json_file)
        for p in data['rows']:
            for r in p['elements']:
                try:
                    tokens = r['duration']['text'].split()
                    #print(tokens)
                    if len(tokens)>2:
                        mins = int(tokens[0])*60+int(tokens[2])
                    else:
                        mins = int(tokens[0])
                    result = r['distance']['text']+','+ str(mins)
                except:
                    result = 'Error'
                f.write("%s\n" % result)        
    f.close()

print('Success')
#https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script