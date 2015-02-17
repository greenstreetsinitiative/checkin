import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ValidationError

from register.forms import Form
from captcha import captcha_valid
from email import registration_confirmation_email
from registration import Registration

def register_view(request):
    """
    Handles requests to /register

    If it's a post request, that means we're receiving the form data and we
    call the form_submission function to save it and return the appropriate
    page (either the registration page if an error occurs otherwise sends the
    user to the confirmation page).

    Otherwise, just returns the registration page.
    """
    if request.method == 'POST':
        return form_submission(request)
    else:
        return form_view(request, {
            'open': Registration.is_open()
        })

def form_view(request, context_dict):
    """
    Returns the rendered form for registering

    Input:
        *   request is just Django's request object
        *   context_dict is a dictionary contaning the context needed to render
            the template. It needs to contain the following keys:
                open: bool, determines if the registration period is active
    """
    template = loader.get_template('register/form.html')
    context = RequestContext(request, context_dict)
    page = template.render(context)
    return HttpResponse(page)


def form_submission(request):
    """
    Handles registration submissions.
    If there's a problem, return user to the registration page and alert them
    of any errors.
    """
    try:
        if not captcha_valid(request):
            return HttpResponse('The captcha gotcha.')
            #redirect('/')
        f = Form(request.POST)
        template = loader.get_template('register/confirmation.html')
        context = RequestContext(request, {
            'fee': f.fee,
            'subteams': f.business_has_subteams
        })
        # registration_confirmation_email(form.email())
        return HttpResponse(template.render(context))
    except ValidationError as e:
        return HttpResponse(json.dumps({
            'error': str(e),
            'post': request.POST
        }))
