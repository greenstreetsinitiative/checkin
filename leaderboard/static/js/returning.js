employer.domain = [];
employer.stack = [[],[]];
employer.checkins.forEach(function(d) {
  employer.domain.push([ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ][(d.month-5)%12]);
  d.percent = d.all / employer.size;
  employer.stack[0].push({'x': d.month-32, 'y': d.all - d.new});
  employer.stack[1].push({'x': d.month-32, 'y': d.new});
});

//Width and height
var margin = {top: 20, right: 120, bottom: 35, left: 65},
    width = 650 - margin.left - margin.right,
    height = 350 - margin.top - margin.bottom;

var stack = d3.layout.stack();
stack(employer.stack);

//Set up scales
var xScale = d3.scale.ordinal()
  .domain(d3.range(employer.stack[0].length))
  .rangeRoundBands([0, width], 0.01);

var xAxis = d3.svg.axis()
  .scale(xScale)
  .tickFormat(function(d){
    return [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ][(d+3)%12];
  })
  .orient("bottom");

var yScale = d3.scale.linear()
  .domain([0,d3.max(employer.stack, function(d) {
      return d3.max(d, function(d) {
        return d.y0 + d.y;
      });
    })
  ])
  .range([height, 0]);

var yAxis = d3.svg.axis()
  .scale(yScale)
  .ticks(5)
  .orient("left")

var colors = function(color) {
    return ['#31a354','#74c476'][color%2];
};

//Create SVG element
var svg = d3.select(".barchart")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Add a group for each row of data
var groups = svg.selectAll("g")
  .data(employer.stack)
  .enter()
  .append("g")
  .style("fill", function(d, i) {
    return colors(i);
  });

// Add a rect for each data value
var rects = groups.selectAll("rect")
  .data(function(d) { return d; })
  .enter()
  .append("rect")
  .attr("x", function(d, i) {
    return xScale(i);
  })
  .attr("y", function(d) {
    return yScale(d.y) + yScale(d.y0) - height;
  })
  .attr("height", function(d) {
    return height - yScale(d.y);
  })
  .attr("width", xScale.rangeBand())
  .on("mouseover", function() { tooltip.style("display", null); })
  .on("mouseout", function() { tooltip.style("display", "none"); })
  .on("mousemove", function(d) {
    var xPosition = d3.mouse(this)[0] - 15;
    var yPosition = d3.mouse(this)[1] - 25;
    tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
    tooltip.select("text").text(d.y);
  });

svg.append("g")
    .attr("class", "x-axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

svg.append("g")
    .attr("class", "y-axis")
    .call(yAxis);

svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left)
    .attr("x",0 - (height / 2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .text("Unique checkins each month");

var c = [colors(0), colors(1)];

var legend = svg.selectAll(".legend")
  .data(c)
  .enter().append("g")
  .attr("class", "legend")
  .attr("transform", function(d, i) { return "translate(30," + i * 19 + ")"; });

legend.append("rect")
  .attr("x", width - 18)
  .attr("width", 18)
  .attr("height", 18)
  .style("fill", function(d, i) {return c.slice().reverse()[i];});

legend.append("text")
  .attr("x", width + 5)
  .attr("y", 9)
  .attr("dy", ".35em")
  .style("text-anchor", "start")
  .text(function(d, i) {
    switch (i) {
      case 0: return "New";
      case 1: return "Returning";
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