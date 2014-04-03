$(function() {
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

  // read cache
  cs = simpleStorage.get('commutersurvey') || {};

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
        } else {
          map.panTo(results[0].geometry.location);
        }

      } else {
        $helptxt = $('<span />', {
          class: 'text-danger'
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

  function toggleCommuteDistance(text) {
    if (text !== '') {
      $('#commute-distance').text(text);
      $('#commute-distance').css('background', '#FFEECC');
    } else {
      $('#commute-distance').text('');
      $('#commute-distance').css('background', '#fff');
    }
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
    addLeg($(this).data('target'));
  });

  function addLeg(group, legData) {
    var $container = ('#' + group),
        $lastLeg = $('.leg:last', $container),
        $removeLegBtn = $('<button class="btn btn-danger"><span class="button">X</span></button>'),
        $newLeg;

    $newLeg = $lastLeg
    .clone()
    .appendTo($container);

    if (legData) {
      $.each(legData, function(k,v) {
        $('[name=' + k +']', $newLeg).val(v);
      });
    }

    $removeLegBtn.on('click', function(event) {
      event.preventDefault();
      var $leg = $(this).parentsUntil($container);
      $leg.remove();
    });
    $('div:first-child', $newLeg)
    .addClass('right')
    .html($removeLegBtn);
  }

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
    weight = parseInt($('#weight_cal').val());
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
    var fields = ['month', 'share', 'name', 'email', 'employer', 'home_address', 'work_address', 'comments', 'health', 'weight', 'height', 'gender', 'gender_other', 'cdays', 'caltdays', 'cpdays', 'tdays', 'bdays', 'rdays', 'wdays', 'odays', 'tcdays', 'lastweek', 'cdaysaway', 'caltdaysaway', 'cpdaysaway', 'tdaysaway', 'bdaysaway', 'rdaysaway', 'wdaysaway', 'odaysaway', 'tcdaysaway', 'outsidechanges', 'affectedyou', 'contact', 'volunteer'],
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
    $errorMsg = $('<span />', {
      class: 'text-danger validation-error'
    }).html(text);
    $element.after($errorMsg);
  }

  function validate(surveyData) {
    var emailRe = /^([a-zA-Z0-9_\.\-\+\'])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/,
        minLegs,
        isValid = true;

    // clear previous errors
    $('.validation-error').remove();
    // email
    if (!emailRe.test(surveyData.email)) {
      addErrorMsg($('#email'), 'Error: Please provide a valid email-address.');
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
    var noCacheKeys = ['home_location', 'work_location', 'geom'],
        cacheData = $.extend(true, {}, data);
    
    $.each(noCacheKeys, function(i,v) {
      if (cacheData[v]) delete cacheData[v];
    });
    return simpleStorage.set('commutersurvey', cacheData);
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

    // persist
    surveyData['csrfmiddlewaretoken'] = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
      type: 'POST',
      url: '/api/survey/',
      data: surveyData
    }).done(function() {
      window.location.href = '/commuterform/complete/';
    }).fail(function() {
      alert('An error occured and your checkin could not be saved. Please try again or contact info@GoGreenStreets.org.');
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
        // FIXME: detect wtw pattern and compare
        // array.push(mode+time).reverse.join
        // combination of mode+time
        // to only toggle yes/no questions instead of showing everything
        $('#' + legContainerId).parent().show(100);
        $('input.morelegs[name=' + legContainerId + ']').prop('checked', true);
        $('input.morelegs.yes[name=' + legContainerId + ']').prop('checked', false);
      });
    }
    if (cs.home_address && cs.work_address) setCommuteGeom(cs.home_address, cs.work_address);
  });

  // show extra questions lastweek section
  if ($('input[name=lastweek]:radio:checked').val() === 'n') $('#lastweekaway').show();

});
