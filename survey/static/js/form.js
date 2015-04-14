$(function() {
  //activate chosen plugin
  $("#employer").chosen({
    width: "99%"
  });

  var cs, // commutersurvey data
      map, geocoder, directionsService, directionsDisplay;

  // map & locations
  geocoder = new google.maps.Geocoder();
  directionsService = new google.maps.DirectionsService();
  directionsDisplay = new google.maps.DirectionsRenderer({
    markerOptions: {
      visible: false
    }
  });

  directionsService2 = new google.maps.DirectionsService();
  directionsDisplay2 = new google.maps.DirectionsRenderer({
    markerOptions: {
      visible: false
    },
    polylineOptions: {
      strokeColor: '#CDAAFF'
    }
  });

  directionsService3 = new google.maps.DirectionsService();
  directionsDisplay3 = new google.maps.DirectionsRenderer({
    markerOptions: {
      visible: false
    },
    polylineOptions: {
      strokeColor: '#FF9966'
    }
  });

  // read cache or use empty value for employer
  cs = simpleStorage.get('commutersurvey') || { 
    employer: ''
  };
  // fix for accidently cached W/R month
  if (cs.wr_day_month) delete cs.wr_day_month;

  // remove cached optional questions
  var optionalquestions = ['comments', 'health', 'weight', 'height', 'gender', 'gender_other', 'cdays', 'caltdays', 'cpdays', 'tdays', 'bdays', 'rdays', 'wdays', 'odays', 'tcdays', 'lastweek', 'cdaysaway', 'caltdaysaway', 'cpdaysaway', 'tdaysaway', 'bdaysaway', 'rdaysaway', 'wdaysaway', 'odaysaway', 'tcdaysaway', 'outsidechanges', 'affectedyou', 'contact', 'volunteer'];
  
  $.each(optionalquestions, function(i,q) {
    if (cs[q]) delete cs[q];
  });

 
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 11,
    mapTypeId: google.maps.MapTypeId.TERRAIN,
    center: new google.maps.LatLng(42.357778, -71.061667),
    streetViewControl: false,
    mapTypeControl: false
  });

  // geocode address
  function geocodeAddress($address) {
    geocoder.geocode({address: $address.val()}, function(results, status) {
      var marker, $helptxt, 
          location = $address.attr('id').replace('address', 'location');

      $address.next('.text-danger').remove();

      if (status == google.maps.GeocoderStatus.OK) {
        
        $address.val(results[0]['formatted_address']);

        cs[location] = cs[location] || {};
        cs[location].name = results[0]['formatted_address'];
        cs[location].position =results[0].geometry.location;
        if (cs[location].marker === undefined) {
          cs[location].marker = new google.maps.Marker({
            map: map,
            title: results[0]['formatted_address'],
            position: results[0].geometry.location,
            animation: google.maps.Animation.DROP
          });
        } else {
          cs[location].marker.setPosition(results[0].geometry.location);
        }
        
        if (cs.home_location && cs.work_location) {
          setCommuteGeom(cs.home_location.position, cs.work_location.position);
          setCommuteGeom2(cs.home_location.position, cs.work_location.position);
          setCommuteGeom3(cs.home_location.position, cs.work_location.position);
        } else {
          map.panTo(results[0].geometry.location);
        }

      } else {
        $helptxt = $('<span />', {
          'class': 'text-danger'
        }).html('We were not able to locate this address.');
        $address.after($helptxt);
        if (cs[location]) {
          cs[location].marker.setMap(null);
          delete cs[location];
        }
        toggleCommuteDistance('');
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
        cs.geom = pathToGeoJson(response.routes[0].overview_path);
        cs.distance = response.routes[0].legs[0].distance.value; // Meters
        cs.duration = response.routes[0].legs[0].duration.value; // Seconds
        toggleCommuteDistance(response.routes[0].legs[0].distance.text + ' (by bike)');
        toggleCalculator('enable');
      } else {
        toggleCommuteDistance('');
        toggleCalculator('disable');
      }
    });
  }

  function setCommuteGeom2(origin, destination) {
    directionsService2.route({
      origin: origin,
      destination: destination,
      travelMode: google.maps.TravelMode.TRANSIT
    }, function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        directionsDisplay2.setMap(map);
        directionsDisplay2.setDirections(response);
        cs.distance = response.routes[0].legs[0].distance.value; // Meters
        cs.duration = response.routes[0].legs[0].duration.value; // Seconds
        toggleCommuteDistance2(response.routes[0].legs[0].distance.text + ' (by transit)');
        toggleCalculator('enable');
      } else {
        toggleCommuteDistance2('');
        toggleCalculator('disable');
      }
    });
  }

  function setCommuteGeom3(origin, destination) {
    directionsService3.route({
      origin: origin,
      destination: destination,
      travelMode: google.maps.TravelMode.WALKING
    }, function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        directionsDisplay3.setMap(map);
        directionsDisplay3.setDirections(response);
        cs.distance = response.routes[0].legs[0].distance.value; // Meters
        cs.duration = response.routes[0].legs[0].duration.value; // Seconds
        toggleCommuteDistance3(response.routes[0].legs[0].distance.text + ' (by foot)');
        toggleCalculator('enable');
      } else {
        toggleCommuteDistance3('');
        toggleCalculator('disable');
      }
    });
  }

  function toggleCommuteDistance(text) {
    if (text !== '') {
      $('#commute-distance').text(text);
      $('#commute-distance').css('background', '#77C5F1');
    } else {
      $('#commute-distance').text('');
      $('#commute-distance').css('background', '#fff');
    }
  }

  function toggleCommuteDistance2(text) {
    if (text !== '') {
      $('#commute-distance2').text(text);
      $('#commute-distance2').css('background', '#CDAAFF');
    } else {
      $('#commute-distance2').text('');
      $('#commute-distance2').css('background', '#fff');
    }
  }

  function toggleCommuteDistance3(text) {
    if (text !== '') {
      $('#commute-distance3').text(text);
      $('#commute-distance3').css('background', '#FF9966');
    } else {
      $('#commute-distance3').text('');
      $('#commute-distance3').css('background', '#fff');
    }
  }

  function pathToGeoJson(path) {
    if (path.length <= 1) {
      // point if home and work location are the same;
      // empty coordinates is a valid MultiLineString in GEOS,
      // only one coordinate is not
      return { type: 'MultiLineString', coordinates: [] };
    } else {
      return {
        type: 'MultiLineString',
        coordinates: [
          $.map(path, function(v,i) {
            return [[v.lng(), v.lat()]];
          })
        ]
      };
    }
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

  // trigger address geocoder on several UI interactions
  $('input.address').on('keyup', function(event) {
    if (event.which === 13) geocodeAddress($(this));
  });
  $('input.address').on('blur', function(event) {
    geocodeAddress($(this));
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
    addLeg($(this).data('target'));
  });

  function addLeg(group, legData) {
    var $container = ('#' + group),
        $lastLeg = $('.leg:last', $container),
        $removeLeg = $('<a href="" class="text-danger"> remove</a>'),
        $then = $('<label>then </label>'),
        $newLeg;

    $newLeg = $lastLeg
    .clone()
    .toggleClass('legB')
    .appendTo($container);

    if (legData) {
      $.each(legData, function(k,v) {
        $('[name=' + k +']', $newLeg).val(v);
      });
    }

    $removeLeg.on('click', function(event) {
      event.preventDefault();
      var $leg = $(this).parentsUntil($container);
      $leg.remove();
    });

    $('span.remove', $newLeg)
    .html($removeLeg);

    $('label.then', $newLeg)
    .html('then &nbsp; I');
  }

  // returns array of all valid commute legs
  function collectAllLegs() {
    var legs = [];
    $('div.leg:visible').each(function() {
      var transport_mode = $('select[name=transport_mode]', this).val(),
          duration = $('select[name=duration]', this).val();
      if (transport_mode && duration) {
        legs.push({
          transport_mode: transport_mode,
          duration: duration,
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
  // approximation by using duration for non-car legs 
  // to estimate proportional non-car distance
  $('#btn-co2').on('click', function(event) {
    event.preventDefault();
    var legs = collectAllLegs(),
        wLegs, distanceNoCar, savedCO2,
        durationTotal = 0, 
        durationNoCar = 0;

    wLegs = $.grep(legs, function(l,i) {
      return l.day === 'w';
    });
    $.each(wLegs, function(i,l) {
      durationTotal += parseInt(l.duration);
      if ($.inArray(l.transport_mode, ['da', 'dalt', 'cp']) === -1) durationNoCar += parseInt(l.duration);
    });
    if (durationNoCar === 0) {
      $('#saved-co2').text('You didn\'t save CO2 emissions on Walk/Ride Day');
    } else {
      distanceNoCar = ( parseInt(cs.distance) * 2 / durationTotal ) * durationNoCar;
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
    weight = parseInt($('#weight_cal').val());
    wLegs = $.grep(legs, function(l,i) {
      return l.day === 'w';
    });
    $.each(wLegs, function(i,l) {
      calories += (METS[l.transport_mode] || 0) * ((l.duration || 0) * 0.25) * (weight * 0.4536);
    });
    if (calories > 0) {
      $('#burned-cal').text('You burned ' + Math.round(calories) + ' extra calories on Walk/Ride Day');
    } else {
      $('#burned-cal').text('You didn\'t burn extra calories on Walk/Ride Day');
    }
  });

  //toggle additional checkin questions
  $('#button_submit_optional').on('click', function(e){
    e.preventDefault();

    $('fieldset#optional').show();

    $('p#optional').hide();
    $('#button_submit_optional').hide();

  });

  // in optional question section
  function duplicateLastWeek(data) {
    var lastWeekDays = ['caltdays', 'cpdays', 'tdays', 'tdays', 'bdays', 'rdays', 'wdays', 'odays', 'tcdays'];
    $.each(lastWeekDays, function(i,v) {
      data[v + 'away'] = data[v];
    });
    return data;
  }

  function collectFormData() {
    var fields = ['wr_day_month', 'share', 'name', 'email', 'employer', 'home_address', 'work_address', 'comments', 'health', 'weight', 'height', 'gender', 'gender_other', 'cdays', 'caltdays', 'cpdays', 'tdays', 'bdays', 'rdays', 'wdays', 'odays', 'tcdays', 'lastweek', 'cdaysaway', 'caltdaysaway', 'cpdaysaway', 'tdaysaway', 'bdaysaway', 'rdaysaway', 'wdaysaway', 'odaysaway', 'tcdaysaway', 'outsidechanges', 'affectedyou', 'contact', 'volunteer'],
        formData = {};

    $.each(fields, function(i,f) {
      var $field = $('#' + f);
      if ($field.attr('type') === 'checkbox') {
        formData[f] = $field.prop('checked'); 
      } else if ($('input[name=' + f + ']').attr('type') === 'radio') {
        formData[f] = $('input[name=' + f + ']:radio:checked').val();
      } else {
        formData[f] = $field.val();
      }
    });
    formData = (formData.lastweek === 'y') ? duplicateLastWeek(formData) : formData;
    formData.legs = collectAllLegs();
    return formData;
  }

  function addErrorMsg($element, text) {
    $errorMsg = $('<div />', {
      'class': 'alert alert-danger alert-dismissable validation-error'
    }).html(text);
    $element.after($errorMsg);
    $('#notvalidated').show();
  }

  function validate(surveyData) {
    var emailRe = /^([a-zA-Z0-9_\.\-\+\'])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/,
        minLegs,
        isValid = true;

    // clear previous errors
    $('.validation-error').remove();
    $('#notvalidated').hide();
    // month
    if (!$('#wr_day_month').val()) {
      addErrorMsg($('#wr_day_month'), 'Error: Please choose the Walk/Ride Day for your Checkin.');
      isValid = false;
    }
    // email
    if (!emailRe.test(surveyData.email)) {
      addErrorMsg($('#email'), 'Error: Please provide a valid email-address.');
      isValid = false;
    }

    // EMPLOYER
    if (!$('#employer').val()) {
      addErrorMsg($('#employer'), 'Error: Please provide an employer or other entity.');
      isValid = false;
    }

    // home and work address
    $('.address').each(function(a,i) {
      if (!$(this).val()) {
        addErrorMsg($(this), 'Error: Please provide a valid street address.');
        isValid = false;
      }
    });
    // minimum legs
    minLegs = [{
      element: '#w-to-work-legs',
      day: 'w',
      direction: 'tw'
    }, {
      element: '#w-from-work-legs',
      day: 'w',
      direction: 'fw'
    }];
    $.each(minLegs, function(i,leg) {
      var validLegs = $.grep(surveyData.legs, function(l,i) {
        return l.day === leg.day && l.direction === leg.direction;
      });
      if (validLegs < 1) {
        addErrorMsg($(leg.element).next(), 'Error: Please provide at least one commute leg with transportation mode and estimated time.');
        isValid = false;
      }
    });
    return isValid;
  }

  function cache(data) {
    var noCacheKeys = ['wr_day_month', 'home_location', 'work_location', 'geom'],
        cacheData = $.extend(true, {}, data);
    
    $.each(noCacheKeys, function(i,v) {
      if (cacheData[v]) delete cacheData[v];
    });
    return simpleStorage.set('commutersurvey', cacheData);
  }

  // remove empty values, invalid numbers and stringify JSON objects
  function djangofy(data) {
    var intFields = ['health', 'cdays', 'caltdays', 'cpdays', 'tdays', 'bdays', 'rdays', 'wdays', 'odays', 'tcdays', 'cdaysaway', 'caltdaysaway', 'cpdaysaway', 'tdaysaway', 'bdaysaway', 'rdaysaway', 'wdaysaway', 'odaysaway', 'tcdaysaway'];

    delete data['home_location'];
    delete data['work_location'];
    $.each(data, function(k,v) {
      if (!v || (!parseInt(v) && $.inArray(k, intFields) > -1)) delete data[k];
      if (typeof v === 'object') {
        data[k] = JSON.stringify(v);
      }
    })
    return data;
  }

  function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  // submit formdata
  $('button.btn-form-submit').on('click', function(event) {
    event.preventDefault();
    var surveyData;
    
    surveyData = $.extend({}, cs, collectFormData());

    if (!validate(surveyData)) return;

    // show optional questions and exit
    if ($(this).hasClass('optional')) {
      $('input[name=lastweek]:radio').on('change', function() {
        $('#lastweekaway').toggle(100);
      });
      $('#optional-questions').show(100);
      $('button.btn-form-submit.optional').remove();
      return;
    }

    // set local cache
    cache(surveyData); 

    // POST data
    $.ajaxSetup({
      crossDomain: false, // obviates need for sameOrigin test
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
          xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
        }
      }
    });
    $.ajax({
      type: 'POST',
      url: '/api/survey/',
      data: djangofy(surveyData)
    }).done(function() {
      window.location.href = '/commuterform/complete/';
    }).fail(function() {
      alert('An error occured and your checkin could not be saved, please try again. Green Streets Support has been notified. We are sorry for the inconvenience.');
    }); 
  });

  // apply cached data
  $.each(cs, function(f,v) {
    var $field,
        legContainers = {
          'wtw': 'w-to-work-legs',
          'wfw': 'w-from-work-legs',
          'ntw': 'n-to-work-legs',
          'nfw': 'n-from-work-legs'
        };
    
    if (f !== 'legs') {
      $field = $('#' + f);
      if ($field.attr('type') === 'checkbox') {
        $field.prop('checked', v); 
      } else if ($('input[name=' + f + ']').attr('type') === 'radio') {
        $('input[name=' + f + '][value=' + v + ']:radio').prop('checked', true);
      } else {
        $field.val(v);
      }
    } else {
      $.each(v, function(k,l) {
        var legContainerId = legContainers[l.day + l.direction];
        addLeg(legContainerId, l);
        console.log(l);
        // FIXME: detect wtw pattern and compare
        // array.push(transport_mode+duration).reverse.join
        // combination of transport_mode+duration
        // to only toggle yes/no questions instead of showing everything
        $('#' + legContainerId).parent().show(100);
        $('input.morelegs[name=' + legContainerId + ']').prop('checked', true);
        $('input.morelegs.yes[name=' + legContainerId + ']').prop('checked', false);
      });
    }
    if (cs.home_address && cs.work_address) { 
      setCommuteGeom(cs.home_address, cs.work_address);
      setCommuteGeom2(cs.home_address, cs.work_address);
      setCommuteGeom3(cs.home_address, cs.work_address);
    }
  });

  // show extra questions lastweek section
  if ($('input[name=lastweek]:radio:checked').val() === 'n') $('#lastweekaway').show();

});
