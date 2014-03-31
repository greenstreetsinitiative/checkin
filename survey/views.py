from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.forms.models import inlineformset_factory

import json

from survey.models import Commutersurvey, Employer
from survey.forms import CommuterForm


def process_request(request):
    """ 
    Sets 'REMOTE_ADDR' to 'HTTP_X_REAL_IP', if the latter is set.
    'HTTP_X_REAL_IP' is specified in Nginx config.
    """
    if 'HTTP_X_REAL_IP' in request.META:
        request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
    return request
      

def commuter(request):
    """
    Renders Commuterform or saves it in case of POST request. 
    """

    request = process_request(request)

    survey = Commutersurvey()

    employers = Employer.objects.filter(active=True)

    if request.method == 'POST':
        surveyform = CommuterForm(request.POST, instance=survey)
        survey.ip = request.META['REMOTE_ADDR']
        
        # check if user already checked in this month
        month = request.POST['month']
        email = request.POST['email']
        if Commutersurvey.objects.filter(month__iexact=month, email__iexact=email).exists():
            existing_survey = Commutersurvey.objects.filter(month__iexact=month, email__iexact=email).order_by('-created')[0]
            # addding existing id forces update
            survey.id = existing_survey.id
            survey.created = existing_survey.created

        # add new employer to GSI Employer list
        employer = request.POST['employer']
        if employer != "" and not Employer.objects.filter(name__exact=employer):
            new_employer = Employer(name=employer)
            new_employer.save()

        if surveyform.is_valid():
            surveyform.save() 
            return render_to_response('survey/thanks.html', locals(), context_instance=RequestContext(request))
        else:
            return render_to_response('survey/commuterform.html', locals(), context_instance=RequestContext(request))
    else:
        surveyform = CommuterForm(instance=survey)
        return render_to_response('survey/commuterform.html', locals(), context_instance=RequestContext(request))


def api(request):
    """
    Simple REST api for survey data
    """

    request = process_request(request)

    if request.method == 'POST':
        # TODO: process formdata
        return HttpResponse(status=200)

    return HttpResponse(status=500)

