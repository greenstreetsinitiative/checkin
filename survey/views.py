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

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory
from django.forms.models import modelform_factory


from survey.forms import MakeLegs_NormalTW, MakeLegs_NormalFW, MakeLegs_WRTW, MakeLegs_WRFW

def add_checkin(request):

    request = process_request(request)

    try:
        wr_day = Month.objects.get(open_checkin__lte=date.today(), close_checkin__gte=date.today())
    except Month.DoesNotExist:
        return redirect('/')
        
    commute_form = CommuterForm()

    leg_formset_NormalTW = MakeLegs_NormalTW(instance=Commutersurvey(), prefix='ntw')
    leg_formset_NormalFW = MakeLegs_NormalFW(instance=Commutersurvey(), prefix='nfw')
    leg_formset_WRTW = MakeLegs_WRTW(instance=Commutersurvey(), prefix='wtw')
    leg_formset_WRFW = MakeLegs_WRFW(instance=Commutersurvey(), prefix='wfw')

    if request.POST:
        commute_form = CommuterForm(request.POST)

        if commute_form.is_valid():
            commutersurvey = commute_form.save(commit=False)
            leg_formset_NormalTW = MakeLegs_NormalTW(request.POST, instance=commutersurvey, prefix='ntw')
            leg_formset_NormalFW = MakeLegs_NormalFW(request.POST, instance=commutersurvey, prefix='nfw')
            leg_formset_WRTW = MakeLegs_WRTW(request.POST, instance=commutersurvey, prefix='wtw')
            leg_formset_WRFW = MakeLegs_WRFW(request.POST, instance=commutersurvey, prefix='wfw')

            if leg_formset_NormalTW.is_valid() and leg_formset_NormalFW.is_valid() and leg_formset_WRTW.is_valid() and leg_formset_WRFW.is_valid():
                commutersurvey.wr_day_month = wr_day
                commutersurvey.email = commute_form.cleaned_data['email']
                commutersurvey.employer = commute_form.cleaned_data['employer']
                commutersurvey.team = commute_form.cleaned_data['team']
                commutersurvey.save()

                leg_formset_NormalTW.save()
                leg_formset_NormalFW.save()
                leg_formset_WRTW.save()
                leg_formset_WRFW.save()

                return HttpResponseRedirect('complete/')

        leg_formset_NormalTW = MakeLegs_NormalTW(request.POST, prefix='ntw')
        leg_formset_NormalFW = MakeLegs_NormalFW(request.POST, prefix='nfw')
        leg_formset_WRTW = MakeLegs_WRTW(request.POST, prefix='wtw')
        leg_formset_WRFW = MakeLegs_WRFW(request.POST, prefix='wfw')

    return render(request, "survey/new_checkin.html", { 'wr_day': wr_day, 'form': commute_form, 'NormalTW_formset': leg_formset_NormalTW, 'NormalFW_formset': leg_formset_NormalFW, 'WRTW_formset': leg_formset_WRTW, 'WRFW_formset': leg_formset_WRFW })

def process_request(request):
    """ 
    Sets 'REMOTE_ADDR' to 'HTTP_X_REAL_IP', if the latter is set.
    'HTTP_X_REAL_IP' is specified in Nginx config.
    """
    if 'HTTP_X_REAL_IP' in request.META:
        request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
    return request
      

# def commuter(request):
#     """
#     Renders Commuterform or saves it in case of POST request. 
#     """

#     request = process_request(request)

#     try:
#         wr_day = Month.objects.get(open_checkin__lte=date.today(), close_checkin__gte=date.today())
#     except Month.DoesNotExist:
#         return redirect('/')

#     survey = Commutersurvey()
#     employers = Employer.objects.filter(active=True, is_parent=False)

#     return render_to_response('survey/commuterform.html', locals(), context_instance=RequestContext(request))

def update_existing_survey(survey, survey_id, created):
    survey.id = survey_id
    survey.created = created
    Leg.objects.filter(commutersurvey=survey).delete()
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

        try:
            data['employer'] = Employer.objects.get(pk=data['employer'])
        except Employer.DoesNotExist:
            return HttpResponse('No such Employer.', status=500)

        survey = Commutersurvey(**data)
        
        # check for existing survey
        try:
            existing_survey = Commutersurvey.objects.get(wr_day_month=data['wr_day_month'], email=data['email'])
            update_existing_survey(survey, existing_survey.id, existing_survey.created)
        except ObjectDoesNotExist:
            pass
        except MultipleObjectsReturned:
            # cleanup, keep the most recent one and delete the rest
            surveys = Commutersurvey.objects.filter(wr_day_month=data['wr_day_month'], email=data['email']).order_by('-created')
            for s in surveys[1:]:
                s.delete()
            update_existing_survey(survey, surveys[0].id, surveys[0].created)

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
            # email error details to Trello
            # FIXME: this could be done with the Trello API
            template_content = [{
                'content': request.META.get('HTTP_USER_AGENT'), 
                'name': 'browser'
            }, {
                'content': json.dumps(request.POST), 
                'name': 'form_data'
            }]
            message = {
                'from_email': 'checkin@gogreenstreets.org',
                'from_name': 'Checkin',
                'metadata': {'website': 'checkin.gogreenstreets.org'},
                'subject': 'Checkin Error for %s' % request.POST['email'],
                'to': [{
                    'email': 'cspanring+qkkzwxbq8tvfsfyfk8wz@boards.trello.com', 
                    'name': 'Checkin', 
                    'type': 'to'
                }]
            }
            send_email('checkin-error', template_content, message)
            return HttpResponse('Somehting went wrong.', status=500)

    return HttpResponse(status=403)

