var properties = {
	title :
		"Trends in Urban flows:  <br>"+
		"an Information Theory approach",
	author: "Roberto Murcio, Karlo Lugumber, Balamurugan Soundararaj",
	sections: [
		"Wi-Fi as a data source",
		"SmartStreetSensor Project",
		"Does it work?",
		"Results" ],
	device_adoption_comment:
		'Almost everyone carries a'+
		'<br>Wifi enabled device' +
		'<br>Almost everyone is broadcasting their presence'+
		'<br>all the time through Wi-Fi probe requests',
	device_adoption_xaxis:"Market penetration (UK 2018)",
	device_adoption_yaxis:"Growth since last year",
	device_adoption_source:"delloite",
	device_adoption_data: { data: [
		{ y: +03, x: 88, z: 88, name: 'Smartphone'},
		{ y: +01, x: 79, z: 79, name: 'Laptop'},
		{ y: -07, x: 44, z: 44, name: 'Desktop'},
		{ y: +01, x: 39, z: 39, name: 'Large<br>tablet'},
		{ y: -11, x: 35, z: 35, name: 'Small<br>tablet'},
		{ y: -09, x: 27, z: 27, name: 'eReader'},
		{ y: -13, x: 18, z: 18, name: 'Gaming<br>device'},
		{ y: +17, x: 18, z: 18, name: 'Fitness<br>band'},
		{ y: -17, x: 15, z: 15, name: 'Mobile<br>phone' },
		{ y: +25, x: 08, z: 08, name: 'Smart<br>watch' },
		{ y: -21, x: 05, z: 05, name: 'VR' } ] } ,
	wifi_method_comment:
		'Almost everyone is broadcasting their presence'+
		'<br>all the time through Wi-Fi probe requests',
	wifi_method_data: {
		first : 'I am Roberto\'s Mobile.<br>Is there any one I can connect to?',
		second : 'I am router from eduram.<br>You can connect to this network!',
		third : 'Cool! Here is my<br>User id and password...',
		fourth : 'Got it. Looks alright!<br>Lets switch to secret mode...',
		fifth : 'gBfzkjFHo4uHlbfON8hU6Lva<br>5HfPe/sG5hR1VPH/KCgOBMx',
		sixth: 'UjuTZZd9V5fQgqR26jeNhlFQ<br>iy24VaN3edu8EzwiWk82EuvJ', },
	research_question: "Can we measure footfall or human activities"+
		"<br>just by capturing these probe requests?",
	sensor_range: [100,150,200,250,300,370,440],
	
	conclusions:[
		"The external noise problem was solved by looking at the singal strength.",
		"MAC randomisation was solved by looking at the sequence numbers",
		"Achieved a stable, accurate footfall count without personal/identifiable data",
		"Examples / Applications"
	],
}
