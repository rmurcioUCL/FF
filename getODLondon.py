import urllib, json
import pandas as pd
from itertools import islice

#path='D:/FF/FF-master/FF-master/data/odLondon/'
path='/Users/casa/2020/bikes/'
df1 = pd.read_csv(path+'CentroidesDistritosCoord_1.csv')
gcoords = df1['lat'].astype(str) + ',' +df1['lon'].astype(str)
#f.write("%s\n" % gcoords)
s='%7C'.join(gcoords)
indexp = [i for i, ltr in enumerate(s) if ltr == '%']
df = pd.read_csv(path+'CentroidesDistritosCoord_1.csv',skiprows=10,names=['name','lat','lon'],index_col='name')
for index,row in df.iterrows():
	print(index)
	outfile = path+index.replace(" ","")+'/tmp'
	x=str(row['lat'])
	y=str(row['lon'])
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='+y+','+x+'&destinations='
	#url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=19.45262317,-99.13524808&destinations='

	dest=''
	init=0
	end=indexp[90]	
	for i in range(0,3):
		if i==0:
			dest=s[init:end]
		elif i==1:
			end=indexp[180]
			dest=s[init:end]
		else:
			end=len(s)-1
			dest=s[init:]									
		init=end+3
		url = url+dest+"&mode=driving&key=AIzaSyDNPwS53wLLo9tIR0BkPrCLP8ZrlcXGl1M"
		#print(url)
		dest=''
		response = urllib.request.urlopen(url)
		url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='+y+','+x+'&destinations='
		#url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=19.45262317,-99.13524808&destinations='

		data =  json.loads(response.read())
		with open(outfile+str(i)+'.json', 'w+') as joutfile:
			json.dump(data, joutfile)
		
		f = open(outfile+'R'+str(i)+'.csv',"w+")
	
		with open(outfile+str(i)+'.json') as json_file:
			data = json.load(json_file)
		for p in data['rows']:
				for r in p['elements']:
					try:
						tokens = r['duration']['text'].split()
						if len(tokens)>2:
							mins = int(tokens[0])*60+int(tokens[2])
						else:
							mins = int(tokens[0])
						result = r['distance']['text']+','+ str(mins)
					except:
						result = 'Error'
					f.write("%s\n" % result)
				f.close()
	#break
print('Success')

