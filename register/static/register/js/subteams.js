/*
 * Returns string containing html for the ith subteam input
 */
/*var subteamHTML = function(i) {
    return "<div class=\"form-group\"><label class=\"form-label subteam_label\">Subteam {i}</label><div class=\"form-inline\"><label for=\"subteam_name_{i}\">Name</label><input type=\"text\" class=\"form-control\" id=\"subteam_name_{i}\" name=\"subteam_name_{i}\" class=\"subteam_name\" placeholder=\"Enter subteam name\"><label for=\"subteam_size_{i}\">Size</label><input type=\"number\" class=\"form-control\" id=\"subteam_size_{i}\" class=\"subteam_size\" name=\"subteam_size_{i}\" placeholder=\"Enter subteam name\"></div></div>".replace(/\{i\}/g, i);
};*/


var subteamHTML = function(i) {
    return "<div id=\"subteam_{i}\"><div class=\"form-group\"><label class=\"form-label\" for=\"subteam_name_{i}\">Subteam {i+} Name</label><input type=\"text\" class=\"form-control\" id=\"subteam_name_{i}\" name=\"subteam_name_{i}\" placeholder=\"Enter subteam name\"></div><div class=\"form-group\"><label class=\"form-label\" for=\"subteam_size_{i}\">Subteam {i+} Size</label><input type=\"number\" class=\"form-control\" id=\"subteam_size_{i}\"  name=\"subteam_size_{i}\" placeholder=\"Enter subteam name\"></div></div>".replace(/\{i\+\}/g, i+1).replace(/\{i\}/g, i);
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
 * Since companies can have variable number of subteams, this has to be
 * handled dynamically
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
