$(function() {
  
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
