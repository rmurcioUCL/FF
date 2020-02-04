$(document).ready(function(){

	
	// =========================================================================
	// Setting up keyboard and mouse events for navigation
	// =========================================================================
	$(this).keyup(function(e){
		if(e.keyCode == 8 || e.keyCode == 37) {
			execute_action(action,action-1);
			if(action>0) { action-- }; }
		if(e.keyCode == 13 || e.keyCode == 39) {
			execute_action(action,action+1);
			action++; } });
	$(this).dblclick(function(e){
		execute_action(action,action+1);
		action++; });

	// =========================================================================
	// Create all the container objects
	// =========================================================================
	$('body').append('<div id="background"></div>');
	$('body').prepend(
		'<div id="title" style="display:none">'+properties.title+'<br>'+
		'<div id="author"><br>'+properties.author+'</div>'+
		'<div id="logos"></div>'+
		'</div>');
	$('body').prepend('<div id="sections" style="display:none"></div>');
	for(i in properties.sections) {
		$('#sections').append('<div class="section" style="display:none;">'
			+properties.sections[i]+'</div>'); }
	$('body').prepend('<div id="device_adoption" style="display:none"></div>');
	$('body').prepend('<div id="device_adoption_con" style="display:none">'+
		properties.device_adoption_comment+'</div>');
	$('body').append('<div id="wifi_method">'+
		'<div id="mobile"></div>'+
		'<div id="router"></div>'+
		'<div id="mobile_router_text"></div>'+
		'</div>');
	$('body').prepend('<div id="wifi_method_con" style="display:none">'+
		properties.wifi_method_comment+
		'</div>');
	$('body').prepend('<div id="research_question"'+
		'style="display:none; line-height:1.6;">'+
		properties.research_question+'</div>');
	$('body').prepend('<div id="section" style="display:none;"'+'</div>');
	$('body').prepend('<svg id="section_svg" style="display:none;"'+'</svg>');
	$('body').prepend('<div id="map_stats" style="display:none;">'+
		'<span id="loc_sum">'+properties.map_stats+'</span>'+
		'<span style="font-size:20px;font-weight:100"><br>Locations (~700 active)</span>'+
		'</div>');
	$('body').prepend('<svg id="map_svg" style="display:none;"'+'</svg>');
	$('body').prepend('<svg id="analysis_svg" style="display:none;"'+'</svg>');
	$('body').prepend('<div id="analysis_con" style="display:none;">'+
		properties.analysis_con+'</div>');
	$('body').prepend('<div id="issue_chart" style="display:none"></div>');
	$('body').prepend('<div id="solutions" style="display:none"></div>');
	$('body').prepend('<div id="signal_strength" style="display:none"></div>');
	$('body').prepend('<div id="signal_strength_con" style="display:none">'+
		properties.signal_strenth_con+'</div>');
	$('body').prepend('<div id="sequence_numbers_top" style="display:none"></div>');
	$('body').prepend('<div id="sequence_numbers_bottom" style="display:none"></div>');
	$('body').prepend('<div id="solution_chart" style="display:none"></div>');
	$('body').prepend('<div id="conclusions" style="display:none"></div>');
	$('body').prepend('<div id="ridge_plots" style="display:none"></div>');
	$('body').prepend('<div id="calendar" style="display:none"></div>');

	action = 0;
	
	if(action==0) { particles_js('background'); }

	// =========================================================================
	// Navigation actions ** Needs to be broken down to smaller chunks**
	// =========================================================================
	
	function execute_action(a,b) {
		
		// Show the Title and Information --------------------------------------
		if(a == 0 && b == 1) { $("#title").fadeIn(300); }
		if(a == 1 && b == 0) { $('#title').fadeOut(300); }
		
		// Remove the Title, background and shows outline ----------------------
		if(a == 1 && b == 2) {
			$('#title').fadeOut(300, function() {
				$('#sections, .section').fadeIn(300); }); }
		if(a == 2 && b == 1) {
			$('#sections, .section').fadeOut(300, function(){
				$("#title").fadeIn(300); }); }
	
		// Remove ouline and show device adoption statistics -------------------
		if(a == 2 && b == 3) {
			$('#sections, .section').fadeOut(300);
			$('.particles-js-canvas-el').fadeOut(300, function(){
				$('.particles-js-canvas-el').remove();
				$('#device_adoption').fadeIn(300, function(){
					device_adoption("device_adoption",properties);
					$('#device_adoption').append(
						'<div id="source">source: '+
						properties.device_adoption_source +
						'</div>'); }); }); }
		if(a == 3 && b == 2) {
			$('#device_adoption').fadeOut(300, function(){
				$('#device_adoption').empty();
				particles_js('background');	
				$('#sections, .section').fadeIn(300); }); }
	
		// Comment for device adoption statistics ------------------------------
		if(a == 3 && b == 4) { $('#device_adoption_con').fadeIn(300); }
		if(a == 4 && b == 3) { $('#device_adoption_con').fadeOut(300); }
		
		// Remove the statistics and add Wi-Fi explaination  -------------------
		if(a == 4 && b == 5) {
			$('#device_adoption_con').fadeOut(300);
			$('#device_adoption').fadeOut(300, function(){
				$('#device_adoption').empty();
				$('#wifi_method').fadeIn(300);
			}); }
		if(a == 5 && b == 4) {
			$('#wifi_method').fadeOut(300);
			$('#device_adoption').fadeIn(300, function(){
				device_adoption("device_adoption",properties);
				$('#device_adoption').append(
					'<div id="source">source: '+
					properties.device_adoption_source +
					'</div>');
				$('#device_adoption_con').fadeIn(300); }); }

		// Device sending probe request ----------------------------------------
		if(a == 5 && b == 6) { 
			$('#mobile_router_text')
				.html(properties.wifi_method_data.first)
				.css({"left":"40%","text-align":"left"})
				.fadeIn(300) 
				.css({"background-position": "-100% 0"})
		}
		if(a == 6 && b == 5) { 
			$('#mobile_router_text')
				.fadeOut(300,function(){ $(this).text(''); })
				.css({"background-position": "0 -100%"}); 
		}

		// Device receiving probe response -------------------------------------
		if(a == 6 && b == 7) { 
			$('#mobile_router_text')
				.fadeOut(300, function() { $(this).text(''); })
				.css({"background-position": "0 -100%"})
				.promise()
				.done(function(){
					$(this).html(properties.wifi_method_data.second)
					.css({"left":"55%","text-align":"right"})
					.fadeIn(300)
					.css({"background-position": "+100% 0"}); 
				});
		}
		if(a == 7 && b == 6) {
			$('#mobile_router_text')
				.fadeOut(300,function(){ $(this).text(''); })
				.css({"background-position": "0 -100%"})
				.promise()
				.done(function(){
					$(this).html(properties.wifi_method_data.first)
						.css({"left":"40%","text-align":"left"})
						.fadeIn(300) 
						.css({"background-position": "-100% 0"})
				});
		}
	
		// Device receiving probe response -------------------------------------
		if(a == 7 && b == 8) { 
			$('#mobile_router_text')
				.fadeOut(300, function() { $(this).text(''); })
				.css({"background-position": "0 +100%"})
				.promise()
				.done(function(){
					$(this).html(properties.wifi_method_data.third)
					.css({"left":"40%","text-align":"left"})
					.fadeIn(300)
					.css({"background-position": "-100% 0"}); 
				});
		}
		if(a == 8 && b == 7) {
			$('#mobile_router_text')
				.fadeOut(300,function(){ $(this).text(''); })
				.css({"background-position": "0 -100%"})
				.promise()
				.done(function(){
					$(this).html(properties.wifi_method_data.second)
					.css({"left":"55%","text-align":"right"})
					.fadeIn(300)
					.css({"background-position": "+100% 0"}); 
				});
		}

		// Device receiving probe response -------------------------------------
		if(a == 8 && b == 9) { 
			$('#mobile_router_text')
				.fadeOut(300, function() { $(this).text(''); })
				.css({"background-position": "0 -100%"})
				.promise()
				.done(function(){
					$(this).html(properties.wifi_method_data.fourth)
						.css({"left":"55%","text-align":"right"})
						.fadeIn(300)
						.css({"background-position": "+100% 0"}); 
				});
		}
		if(a == 9 && b == 8) {
			$('#mobile_router_text')
				.fadeOut(300,function(){ $(this).text(''); })
				.css({"background-position": "0 -100%"})
				.promise()
				.done(function(){
					$(this).html(properties.wifi_method_data.third)
					.css({"left":"40%","text-align":"left"})
					.fadeIn(300)
					.css({"background-position": "-100% 0"}); 
				});
		}
	
		// Device receiving probe response -------------------------------------
		if(a == 9 && b == 10) { 
			$('#mobile_router_text')
				.fadeOut(300, function() { $(this).text(''); })
				.css({"background-position": "0 +100%"})
				.promise()
				.done(function(){
					$(this).html(properties.wifi_method_data.fifth)
						.css({"left":"40%","text-align":"left"})
						.fadeIn(300)
						.css({"background-position": "-100% 0"}); 
				});
		}
		if(a == 10 && b == 9) {
			$('#mobile_router_text')
				.fadeOut(300,function(){ $(this).text(''); })
				.css({"background-position": "0 -100%"})
				.promise()
				.done(function(){
					$(this).html(properties.wifi_method_data.fourth)
						.css({"left":"55%","text-align":"right"})
						.fadeIn(300)
						.css({"background-position": "+100% 0"}); 
				});
		}

		// Device receiving probe response -------------------------------------
		if(a == 10 && b == 11) { 
			$('#mobile_router_text')
				.fadeOut(300, function() { $(this).text(''); })
				.css({"background-position": "0 -100%"})
				.promise()
				.done(function(){
					$(this).html(properties.wifi_method_data.sixth)
						.css({"left":"55%","text-align":"right"})
						.fadeIn(300)
						.css({"background-position": "+100% 0"}); 
				});
		}
		if(a == 11 && b == 10) {
			$('#mobile_router_text')
				.fadeOut(300,function(){ $(this).text(''); })
				.css({"background-position": "0 -100%"})
				.promise()
				.done(function(){
					$(this).html(properties.wifi_method_data.fifth)
						.css({"left":"40%","text-align":"left"})
						.fadeIn(300)
						.css({"background-position": "-100% 0"}); 
				});
		}

		// Device receiving probe response -------------------------------------
		if(a == 11 && b == 12) { 
			$('#mobile_router_text')
				.fadeOut(300, function() { $(this).text(''); })
				.css({"background-position": "0 +100%"})
				.promise()
				.done(function(){
					$(this).html(properties.wifi_method_data.first)
						.css({"left":"40%","text-align":"left"})
						.css({"background-image":"linear-gradient(to right, #ffffff00 50%, #ff000022 50%)"})
						.fadeIn(300)
						.css({"background-position": "-100% 0"}); 
				});
		}
		if(a == 12 && b == 11) {
			$('#mobile_router_text')
				.fadeOut(300,function(){ $(this).text(''); })
				.css({"background-position": "0 -100%"})
				.promise()
				.done(function(){
					$(this).css({"background-image":"linear-gradient(to right, #ffffff00 50%, #ffffff22 50%)"})
						.html(properties.wifi_method_data.sixth)
						.css({"left":"55%","text-align":"right"})
						.fadeIn(300)
						.css({"background-position": "+100% 0"}); 
				});
		}

		// Device receiving probe response -------------------------------------
		if(a == 12 && b == 13) {
			$('#router').fadeOut(300);
			setTimeout(function(){
				$('#mobile_router_text')
					.fadeOut(300) 
					.css({"background-position": "0 -100%"})
					.promise()
					.done(function(){
						$(this)
							.fadeIn(300)
							.css({"background-position": "-100% 0"});
					});
			},600);
			blink = setInterval(function(){
				$('#mobile_router_text')
					.fadeOut(300) 
					.css({"background-position": "0 -100%"})
					.promise()
					.done(function(){
						$(this)
							.fadeIn(300)
							.css({"background-position": "-100% 0"}); });
			},2000);
		}
		if(a == 13 && b == 12) {
			$('#router').fadeIn(300);
			if(typeof blink != "undefined") { clearInterval(blink); }
		}

		// Wi-Fi method test ---------------------------------------------------
		if(a == 13 && b == 14) {
			$('#wifi_method_con').fadeIn(300);
			if(typeof blink != "undefined") { clearInterval(blink); }
		}
		if(a == 14 && b == 13) { 
			$('#wifi_method').fadeIn(300);
			$('#mobile_router_text')
				.fadeOut(300, function() { $(this).text(''); })
				.css({"background-position": "0 +100%"})
				.promise()
				.done(function(){
					$(this).html(properties.wifi_method_data.first)
						.css({"left":"40%","text-align":"left"})
						.css({"background-image":"linear-gradient(to right, #ffffff00 50%, #ff000022 50%)"})
						.fadeIn(300)
						.css({"background-position": "-100% 0"}); 
				});
			$('#wifi_method_con').fadeOut(300); }

		// Summary and recap ---------------------------------------------------
		if(a == 14 && b == 15) {
			$('#mobile').fadeOut(300);
			$('#mobile_router_text').fadeOut(300);
			$('#wifi_method_con').fadeOut(300,function(){
				if($('.particles-js-canvas-el').length == 0) {
					particles_js('background'); }
				$('#research_question').fadeIn(300); });
		}
		if(a == 15 && b == 14) {
			$('.particles-js-canvas-el').remove();
			$('#research_question').fadeOut(300,function(){ 
				$('#mobile').fadeIn(300);
				$('#mobile_router_text').fadeIn(300);
				$('#wifi_method_con').fadeIn(300); });
		}

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 15 && b == 16) {
			$('#research_question').fadeOut(300, function() {
				$(this).html('<span style="font-weight:500">Smart Street Sensor</span>'+
					'<span style="font-weight:100"> Project</span>')
					.fadeIn(300); });
		}
		if(a == 16 && b == 15) {
			$('#research_question').fadeOut(300, function() {
				$(this).html(properties.research_question)
					.fadeIn(300); });
		}

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 16 && b == 17) {
			$('.particles-js-canvas-el').remove();
			$('#research_question').fadeOut(300,function(){
				$('#section').fadeIn(300);
				$('#section_svg').fadeIn(500); });
		}
		if(a == 17 && b == 16) {
			$('#section').fadeOut(300,function(){
				if($('.particles-js-canvas-el').length == 0) {
					particles_js('background'); }
				$('#research_question').fadeIn(300);
				$('#section, #section_svg').fadeOut(300); });
		}

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 17 && b == 18) {
			d3.select('#section_svg')
				.selectAll()
				.data(properties.sensor_range)
				.enter()
				.append('circle')
				.attr('class','sensor_range')
				.attr('cx', 252)
				.attr('cy', 510)
				.attr('r',0)
				.style('opacity', 0.03 )
				.style('fill','#88F')
				.transition().duration(500)
				.attr('r',function(d){return(d)}); }
		if(a == 18 && b == 17) {
			d3.selectAll('.sensor_range')
				.transition().duration(500)
				.attr('r',0)
				.remove(); }

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 18 && b == 19) {
			d3.select('#section_svg')
			.selectAll()
			.data([{x:402,y:482},{x:465,y:484},{x:570,y:470}])
			.enter().append('circle')
			.attr('class','footfall_range')
			.attr('cx',function(d){return(d.x)})
			.attr('cy',function(d){return(d.y)})
			.attr('r',0)
			.style('fill','#0F0')
			.transition().duration(300)
			.attr('r',15)
			.style('opacity',0.2);
		}
		if(a == 19 && b == 18) {
			d3.selectAll('.footfall_range')
				.transition().duration(300)
				.attr('r',0)
				.remove();
		}

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 19 && b == 20) {
			d3.select('#section_svg')
			.selectAll()
			.data([{x:702,y:485},{x:790,y:460}])
			.enter().append('circle')
			.attr('class','noise_range')
			.attr('cx',function(d){return(d.x)})
			.attr('cy',function(d){return(d.y)})
			.attr('r',0)
			.style('opacity',0.25).style('fill','#E67E22')
			.transition().duration(300)
			.attr('r',20);
		}
		if(a == 20 && b == 19) {
			d3.selectAll('.noise_range')
				.transition().duration(300)
				.attr('r',0)
				.remove();
		}

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 20 && b == 21) {
			d3.select('#section_svg')
			.selectAll()
			.data([{x:185,y:460},{x:145,y:470},{x:135,y:325},{x:225,y:320}])
			.enter().append('circle')
			.attr('class','dweller_range')
			.attr('cx',function(d){return(d.x)})
			.attr('cy',function(d){return(d.y)})
			.attr('r',0)
			.style('opacity',0.25).style('fill','#E67E22')
			.transition().duration(300)
			.attr('r',15);
		}
		if(a == 21 && b == 20) {
			d3.selectAll('.dweller_range')
				.transition().duration(300)
				.attr('r',0)
				.remove();
		}

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 21 && b == 22) {
			d3.select('#section_svg')
			.selectAll()
			.data([{x:165,y:315,h:22,w:30},{x:112,y:380,h:78,w:132}])
			.enter().append('rect')
			.attr('class','installed_range')
			.attr('x',function(d){return(d.x)})
			.attr('y',function(d){return(d.y)})
			.attr('height',0)
			.attr('width',0)
			.attr('stroke',2)
			.attr('stroke-color','#fff')
			.style('opacity',0.20).style('fill','#E67E22')
			.transition().duration(300)
			.attr('height',function(d){return(d.h)})
			.attr('width',function(d){return(d.w)});
		}
		if(a == 22 && b == 21) {
			d3.selectAll('.installed_range')
				.transition().duration(300)
				.style('opacity',0)
				.remove();
		}

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 22 && b == 23) {
			$('#section, #section_svg').fadeOut(300);
			$('#wifi_method').fadeOut(300,function(){
				$('#map_stats').fadeIn(300,function(){ device_locations(); });
			});
		}
		if(a == 23 && b == 22) {
			$('#map_stats, #map_svg').fadeOut(300,function(){
				$('#map_svg').empty();
				$('#router, #mobile').hide();
				$('#wifi_method, #section, #section_svg').fadeIn(300);
			});
		}

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 23 && b == 24) {
			$('#map_stats').fadeOut(300);
			$('#map_svg').fadeOut(300,function(){
				$('#map_svg').empty();
				$('#analysis_svg').show(function(){
					var width = $(this).width();
					var height = $(this).height();
					var chart = d3.select(this).append('g');
					d3.csv('data/sample_probes.csv',function(pr){
						chart.selectAll('.pr')
							.data(pr)
							.enter()
							.append('circle')
							.attr("cy",function(d){return(height-height*0.33); })
							.attr('cx',width+10)
							.attr('r',10)
							.style("stroke",'#000')
							.style("fill",'#CCC')
							.style("opacity",0.65)
							.on('mouseover',function(){
								d3.select(this)
									.style('fill','#F55')
									.style('stroke','#CCC')})
							.on('mouseout',function(){
								d3.select(this)
									.style('fill','#CCC')
									.style('stroke','#000')})
							.transition().duration(500)
							.attr("cx",function(d){return(5+(d.timestamp/5*(width-10)));})
					});
					chart.append('rect')
						.attr('x',0).attr('y',height-(height*0.33))
						.attr('height',1).attr('width',width)
						.style('stroke','#fff')
					chart.append('text')
						.text("Time")
						.attr('x',width/2).attr('y',height-(height*0.33)+50)
						.style('transform','translate(-50% -50%)')
						.style('font-size','12')
						.style('fill','#fff')
						.attr('text-anchor','middle')
				});
			});
		}
		if(a == 24 && b == 23) {
			var chart = d3.select("#analysis_svg > g")
			var width = $('#analysis_svg').width()
			chart.selectAll('circle')
				.transition().duration(1000)
				.attr('cx',width+10)
				.call(endall,function(){
					$('#analysis_svg').empty();
					$('#map_svg').show();
					$('#map_stats').fadeIn(300,function(){ device_locations(); });
				});
		}

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 24 && b == 25) {
			var chart = d3.select("#analysis_svg > g");
			var cols = d3.scale.ordinal().domain([1,2,3,4,5,6,7,8,9,10,'r']).range(['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#aaaaaa']);
			chart.selectAll('circle')
				.on('mouseout',function(){
						d3.select(this)
							.style('fill',function(d){return(cols(d.mac))})
							.style('stroke','#000')})
				.transition().duration(1000)
				.style("opacity",0.85)
				.style('fill',function(d){return(cols(d.mac))})
		}

		if(a == 25 && b == 24) {
			var chart = d3.select("#analysis_svg > g");
			chart.selectAll('circle')
				.on('mouseout',function(){
					d3.select(this)
						.style('fill','#CCC')
						.style('stroke','#000')})
				.transition().duration(1000)
				.style("opacity",0.65)
				.style('fill','#CCC')
		}

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 25 && b == 26) {
			var chart = d3.select("#analysis_svg > g");
			var width = $('#analysis_svg').width()
			var height= $('#analysis_svg').height()
			chart.selectAll('circle')
				.transition().duration(1000)
				.attr("cx",function(d){return((d.interval/5-0.1)*width)})
				.attr("cy",function(d){return(height-(d.pos1/15*height)-25)})
			chart.selectAll('rect').transition().duration(1000)
				.attr('y',height-50)
				.attr('x',width*0.075)
				.attr('width',width*0.85)
			chart.selectAll('text').transition().duration(1000)
				.text("5 min interval")
				.attr('y',height-15)
		}
		if(a == 26 && b == 25) {
			var chart = d3.select("#analysis_svg > g");
			var width = $('#analysis_svg').width()
			var height= $('#analysis_svg').height()
			chart.selectAll('circle')
				.transition().duration(1000)
				.attr("cy",function(d){return(height-height*0.33); })
				.attr("cx",function(d){return(5+(d.timestamp/5*(width-10)));})
			chart.selectAll('rect').transition().duration(1000)
				.attr('y',height-height*0.33)
				.attr('x',0)
				.attr('width',width)
			chart.selectAll('text').transition().duration(1000)
				.text("Timestamp")
				.attr('y',height-height*0.33+50)
		}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 26 && b == 27) {
			var chart = d3.select("#analysis_svg > g");
			chart.selectAll('circle')
				.transition().duration(1000)
				.style("stroke-width",function(d){return(d.rep1 == 1 ? 1 : 5)})
				.style("opacity",function(d){return(d.rep1 == 1 ? 1 : 0.10)})
		}
		if(a == 27 && b == 26) {
			var chart = d3.select("#analysis_svg > g");
			chart.selectAll('circle')
				.transition().duration(1000)
				.style("stroke-width",1)
				.style("opacity",0.85)
		}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 27 && b == 28) {
			var chart = d3.select("#analysis_svg > g");
			var width = $('#analysis_svg').width()
			var height= $('#analysis_svg').height()
			chart.selectAll('circle')
				.transition().duration(1000)
				.attr("cy",function(d){return(height-(d.pos2/15*height)-25)})
		}
		if(a == 28 && b == 27) {
			var chart = d3.select("#analysis_svg > g");
			var width = $('#analysis_svg').width()
			var height= $('#analysis_svg').height()
			chart.selectAll('circle')
				.transition().duration(1000)
				.attr("cy",function(d){return(height-(d.pos1/15*height)-25)})
		}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 28 && b == 29) {
			var chart = d3.select("#analysis_svg > g");
			var width = $('#analysis_svg').width()
			var height= $('#analysis_svg').height()
			chart.selectAll('circle')
				.transition().duration(1000)
				.style("stroke-width",function(d){return(d.rep2 == 1 ? 1 : 5)})
				.style("opacity",function(d){return(d.rep2 == 1 ? 1 : 0.10)})
		}
		if(a == 29 && b == 28) {
			var chart = d3.select("#analysis_svg > g");
			chart.selectAll('circle')
				.transition().duration(1000)
				.style("stroke-width",function(d){return(d.rep1 == 1 ? 1 : 5)})
				.style("opacity",function(d){return(d.rep1 == 1 ? 1 : 0.10)})	
		}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 29 && b == 30) {
			var chart = d3.select("#analysis_svg > g");
			var width = $('#analysis_svg').width()
			var height= $('#analysis_svg').height()
			chart.selectAll('circle')
				.transition().duration(1000)
				.attr("cy",function(d){return(height-(d.pos3/15*height)-25)})
		}
		if(a == 30 && b == 29) {
			var chart = d3.select("#analysis_svg > g");
			var width = $('#analysis_svg').width()
			var height= $('#analysis_svg').height()
			chart.selectAll('circle')
				.transition().duration(1000)
				.attr("cy",function(d){return(height-(d.pos2/15*height)-25)})
		}

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 30 && b == 31) {
			$("#analysis_svg").fadeOut(300,function(){
				particles_js('background');
				$("#analysis_con").fadeIn(300);
			});
		}
		if(a == 31 && b == 30) {
			$('#analysis_con').fadeOut(300);
			$('.particles-js-canvas-el').fadeOut(300, function(){
				$('.particles-js-canvas-el').remove();
				$("#analysis_svg").fadeIn(300);
			});
		}

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 31 && b == 32) {
			$('#analysis_con').fadeOut(300,function(){
				$(this).html(properties.analysis_issue)
					.fadeIn(300); });
		}
		if(a == 32 && b == 31) {
			$('#analysis_con').fadeOut(300,function(){
				$(this).html(properties.analysis_con)
					.fadeIn(300);
			});
		}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 32 && b == 33) {
			$('#analysis_con').fadeOut(300,function(){
				$('.particles-js-canvas-el').remove();
				$('#issue_chart').show();
				$.getJSON("data/issue.json",function(data){ issue_chart('issue_chart',data); });
			});
		}
		if(a == 33 && b == 32) {
			$('#issue_chart').fadeOut(300,function(){
				$(this).empty();
				particles_js('background');
				$('#analysis_con').fadeIn(300);
			});
		}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 33 && b == 34) {
			$('#issue_chart').fadeOut(300,function(){
				$(this).empty();
				var chart = d3.select("#analysis_svg > g");
				var width = $('#analysis_svg').width()
				var height= $('#analysis_svg').height()
				var cols = d3.scale.ordinal().domain([1,2,3,4,5,6,7,8,9,10,'r']).range(['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#aaaaaa']);
				$('#analysis_svg').fadeIn(300);
				chart.selectAll('circle')
					.on('mouseout',function(){
							d3.select(this)
								.style('fill',function(d){return(cols(d.mac))})
								.style('stroke','#000')})
					.style("opacity",0.85)
					.style('fill',function(d){return(cols(d.mac))})
					.style("stroke",'#000')
					.style("stroke-width",1)
					.attr("cy",function(d){return(height-(d.pos1/15*height)-25)})
			});
		}
		if(a == 26 && b == 25) {
			
		
		}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 34 && b == 35) {
			var chart = d3.select("#analysis_svg > g");
			var height= $('#analysis_svg').height()
			var cols = d3.scale.ordinal().domain([1,2,3,4,5,6,7,8,9,10,99]).range(['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#000000']);
			chart.selectAll('circle')
				.style('opacity',1)
				.on('mouseout',function(){
						d3.select(this)
							.style('fill',function(d){return(cols(d.mac2))})
							.style('stroke-width',function(d){return(d.mac2==99?2:1)})
							.style('stroke','#fff')})
				.transition().duration(1000)
				.style('fill',function(d){return(cols(d.mac2))})
				.style('stroke','#fff')
				.style('stroke-width',function(d){return(d.mac2==99?2:1)})
				.attr("cy",function(d){return(height-(d.pos4/15*height)-25)})
		}
		if(a == 26 && b == 25) {}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 35 && b == 36) {
			var chart = d3.select("#analysis_svg > g");
			var height= $('#analysis_svg').height();
			chart.selectAll('circle')
				.transition().duration(1000)
				.attr('cy',function(d){return(height-(d.pos5/15*height)-25)})
		}
		if(a == 26 && b == 25) {}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 36 && b == 37) {
			$('#analysis_svg').fadeOut(300,function(){
				$(this).empty();
				particles_js('background')
				$("#solutions")
					.html(properties.solution_discussion1)
					.fadeIn(300);
			});
		}
		if(a == 26 && b == 25) {}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 37 && b == 38) {
			$('#solutions').fadeOut(300,function(){
				$("#solutions")
					.html(properties.solution_discussion2)
					.fadeIn(300);
			});
		}
		if(a == 26 && b == 25) {}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 38 && b == 39) {
			$('#solutions').fadeOut(300,function(){
				$("#solutions")
					.html(properties.solution_discussion3)
					.fadeIn(300);
			});
		}
		if(a == 26 && b == 25) {}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 39 && b == 40) {
			$('#solutions').fadeOut(300,function(){
				$('.particles-js-canvas-el').remove();
				$('#signal_strength_con').fadeIn(300);
				$('#signal_strength').fadeIn(300);
			});
		}
		if(a == 26 && b == 25) {}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 40 && b == 41) {
			$('#signal_strength_con').fadeOut(300);
			$('#signal_strength').fadeOut(300,function(){
				$('#analysis_svg').show(function(){
					var width = $(this).width();
					var height = $(this).height();
					var chart = d3.select(this).append('g');
					d3.csv('data/sample_probes.csv',function(pr){
						chart.selectAll('.pr')
							.data(pr)
							.enter()
							.append('circle')
							.attr("cy",function(d){return(height-height*0.33); })
							.attr('cx',width+10)
							.attr('r',10)
							.style("stroke",'#000')
							.style("fill",'#CCC')
							.style("opacity",0.65)
							.transition().duration(500)
							.attr("cx",function(d){return(5+(d.timestamp/5*(width-10)));})
					});
					chart.append('rect')
						.attr('x',0).attr('y',height-(height*0.33))
						.attr('height',1).attr('width',width)
						.style('stroke','#fff')
					chart.append('text')
						.text("Time")
						.attr('class','xaxis_text')
						.attr('x',width/2).attr('y',height-(height*0.33)+50)
						.style('transform','translate(-50% -50%)')
						.style('font-size','12')
						.style('fill','#fff')
						.attr('text-anchor','middle')
				});
			});
		}
		if(a == 26 && b == 25) {}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 41 && b == 42) {
			var width = $('#analysis_svg').width();
			var height = $('#analysis_svg').height();
			var chart = d3.select('#analysis_svg > g');
			chart.selectAll('circle')
				.transition().duration(1000)
				.attr('cy',function(d){return(height-(d.signal/100*height)-25)})
			chart.selectAll('rect').transition().duration(1000)
				.attr('y',height-50)
			chart.selectAll('.xaxis_text').transition().duration(1000)
				.attr('y',height-15)
			chart.append('text')
				.text('Signal Strength')
				.attr('class','yaxis_text')
				.style('transform','translate(-50% -50%)')
				.attr('x',-height+200).attr('y',10)
				.attr('transform','rotate(-90)')
				.style('font-size','12')
				.style('fill','#fff')
				.attr('text-anchor','middle')
		}
		if(a == 26 && b == 25) {}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 42 && b == 43) {
			var chart = d3.select('#analysis_svg > g');
			chart.selectAll('circle')
				.transition().duration(1000)
				.style('stroke','#fff')
				.style('fill',function(d){return(d.signal>40?'#87C38F':'#DA2C38')})
		}
		if(a == 26 && b == 25) {}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 43 && b == 44) {
			var chart = d3.select('#analysis_svg > g');
			chart.selectAll('circle')
				.transition().duration(1000)
				.style('opacity',function(d){return(d.signal>40?0.85:0)})
		}
		if(a == 26 && b == 25) {}



		// Introduction to Smart Street Sensors --------------------------------
		if(a == 44 && b == 45) {
			var width = $('#analysis_svg').width();
			var height = $('#analysis_svg').height();
			var chart = d3.select('#analysis_svg > g');
			chart.selectAll('circle')
				.transition().duration(1000)
				.attr('cy',function(d){return(height-(d.seq/25*height)-25)})
			chart.selectAll('.yaxis_text').transition().duration(1000)
				.text('Sequence Number')
		}
		if(a == 26 && b == 25) {}


		// Introduction to Smart Street Sensors --------------------------------
		if(a == 45 && b == 46) {
			var chart = d3.select('#analysis_svg > g');
			var cols = d3.scale.ordinal().domain([1,2,3,4,5,6,7,8,9,10,'r']).range(['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#aaaaaa']);
			chart.selectAll('circle')
				.transition().duration(1000)
				.style('fill',function(d){return(cols(d.mac))})
		}
		if(a == 26 && b == 25) {}

		// Introduction to Smart Street Sensors --------------------------------
		if(a == 46 && b == 47) {
			$('#analysis_svg').fadeOut(300,function(){
				$(this).empty();
				$("#sequence_numbers_top, #sequence_numbers_bottom").fadeIn(300);
			});
		}
		if(a == 26 && b == 25) {}
		
		// Introduction to Smart Street Sensors --------------------------------
		if(a == 47 && b == 48) {
			$("#sequence_numbers_top").fadeOut(300);
			$('#sequence_numbers_bottom').fadeOut(300,function(){
				$('#solution_chart').show();
				$.getJSON("data/solution.json",function(data){ solution_chart('solution_chart',data); });
			});
		}


		if(a == 48 && b == 49) {
			$("#solution_chart").fadeOut(300,function(){
				particles_js('background');
				$("#conclusions")
					.html(properties.conclusions[0])
					.fadeIn(300);
			});
		}
		
		if(a == 49 && b == 50) {
			$("#conclusions").fadeOut(300,function(){
				$("#conclusions")
					.html(properties.conclusions[1])
					.fadeIn(300);
			});
		}
	
		if(a == 50 && b == 51) {
			$("#conclusions").fadeOut(300,function(){
				$("#conclusions")
					.html(properties.conclusions[2])
					.fadeIn(300);
			});
		}
	
		if(a == 51 && b == 52) {
			$("#conclusions").fadeOut(300,function(){
				$("#conclusions")
					.html(properties.conclusions[3])
					.fadeIn(300);
			});
		}

		if(a == 52 && b == 53) {
			$("#conclusions").fadeOut(300,function(){
				$('.particles-js-canvas-el').remove();
				$('#ridge_plots').fadeIn(300);
			})
		}
	
		if(a == 53 && b == 54) {
			$("#ridge_plots").fadeOut(300,function(){
				$('#calendar').fadeIn(300);
			})		
		}
	
		if(a == 54 && b == 55) {
			$("#calendar").fadeOut(300,function(){
				particles_js('background');
				$("#conclusions")
					.html("Questions?")
					.fadeIn(300);
			});
		}
				
	}
});


$.fn.isInViewport = function() {
	  var tr = d3.transform(d3.select('#map_svg > g').attr('transform')).translate
	  var sc = d3.transform(d3.select('#map_svg > g').attr('transform')).scale
	  var h = $('#map_svg').height()/sc[0]
	  var w = $('#map_svg').width()/sc[1]
	  var x = $(this).attr('cx');
	  var y = $(this).attr('cy');
	  var l = -(tr[0]/sc[0])
	  var r = l+w
	  var t = -(tr[1]/sc[1]);
	  var b = t+h;
	  return  x > l && x < r && y > t && y < b;
};

function update_location_count () {
	$.when($('.inner_marker').each(function(){
		if($(this).isInViewport()){
			$(this).attr("vis","visible")
		}else{
			$(this).attr("vis","hidden")
		}
	})).done(function(){
		$('#loc_sum').text(parseInt($('.inner_marker[vis="visible"]').length));
	});
}

function endall(transition, callback) { 
	  if (typeof callback !== "function") throw new Error("Wrong callback in endall");
	  if (transition.size() === 0) { callback() }
	  var n = 0; 
	  transition 
		  .each(function() { ++n; }) 
		  .each("end", function() { if (!--n) callback.apply(this, arguments); }); 
} 
