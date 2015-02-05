/*
 * earlyBird
 * Given a company's size as a number, return the fee for that size category
 */
var earlyBird = function(size) {
    if (size > 5000) {
        return 950;
    } else if (size > 3000) {
        return 850;
    } else if (size > 1000) {
        return 800;
    } else if (size > 500) {
        return 650;
    } else if (size > 100) {
        return 550;
    } else if (size > 50) {
        return 450;
    } else if (size > 15) {
        return 250;
    } else if (size > 0) {
        return 150;
    } else {
        return 0;
    }
};

var sizeFee = function() {
    var size = $("#business_size").val();
    if(isNaN(size) || size < 0) {
        size = 0;
    }
    return earlyBird(size);
};

//
var subteamFee = function() {
    if ($("#subteams:checked").length === 0) {
        return 0;
    } else {
        var subteams = $("#num_subteams").val();
        if (isNaN(subteams) || subteams < 0) {
            subteams = 0;
        }
        return 50 * subteams;
    }
};

var registrationFee = function() {
    var price = sizeFee() + subteamFee();
    // How to deal with ceo_discount?
    //var ceo_discount = $('#ceo_discount:checked').length;
    $(".fee").empty();
    $(".fee").append('$'+price+'.00');
};

$(document).ready(function() {
    $("#business_size").change(function(){ registrationFee(); });
    $("#num_subteams").change(function(){ registrationFee(); });
    $("#subteams").change(function(){ registrationFee(); });
});
