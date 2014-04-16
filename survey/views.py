from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.forms.models import inlineformset_factory

from survey.models import Commutersurvey, Employer, Leg, Month
from survey.forms import CommuterForm

import json
import mandrill
from datetime import date


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

    try:
        wr_day = Month.objects.get(open_checkin__lte=date.today(), close_checkin__gte=date.today())
    except Month.DoesNotExist:
        return redirect('/')

    survey = Commutersurvey()
    employers = Employer.objects.filter(active=True)

    return render_to_response('survey/commuterform.html', locals(), context_instance=RequestContext(request))

def update_existing_survey(survey, survey_id, created, legs):
    survey.id = survey_id
    survey.created = created
    legs = Leg.objects.filter(commutersurvey=survey)
    for leg in legs:
        leg.delete()
    return survey

def send_email(template, template_content, message):
    try:
        mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)
        mandrill_client.messages.send_template(template_name=template, template_content=template_content, message=message)
    except mandrill.Error, e:
        pass

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
        
        try:
            data['wr_day_month'] = Month.objects.get(pk=data['wr_day_month'])
        except Month.DoesNotExist:
            return HttpResponse('No such Walk/Ride Day.', status=500)

        survey = Commutersurvey(**data)
        
        # check for existing survey
        try:
            existing_survey = Commutersurvey.objects.get(wr_day_month=data['wr_day_month'], email=data['email'])
            update_existing_survey(survey, existing_survey.id, existing_survey.created, legs)
        except ObjectDoesNotExist:
            pass
        except MultipleObjectsReturned:
            # cleanup, keep the most recent one and delete the rest
            surveys = Commutersurvey.objects.filter(wr_day_month=data['wr_day_month'], email=data['email']).order_by('-created')
            for s in surveys[1:]:
                s.delete()
            update_existing_survey(survey, surveys[0].id, surveys[0].created, legs)

        try:
            survey.save_with_legs(legs=legs)
            
            try:
                next_wr_day = 'Remember to check-in for next month\'s Walk/Ride Day on %s.' % Month.objects.active_months().filter(wr_day__gt=survey.wr_day_month.wr_day).reverse()[0].wr_day_humanized
            except IndexError:
                next_wr_day = 'Remember to check-in again next season.'
            
            template_content = [{
                'content': survey.name or survey.email, 
                'name': 'salutation'
            }, {
                'content': survey.wr_day_month.month,
                'name': 'current_wr_day'
            }, {
                'content': next_wr_day,
                'name': 'next_wr_day'
            }]
            message = {
                'from_email': 'checkin@gogreenstreets.org',
                'from_name': 'Green Streets Initiative',
                'metadata': {'website': 'checkin.gogreenstreets.org'},
                'subject': 'Walk/Ride Day %s Checkin' % survey.wr_day_month.month,
                'to': [
                    {'email': survey.email, 
                    'name': survey.name or survey.email, 
                    'type': 'to'}
                ],
                'track_opens': True
            }
            send_email('checkin-confirmation', template_content, message)
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)

    return HttpResponse(status=403)

