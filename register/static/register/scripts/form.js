/* Form validation and submission */

var validate = {
    name: /[0-9]|[~!@#$%\^&*()_|+=?;:",.<>\{\}\[\]\\\/]+/g,
    telephone: /(?:\()?\d{3}(?:-|\s|\.|\)\s|\))?\d{3}(?:-|\.|\s)?\d{4}/g,
    email: /\S+@\S+\.\S+/,
};


/*
 * Obtains all data from the form
 */
var obtainForm = function() {
    var subteam = {};
    var has_subteams = $("#subteams:checked").length === 1 ? true : false;
    if(has_subteams) {
        subteam.has_subteams = true;
        subteam.count = $("#num_subteams").val();
        subteams = [];
        for(var i = 0; i < subteam.count; i++) {
            subteams.push({
                name: $("#subteam_name_"+i).val(),
                size: $("#subteam_size_"+i).val()
            });
        }
        subteam.subteams = subteams;
    } else {
        subteam.has_subteams = false;
        subteam.count = 0;
        subteam.subteams = [];
    }

    return {
        business: {
            name: $("#business_name").val(),
            address: $("#business_address").val(),
            website: $("#business_website").val(),
            size: $("#business_size").val(),
            subteams: subteam
        },
        contact: {
            name: $("#contact_name").val(),
            title: $("#contact_title").val(),
            phone: $("#contact_phone").val(),
            email: $("#contact_email").val()
        },
        questions: {
            heard_about: $("#wr_hear").val(),
            goals: $("#wr_goals").val(),
            sponsor: $("#wr_sponsor").val()
        }
    };
};


var validateForm = function(form) {
    validate.telephone.test(form.contact.phone);
    return true;
};


/*
 *  Submits form
 */
var submit = function() {
    var form_data = obtainForm();
    console.log(form_data);

    if(validateForm(form_data)) {
        // Deal with csrf
        var csrftoken = $.cookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $.post('submit', {form: JSON.stringify(form_data)}, function(data) {
            console.log('Que?');
            // window.location.replace("");
            // If data is bad, alert user of potential problems
        })
        .fail(function() {
            console.log( "There was a problem submitting your form." );
        });
    }
};
