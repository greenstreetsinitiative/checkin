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

  directionsDisplay.setMap(map);

  // geocode address
  function geocodeAddress($address) {
    geocoder.geocode({address: $address.val()}, function(results, status) {
      var marker, $helptxt, 
          id = $address.attr('id');

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
          getCommuteRoute();
        } else {
          map.panTo(results[0].geometry.location);
        }
      } else {
        $helptxt = $('<span />', {
          class: 'text-danger'
        }).html('We were not able to locate this address.');
        $address.after($helptxt);
      }
    });
  }

  function getCommuteRoute() {
    directionsService.route({
      origin: cs.home_address.position,
      destination: cs.work_address.position,
      travelMode: google.maps.TravelMode.DRIVING
    }, function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        directionsDisplay.setDirections(response);
        $('#commute-distance').text(response.routes[0].legs[0].distance.text + ' (approx. if driving)');
        // TODO: parse response.routes[0].overview_path to polyline
      }
    });
  }

  // trigger address geocoder on several UI interactions
  $('.btn.locate-address').on('click', function(event) {
    event.preventDefault();
    var $address = $(this).parent().prev().find('input.address');
    
    geocodeAddress($address);
  });
  $('input.address').on({
    focusout: function() {
      geocodeAddress($(this));
    },
    keyup: function(event) {
      if (event.which === 13) geocodeAddress($(this));
    }
  });
  
  //Calls the selectBoxIt method on your HTML select box. Just makes dropdowns nicer.
  // FIXME: interferes with dropdown in added multiple legs
  $('select').selectBoxIt();

  // toggle more legs options
  $('input.morelegs[type=radio').on('change', function(event) {
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
});
