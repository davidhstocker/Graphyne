function InitChart() {
    var vis = d3.select("#visualisation");
    WIDTH = 1000;
    HEIGHT = 500;
    MARGINS = {top: 20, right: 20, bottom: 20, left: 50};
    xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([ranges.xMin, ranges.xMax]);
    yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([ranges.yMin, ranges.yMax]);
    xAxis = d3.svg.axis().scale(xScale);
    yAxis = d3.svg.axis().scale(yScale).orient("left");
    var verticalRange = HEIGHT - MARGINS.top - MARGINS.bottom;
    vis.append("svg:g").attr("class", "x axis").attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")").call(xAxis).append("text").attr("transform", "translate("+ WIDTH/2 + ", 35)").style("text-anchor", "middle").text("Entity Count");
    vis.append("svg:g").attr("class", "y axis").attr("transform", "translate(" + (MARGINS.left) + ",0)").call(yAxis).append("text").attr("transform", "translate(" + (20) + ", " + HEIGHT/2 + "), rotate(-90)").style("text-anchor", "middle").text("Time (s)");
    var lineGen = d3.svg.line().x(function(d) {return xScale(d.entityCount);}).y(function(d) {return yScale(d.testTime);}).interpolate("basis");
    var yRange = {};
    for (l = 0; l < data.length; l++) {
    	var currData = data[l];
    	if (currData.length > 0){
		  	for (j = 0; j < currData.length; j++) { 
		  		if (yRange.upper == undefined){
		  			yRange.upper = currData[j].testTime; 
		  		}
		  		else if (currData[j].testTime > yRange.upper){
		  			yRange.upper = currData[j].testTime;
		  		}
		  	}
		  	for (k = 0; k < currData.length; k++) { 
		  		if (yRange.lower == undefined){
		  			yRange.lower = currData[k].testTime; 
		  		}
		  		else if (currData[k].testTime < yRange.lower){
		  			yRange.lower = currData[k].testTime;
		  		}
		  	}
    	}
    }
    yRange.delta = yRange.upper - yRange.lower;
    
    for (i = 0; i < data.length; i++) { 
    	var currData = data[i];
    	if (currData.length > 0){
	    	var currDataLast = currData.length-1;
	    	vis.append('svg:path').attr('d', lineGen(currData)).attr('stroke', 'black').attr('stroke-width', 2).attr('fill', 'none').append("text").attr("dy", ".71em").attr("transform", "translate(50,50)").style("text-anchor", "end").text(labels[i]);
	    	var relativeHieght = ((ranges.yMax - currData[currDataLast].testTime)/ranges.yMax);
	    	var yTextPosition = verticalRange * relativeHieght
	    	vis.append("text").attr("dy", ".71em").attr("transform", "translate("+ (WIDTH - MARGINS.right) +","+ yTextPosition +")").style("text-anchor", "end").text(labels[i]);
    	}
    }
}