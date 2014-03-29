$(function() {
  var cs = {}, // formdata
      map, geocoder, directionsService, directionsDisplay;

  // map & locations
  geocoder = new google.maps.Geocoder();
  directionsService = new google.maps.DirectionsService();
  directionsDisplay = new google.maps.DirectionsRenderer({
    markerOptions: {
      visible: false
    }
  });

  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 11,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    center: new google.maps.LatLng(42.357778, -71.061667),
    streetViewControl: false,
    mapTypeControl: false
  });

  // geocode address
  function geocodeAddress($address) {
    geocoder.geocode({address: $address.val()}, function(results, status) {
      var marker, $helptxt, 
          id = $address.attr('id');

      $address.next('.text-danger').remove();

      if (status == google.maps.GeocoderStatus.OK) {
        
        $address.val(results[0]['formatted_address']);

        cs[id] = cs[id] || {};
        cs[id].name = results[0]['formatted_address'];
        cs[id].position =results[0].geometry.location;
        if (cs[id].marker === undefined) {
          cs[id].marker = new google.maps.Marker({
            map: map,
            title: results[0]['formatted_address'],
            position: results[0].geometry.location,
            animation: google.maps.Animation.DROP
          });
        } else {
          cs[id].marker.setPosition(results[0].geometry.location);
        }
        
        if (cs.home_address && cs.work_address) {
          setCommuteGeom(cs.home_address.position, cs.work_address.position);
        } else {
          map.panTo(results[0].geometry.location);
        }

      } else {
        $helptxt = $('<span />', {
          class: 'text-danger'
        }).html('We were not able to locate this address.');
        $address.after($helptxt);
        if (cs[id]) {
          cs[id].marker.setMap(null);
          delete cs[id];
        }
        toggleCalculator('disable');
      }
    });
  }

  function setCommuteGeom(origin, destination) {
    directionsService.route({
      origin: origin,
      destination: destination,
      travelMode: google.maps.TravelMode.BICYCLING
    }, function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        directionsDisplay.setMap(map);
        directionsDisplay.setDirections(response);
        $('#commute-distance').text(response.routes[0].legs[0].distance.text + ' (by bike)');
        cs.geom = pathToGeoJson(response.routes[0].overview_path);
        cs.distance = response.routes[0].legs[0].distance.value; // Meters
        cs.duration = response.routes[0].legs[0].duration.value; // Seconds
        toggleCalculator('enable');
      } else {
        toggleCalculator('disable');
      }
    });
  }

  function pathToGeoJson(path) {
    return {
      type: 'MultiLineString',
      coordinates: [
        $.map(path, function(v,i) {
          return [[v.lng(), v.lat()]];
        })
      ]
    };
  }

  function toggleCalculator(status) {
    // we don't know distance and duration
    if (status === 'disable') {
      delete cs.distance;
      delete cs.duration;
      directionsDisplay.setMap(null);
      $('.calculator button').prop('disabled', true);
    } else if (status === 'enable') {
      $('.calculator button').prop('disabled', false);
    }
  }

  // hide extra questions 
  $("#ToNormNo").hide();
  $types2 = $('.ToNorm');
  $away2 = $('#ToNormNo');
  $types2.change(function() {
      $this = $(this).val();
      if ($this == "ToNormNo") {
          $away2.show(500);
                  }
      else  {
          $away2.hide(250);
      }
  });   

  $("#AwayNormNo").hide();
  $types = $('.AwayNorm');
  $away = $('#AwayNormNo');
  $types.change(function() {
      $this = $(this).val();
      if ($this == "AwayNormNo") {
          $away.show(500);
                  }
      else  {
          $away.hide(250);
      }
  }); 

  // trigger address geocoder on several UI interactions
  $('.btn.locate-address').on('click', function(event) {
    event.preventDefault();
    var $address = $(this).parent().prev().find('input.address');
    geocodeAddress($address);
  });
  $('input.address').on('keyup', function(event) {
    if (event.which === 13) geocodeAddress($(this));
  });

  // toggle more legs options
  $('input.morelegs:radio').on('change', function(event) {
    var targetLegs = $(this).attr('name'),
        $targetLegsContainer = $('#' + targetLegs).parent(); 
    $targetLegsContainer.toggle(100);
  });
  
  // add another leg
  $('.btn.morelegs').on('click', function(event) {
    event.preventDefault();
    var targetLegs = $(this).data('target'),
        $targetLegs = $('#' + targetLegs),
        $lastLeg = $('.leg:last', $targetLegs),
        $removeLegBtn = $('<button class="btn btn-danger"><span class="button">X</span></button>'),
        $newLeg;

    $newLeg = $lastLeg
    .clone()
    .appendTo($targetLegs);

    $removeLegBtn.on('click', function(event) {
      event.preventDefault();
      var $leg = $(this).parentsUntil($targetLegs);
      $leg.remove();
    });
    $('div:first-child', $newLeg)
    .addClass('right')
    .html($removeLegBtn);
  });

  // returns array of all valid commute legs
  function collectAllLegs() {
    var legs = [];
    $('div.leg:visible').each(function() {
      var mode = $('select[name=mode]', this).val(),
          time = $('select[name=time]', this).val();
      if (mode && time) {
        legs.push({
          mode: mode,
          time: time,
          day: $('input[name=day]', this).val(),
          direction: $('input[name=direction]', this).val()
        });
      }
    });
    $('input.morelegs.yes:radio:checked').each(function() {
      var legType = $(this).attr('name');
      $.merge(legs, duplicateLegs(legType, legs));
    });
    return legs;
  }

  // returns array with duplicated legs
  // according to a given set of rules
  function duplicateLegs(legType, legs) {
    return {
      'w-from-work-legs': function() {
        var dLegs = $.grep(legs, function(l,i) {
          return l.day === 'w' && l.direction === 'tw';
        }).reverse();
        return $.map(dLegs, function(l,i) {
          return $.extend({}, l, { direction: 'fw' });
        });
      },
      'n-to-work-legs': function() {
        var dLegs = $.grep(legs, function(l,i) {
          return l.day === 'w' && l.direction === 'tw';
        });
        return $.map(dLegs, function(l,i) {
          return $.extend({}, l, { day: 'n' });
        });
      },
      'n-from-work-legs': function() {
        var dLegs = $.grep(legs, function(l,i) {
          return l.day === 'n' && l.direction === 'tw';
        }).reverse();
        return $.map(dLegs, function(l,i) {
          return $.extend({}, l, { direction: 'fw' });
        });
      }
    }[legType]();
  }

  // calculate CO2 for Walk/Ride day
  // approximation by using time for non-car legs 
  // to estimate proportional non-car distance
  $('#btn-co2').on('click', function(event) {
    event.preventDefault();
    var legs = collectAllLegs(),
        wLegs, distanceNoCar, savedCO2,
        timeTotal = 0, 
        timeNoCar = 0;

    wLegs = $.grep(legs, function(l,i) {
      return l.day === 'w';
    });
    $.each(wLegs, function(i,l) {
      timeTotal += parseInt(l.time);
      if (['da', 'dalt', 'cp'].indexOf(l.mode) === -1) timeNoCar += parseInt(l.time);
    });
    if (timeNoCar === 0) {
      $('#saved-co2').text('You didn\'t save CO2 emissions on Walk/Ride Day');
    } else {
      distanceNoCar = ( parseInt(cs.distance) * 2 / timeTotal ) * timeNoCar;
      // EPA standard: 0.41kg CO2 per mile driven 
      // (convert to lbs and meters)
      savedCO2 = 0.41 * 2.20462262 * distanceNoCar / 1609.344;
      $('#saved-co2').text('You saved ' + Math.round(savedCO2) + ' lbs CO2 emissions on Walk/Ride Day');
    }
  });

  // calculate calories: kcal = METS * hours * kg
  // http://en.wikipedia.org/wiki/Metabolic_equivalent
  $('#btn-cal').on('click', function(event) {
    event.preventDefault();
    var legs = collectAllLegs(),
        weight, METS, wlegs,
        calories = 0;

    METS = {
      'b': 4.0,
      'r': 7.0,
      'w': 3.3,
      'o': 3.5
    };
    weight = parseInt($('#weight').val());
    wLegs = $.grep(legs, function(l,i) {
      return l.day === 'w';
    });
    $.each(wLegs, function(i,l) {
      calories += (METS[l.mode] || 0) * ((l.time || 0) * 0.25) * (weight * 0.4536);
    });
    if (calories > 0) {
      $('#burned-cal').text('You burned ' + Math.round(calories) + ' extra calories on Walk/Ride Day');
    } else {
      $('#burned-cal').text('You didn\'t burn extra calories on Walk/Ride Day');
    }
  });
});
