from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.forms.models import inlineformset_factory

import json

from survey.models import Commutersurvey, Employer, Leg
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

def update_existing_survey(survey, survey_id, created, legs):
    survey.id = survey_id
    survey.created = created
    legs = Leg.objects.filter(commutersurvey=survey)
    for leg in legs:
        leg.delete()
    return survey

def api(request):
    """
    Simple REST api for survey data
    """

    request = process_request(request)

    if request.method == 'POST':
        data = request.POST.dict()
        # look for survey legs
        try:
            legs = json.loads(data['legs'])
            del data['legs']
        except KeyError:
            legs = []
        
        survey = Commutersurvey(**data)
        
        # check for existing survey
        try:
            existing_survey = Commutersurvey.objects.get(month=data['month'], email=data['email'])
            update_existing_survey(survey, existing_survey.id, existing_survey.created, legs)
        except ObjectDoesNotExist:
            pass
        except MultipleObjectsReturned:
            # cleanup, keep the most recent one and delete the rest
            surveys = Commutersurvey.objects.filter(month=data['month'], email=data['email']).order_by('-created')
            for s in surveys[1:]:
                s.delete()
            update_existing_survey(survey, surveys[0].id, surveys[0].created, legs)

        survey.save_with_legs(legs=legs)
        return HttpResponse(status=200)

    return HttpResponse(status=500)

