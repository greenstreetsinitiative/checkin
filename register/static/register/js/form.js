/* Form validation
 *
 * Overall, the validation isn't particularly thorough, especially since a lot
 * of the fields can't be validated easily (like names, or the open ended
 * questions at the bottom of the form).
 *
 * A good part of the validation is just checking to see if certain entries
 * aren't too long or if inputs that should be numbers are numbers.
 *
 * Properly validating things like emails, urls, and telephones is tricky as
 * well, but the validation done should handle most cases.
 */

/*
 * Checks if the length of some string n is less than or equal to some
 * integer n.
 */
var str_length_lte = function(s, n) {
    return s.length <= n ? true : false;
};

var str_length_gte = function(s, n) {
    return s.length >= n ? true : false;
};

var str_length_range = function(s, lower_bound, upper_bound) {
    return str_length_lte(s, upper_bound) && str_length_gte(s, lower_bound);
};

var is_positive_number = function(n) {
    if (isNaN(n)) {
        return false;
    } else {
        return parseInt(n) > 0 ? true : false;
    }
};

var exists = function(s) {
    return str_length_gte(s, 0);
};

/*
 * Validates a URL
 * Not full URL specifications, but should deal with most cases.
 * Regex adapted from Django's is_valid_url function, except localhost isn't
 * an option.
 * Breaking it down:
 * Begin string:
 *      ^
 * Protocol:
 *      (https?:\/\/)?
 * Looking for http://, https:// or nothing
 * IP:
 *      ((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
 * Domain:
 *      ((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?))
 * The regex looks for either an IP address or a domain
 *      (ip)|(domain)
 * Port:
 *      (?::\d+)?
 * The port is just a colon followed by numbers and is optional
 * Extension (everything that comes after the domain/ip/port)
 *      (?:\/?|[/?]\S+)?
 * Optional and accepts pretty much anything that isn't a space
 * Finally, end url:
 *      $
 */
var validate_url = function(url) {
    var url_regex =  /^(https?:\/\/)?((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?))(?::\d+)?(?:\/?|[/?]\S+)?$/i;
    return url.match(url_regex) ? true : false;
};

var business = {
    // Business name is limited to 200 characters
    name: function(name) {
        return str_length_lte(name, 200);
    },
    address: function(address) {
        return exists(address);
    },
    // Business size must be a positive number
    size: function(size) {
        return is_positive_number(size);
    },
    website: function(url) {
        if (url === ''){
            return true;
        } else {
            return validate_url(url);
        }
    },
    // Validates subteam information
    subteams: function() {
        return true;
    }
};

var contact = {
    // Just checks that name and title are under 200 characters each
    name: function(name) {
        return str_length_lte(name, 200);
    },
    title: function(title){
        return str_length_lte(title, 200);
    },
    // 15 digits is the longest that a telephone number can be
    // Strip out any non-numeric character since we don't really know how
    // someone is going to try and format their phone number
    phone: function(phone) {
        // Strip out non numbers
        phone_number = phone.replace(/\D/g, '');
        return str_length_range(phone_number, 7, 15);
    },
    // Just checks that email is something@something.something
    email: function(email) {
        return email.match(/\S+@\S+\.\S+/) ? true : false;
    }
};

/*
 * Listen to changes on input with `id` and validate the value
 * of that input using the validator function
 */
var validate_input = function(id, validator) {
    var form_input = $(id);
    var last_value = '';
    form_input.bind('input', function() {
        var value = form_input.val();
        if (validator(value)) {
            form_input.parent().removeClass('has-error');
        } else {
            form_input.parent().addClass('has-error');
        }
    });
};

var validate_all = function(arr) {
    for (var i in arr) {
        var v = arr[i];
        validate_input(v[0], v[1]);
    }
};

var validate = {
    business: function() {
        validate_all([
            ['#business_name', business.name],
            ['#business_address', business.address],
            ['#business_size', business.size],
            ['#business_website', business.website]
        ]);
    },
    subteams: function() {
        $('#num_subteams').change(function(){
            console.log($('#num_subteams').val());
            for(var i=0; i < $('#num_subteams').val(); i++) {
                validate_all([
                    ['#subteam_name_'+i, business.name],
                    ['#subteam_size_'+i, business.size]
                ]);
            }
        });
    },
    contact: function() {
        validate_all([
            ['#contact_name', contact.name],
            ['#contact_title', contact.title],
            ['#contact_phone', contact.phone],
            ['#contact_email', contact.email]
        ]);
    }
};

$(document).ready(function() {
    validate.business();
    validate.subteams();
    validate.contact();
});
