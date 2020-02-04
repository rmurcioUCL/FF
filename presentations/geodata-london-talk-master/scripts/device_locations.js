function device_locations() {
	var map_svg = d3.select("#map_svg").call(d3.behavior.zoom()
		.on("zoom", function () {
			map_svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")");
			update_location_count();
		})).append('g')

	var width = $('#map_svg').width();
	var height = $('#map_svg').height();
	var projection = d3.geo.albers()
		.center([1, 54])
		.rotate([4.4, 0])
		.parallels([50, 60])
		.scale(5000)
		.translate([width / 2, height / 2]);
	var path = d3.geo.path().projection(projection);
	d3.json("data/uk.json", function(error, uk) {
		if (error) { return console.error(error); }
		var subunits = topojson.feature(uk, uk.objects.subunits);
		map_svg.selectAll(".subunit")
			.data(subunits.features)
			.enter().append("path")
			.attr("d", path)
			.style('opacity',0.25)
			.style('fill','#666')
			.on('mouseover',
				function(d){ d3.select(this).style('fill','#888888') })
			.on('mouseout',
				function(d){ d3.select(this).style('fill', '#666666') })
		map_svg.append("path")
			.datum(topojson.mesh(uk, uk.objects.subunits, function(a, b) { return a !== b; }))
			.attr("d", path)
			.attr("class", "subunit-boundary");
		d3.csv("data/locations.csv", function(data) {
			$('#map_svg').fadeIn(200,function(){
			map_svg.selectAll(".catchment_marker")
				.data(data).enter().append("circle")
				.attr("cx", function(d) { return projection([d.lon,d.lat])[0]; })
				.attr("cy", function(d) { return projection([d.lon,d.lat])[1]; })
				.attr("r",0).style("opacity",1).style("fill", "#770000")
				.style("pointer-events","none")
				.transition().duration(300).attr('r',2)
			map_svg.selectAll(".inner_marker")
				.data(data).enter().append("circle")
				.attr("cx", function(d) { return projection([d.lon,d.lat])[0]; })
				.attr("cy", function(d) { return projection([d.lon,d.lat])[1]; })
				.attr("r",0).style("opacity",1).style("fill", "#990000")
				.attr("class","inner_marker")
				.style("pointer-events","none")
				.transition().duration(300).attr('r',1.5)
			map_svg.selectAll(".middle_marker")
				.data(data).enter().append("circle")
				.attr("cx", function(d) { return projection([d.lon,d.lat])[0]; })
				.attr("cy", function(d) { return projection([d.lon,d.lat])[1]; })
				.attr("r", 0).style("opacity", 1).style("fill", "#bb0000")
				.style("pointer-events","none")
				.transition().duration(300).attr('r',0.8)
			map_svg.selectAll(".outer_marker")
				.data(data).enter().append("circle")
				.attr("cx", function(d) { return projection([d.lon,d.lat])[0]; })
				.attr("cy", function(d) { return projection([d.lon,d.lat])[1]; })
				.attr("r", 0).style("opacity", 1).style("fill", "#ff1111")
				.style("pointer-events","none")
				.transition().duration(300).attr('r',0.05)
			map_svg.selectAll(".place-label")
				.data(topojson.feature(uk, uk.objects.places).features)
				.enter().append("text")
				.attr("class", "place-label")
				.attr("transform", function(d) { return "translate(" + projection(d.geometry.coordinates) + ")"; })
				.attr("dy", ".01em")
				.style("pointer-events","none")
				.text(function(d) { return d.properties.name; });
			map_svg.selectAll(".place-label")
				.attr("x", function(d) { return d.geometry.coordinates[0] > -1 ? 6 : -6; })
				.style("pointer-events","none")
				.style("text-anchor", function(d) { return d.geometry.coordinates[0] > -1 ? "start" : "end"; });
			map_svg.selectAll(".subunit-label")
				.data(topojson.feature(uk, uk.objects.subunits).features)
				.enter().append("text")
				.attr("class", function(d) { return "subunit-label " + d.id; })
				.attr("transform", function(d) { return "translate(" + path.centroid(d) + ")"; })
				.attr("dy", ".35em")
				.style("pointer-events","none")
				.text(function(d) { return d.properties.name; }); 
			});
		});
	});
}
