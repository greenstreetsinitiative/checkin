var margins = {top: 20, right: 300, bottom: 35, left: 40},
    w = 800 - margins.left - margins.right,
    h = 500 - margins.top - margins.bottom;

// var datas = JSON.parse('[["n", "b", 32, 26], ["n", "b", 33, 46], ["n", "b", 34, 39], ["n", "b", 35, 39], ["n", "b", 36, 43], ["n", "b", 37, 64], ["n", "da", 32, 20], ["n", "da", 33, 53], ["n", "da", 34, 45], ["n", "da", 35, 58], ["n", "da", 36, 46], ["n", "da", 37, 94], ["n", "dalt", 32, 1], ["n", "dalt", 33, 5], ["n", "dalt", 34, 2], ["n", "dalt", 35, 6], ["n", "dalt", 36, 3], ["n", "dalt", 37, 3], ["n", "o", 35, 1], ["n", "r", 32, 1], ["n", "r", 35, 1], ["n", "t", 32, 49], ["n", "t", 33, 56], ["n", "t", 34, 67], ["n", "t", 35, 55], ["n", "t", 36, 46], ["n", "t", 37, 74], ["n", "tc", 35, 1], ["n", "tc", 36, 1], ["n", "w", 32, 36], ["n", "w", 33, 55], ["n", "w", 34, 75], ["n", "w", 35, 60], ["n", "w", 36, 63], ["n", "w", 37, 101], ["w", "b", 32, 27], ["w", "b", 33, 51], ["w", "b", 34, 39], ["w", "b", 35, 46], ["w", "b", 36, 46], ["w", "b", 37, 70], ["w", "da", 32, 15], ["w", "da", 33, 51], ["w", "da", 34, 45], ["w", "da", 35, 57], ["w", "da", 36, 41], ["w", "da", 37, 90], ["w", "dalt", 32, 1], ["w", "dalt", 33, 5], ["w", "dalt", 34, 2], ["w", "dalt", 35, 4], ["w", "dalt", 36, 3], ["w", "dalt", 37, 3], ["w", "o", 35, 1], ["w", "r", 32, 1], ["w", "r", 33, 1], ["w", "r", 34, 2], ["w", "r", 35, 1], ["w", "r", 36, 1], ["w", "t", 32, 48], ["w", "t", 33, 63], ["w", "t", 34, 69], ["w", "t", 35, 61], ["w", "t", 36, 48], ["w", "t", 37, 80], ["w", "tc", 32, 1], ["w", "tc", 35, 1], ["w", "tc", 36, 4], ["w", "tc", 37, 1], ["w", "w", 32, 46], ["w", "w", 33, 61], ["w", "w", 34, 79], ["w", "w", 35, 64], ["w", "w", 36, 68], ["w", "w", 37, 105]]');

// var datas = {{ checkinsByMode | safe }};

var stackifyData = function(data, dayType) {
    if(dayType !== 'n' && dayType !== 'w') {
      return 0;
    }
    // Extract and organize the relevant data, but in a dict first
    var stackDict = {};
    data.forEach(function(element) {
      if ( element[0] === dayType ) {
        try {
            stackDict[ element[1] ].push( { "x": element[2] - 32,
                                            "y": element[3] });
        }
        catch (TypeError) {
          stackDict[ element[1] ] = [
              {
                "x": element[2] - 32,
                "y": element[3]
              }
          ];
        }
      }
    });
    // Get number of months
    var numMonths = 0;
    for(var key in stackDict) {
      if ( stackDict[key].length > numMonths ) {
        numMonths = stackDict[key].length;
      }
    }
    // Deal with months in which no one checked in by a certain method
    for (var key in stackDict) {
        var missing = [];
        for(var i = 0; i < numMonths; i++) {
            missing.push(i);
        }
        stackDict[key].forEach(function(value) {
            missing.splice(missing.indexOf(value.x), 1);
        });
      missing.forEach(function(x){
        stackDict[key].push({"x": x, "y": 0});
      });
    }
    // Convert into an array
    var stack = [];
    for(key in stackDict) {
      stack.push(stackDict[key]);
    }
    return stack;
}

var barchart = function(day) {
  if(day !== 'w' && day !== 'n'){ console.log('Invalid input.'); return 0; }

  var stack = d3.layout.stack();
  var dataset = stack(stackifyData(datas, day));

  var xScale = d3.scale.ordinal()
    .domain(d3.range(dataset[0].length))
    .rangeRoundBands([0, w], 0.05);

  var xAxis = d3.svg.axis()
    .scale(xScale)
    .tickFormat(function(d){
      return [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ][(d+3)%12];
    })
    .orient("bottom");

  var yScale = d3.scale.linear()
    .domain([0,
      d3.max(dataset, function(d) {
        return d3.max(d, function(d) {
          return d.y0 + d.y;
        });
      })
    ])
    .range([h,0]);

  var yAxis = d3.svg.axis()
    .scale(yScale)
    .ticks(5)
    .orient("left")

  var colors = d3.scale.category20c();

  //Create SVG element
  var svg = d3.select(".checkins-barchart")
    .attr("width", w + margins.left + margins.right)
    .attr("height", h + margins.top + margins.bottom)
    .append("g")
    .attr("transform", "translate(" + margins.left + "," + margins.top + ")");

  // Add a group for each row of data
  var groups = svg.selectAll("g")
    .data(dataset)
    .enter()
    .append("g")
    .style("fill", function(d, i) {
      return colors(i);
    })

  // Add a rect for each data value
  var rects = groups.selectAll("rect")
    .data(function(d) { return d; })
    .enter()
    .append("rect")
    .attr("x", function(d, i) {
      return xScale(i);
    })
    .attr("width", xScale.rangeBand())
    .attr("y", function(d) {
      //return yScale(d.y0);
      return yScale(d.y) + yScale(d.y0) - h;
    })
    .attr("height", function(d) {
      //return yScale(d.y);
      return h - yScale(d.y);
    })
    .on("mouseover", function() { tooltip.style("display", null); })
    .on("mouseout", function() { tooltip.style("display", "none"); })
    .on("mousemove", function(d) {
      var xPosition = d3.mouse(this)[0] - 15;
      var yPosition = d3.mouse(this)[1] - 25;
      tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
      tooltip.select("text").text(d.y);
    })

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + h + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

  c = [];
  for(var i = 0; i<8; i++){
    c.push(colors(i));
  }

  var legend = svg.selectAll(".legend")
    .data(c)
    .enter().append("g")
    .attr("class", "legend")
    .attr("transform", function(d, i) { return "translate(30," + i * 19 + ")"; });

  legend.append("rect")
    .attr("x", w - 18)
    .attr("width", 18)
    .attr("height", 18)
    .style("fill", function(d, i) {return c.slice().reverse()[i];});

  legend.append("text")
    .attr("x", w + 5)
    .attr("y", 9)
    .attr("dy", ".35em")
    .style("text-anchor", "start")
    .text(function(d, i) {
      switch (i) {
        case 0: return "Walking";
        case 1: return "Telecommuting";
        case 2: return "Public Transit";
        case 3: return "Running or Jogging";
        case 4: return "Other";
        case 5: return "Driving Alone (alternate vehicle)";
        case 6: return "Driving Alone";
        case 7: return "Biking";
      }
    });

  // Prep the tooltip bits, initial display is hidden
  var tooltip = svg.append("g")
    .attr("class", "tooltip")
    .style("display", "none");

  tooltip.append("rect")
    .attr("width", 30)
    .attr("height", 20)
    .attr("fill", "white")
    .style("opacity", 0.5);

  tooltip.append("text")
    .attr("x", 15)
    .attr("dy", "1.2em")
    .style("text-anchor", "middle")
    .attr("font-size", "12px")
    .attr("font-weight", "bold");
}

d3.selectAll("input")
  .on("change", function() {
    var val = this.value;
    if(val === 'n' || val === 'w') {
      d3.select(".checkins-barchart")
        .selectAll('g')
        .remove();
      barchart(val);
    }
  });


barchart('w');