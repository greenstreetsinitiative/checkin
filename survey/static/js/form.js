$(function() {
  var cs = {}, // formdata
      map, geocoder;

  // map & locations
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 11,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    center: new google.maps.LatLng(42.357778, -71.061667),
    streetViewControl: false,
    mapTypeControl: false
  });

  geocoder = new google.maps.Geocoder();

  // geocode address
  function geocodeAddress($address) {
    geocoder.geocode({address: $address.val()}, function(results, status) {
      var marker, $helptxt;
      if (status == google.maps.GeocoderStatus.OK) {
        $address.val(results[0]['formatted_address']);
        marker = new google.maps.Marker({
          map: map,
          title: results[0]['formatted_address'],
          position: results[0].geometry.location,
          animation: google.maps.Animation.DROP
        });
        cs[$address.attr('id')] = {
          name: results[0]['formatted_address'],
          position: results[0].geometry.location
        };
        map.panTo(results[0].geometry.location);
        // TODO:  if work and home location, geocode route
        //        remove existing marker
        //        show commute length
      } else {
        $helptxt = $('<span />', {
          class: 'text-danger'
        }).html('We were not able to locate this address.');
        $address.after($helptxt);
      }
    });
  }

  // trigger address geocoder
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
    var targetLegs = $(event.target).attr('name'),
        $targetLegsContainer = $('#' + targetLegs).parent();
    $targetLegsContainer.toggle(100);
  });
  
  // add another leg
  $('.btn.morelegs').on('click', function(event) {
    var targetLegs = $(event.target).data('target'),
        $targetLegs = $('#' + targetLegs),
        $lastLeg = $('.leg:last', $targetLegs),
        $removeLegBtn = $('<button class="btn btn-danger"><span class="button">X</span></button>'),
        $newLeg;

    event.preventDefault();

    $newLeg = $lastLeg
    .clone()
    .appendTo($targetLegs);

    $removeLegBtn.on('click', function(event) {
      var $leg = $(event.target).parentsUntil($targetLegs);
      event.preventDefault();
      $leg.remove();
    });

    $('div:first-child', $newLeg)
    .addClass('right')
    .html($removeLegBtn);
  });
});
