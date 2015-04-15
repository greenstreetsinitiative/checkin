$(function() {
  //activate chosen plugin
  $("#id_employer, #id_team").chosen({
    width: "99%"
  });

  var geocoder = new google.maps.Geocoder();

  function geocodeAddress($address) {
    geocoder.geocode({address: $address.val()}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        $address.val(results[0]['formatted_address']);
      }
    });
  }

  // trigger address geocoder on several UI interactions
  $('#id_home_address, #id_work_address').on('keyup', function(event) {
    if (event.which === 13) geocodeAddress($(this));
  });
  $('#id_home_address, #id_work_address').on('blur', function(event) {
    geocodeAddress($(this));
  });

});