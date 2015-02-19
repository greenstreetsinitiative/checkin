/*
 * Every last Friday of the month, the price goes up 10% until
 * the competition closes in April. This will happen on the last
 * Friday of January, February, and March.
 */

/* Returns how many days are in a month */
var days_in_month = function(year, month) {
    var is_leap = new Date(year, 1, 29).getMonth() == 1;
    if (month == 1 && is_leap) {
        return 29;
    } else {
        var days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        return days_per_month[month];
    }
};

/* Returns last Friday of the month for a given month and year */
var last_friday = function(year, month) {
    var friday = 5;
    var num_days = days_in_month(year, month);
    var first_day = new Date(year, month, 1).getDay();
    if (first_day <= friday) {
        first_friday = 1 + friday - first_day;
    } else {
        first_friday = 8 - (first_day - friday);
    }
    return first_friday + 7 * Math.floor((num_days - first_friday)/7);
};

var deadline = function(year, month) {
    var day = last_friday(year, month);
    return new Date(year, month, day).getTime();
};

/* Returns an amount to be multiplied by the original fee */
var multiplier = function() {
    var today = new Date().getTime();
    var year = new Date().getFullYear();
    var mult = 1;
    for(var month = 0; month < 3; month++) {
        if (today < deadline(year, month)) {
            break;
        }
        mult *= 1.1;
    }
    return mult;
};

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
    return multiplier() * earlyBird(size);
};

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
    $(".fee").empty();
    $(".fee").append('$'+Math.round(price)+'.00');
};

$(document).ready(function() {
    $("#business_size").change(function(){ registrationFee(); });
    $("#num_subteams").change(function(){ registrationFee(); });
    $("#subteams").change(function(){ registrationFee(); });
});
