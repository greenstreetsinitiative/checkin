/*
 * Returns string containing html for the ith subteam input
 */
/*var subteamHTML = function(i) {
    return "<div class=\"form-group\"><label for=\"subteam_"+i+"\">Subteam "+(i+1)+"</label><input type=\"text\" class=\"form-control\" id=\"subteam_"+i+"\" name=\"subteam_"+i+"\" placeholder=\"Enter subteam name\"></div>";
};*/

var subteamHTML = function(i) {
    return "<div class=\"form-group\"><span class=\"form-label\">Subteam __i__</span><div class=\"form-inline\"><label for=\"subteam_name___i__\">Name</label><input type=\"text\" class=\"form-control\" id=\"subteam_name___i__\" name=\"subteam___i__\" placeholder=\"Enter subteam name\"><label for=\"subteam_size___i__\">Size</label><input type=\"number\" class=\"form-control\" id=\"subteam_size___i__\" name=\"subteam___i__\" placeholder=\"Enter subteam name\"></div></div>".replace(/__i__/g, i);
};


/*
 * Given a number of subteams, returns the html for that many subteam
 * inputs
 */
var subteamInputHTML = function(n) {
    var html = "";
    for(var i = 0; i < n; i++) {
        html += subteamHTML(i);
    }
    return html;
};

/*
 * Display inputs for how many subteams the company has
 */
var showSubteamInputs = function() {
    $("#num_subteams").change(function() {
        num_subteams = $("#num_subteams").val();
        html = subteamInputHTML(num_subteams);
        $("#subteam_list").empty();
        $("#subteam_list").append(html);
    });
};

/*
 * Listens for changes in the subteams checkbox.
 * If selected, show the input box for number of subteams
 * Otherwise hide it
 */
var showNumSubteam = function() {
    $('#subteams').change(function() {
        if($('#subteams:checked').length === 1) {
            // show it
            $("#subteam_num_group").removeClass('hidden');
        } else {
            $("#subteam_num_group").addClass('hidden');
        }
    });
};

$(document).ready(function() {
    showNumSubteam();
    showSubteamInputs();
});
