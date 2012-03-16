from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.utils import simplejson
from django.contrib.gis.geos import fromstr
from django.conf import settings

from datetime import date, timedelta

from django.forms.models import inlineformset_factory

from survey.models import School, Studentsurvey, Child, Schooldistrict, Street, Town, Commutersurvey, Employer, EmployerGSI, Walkrideday, Teachersurvey, Studentgroup
from survey.forms import StudentForm, ChildForm, CommuterForm, TeacherForm, StudentgroupForm


def process_request(request):
    """ 
    Sets 'REMOTE_ADDR' based on 'HTTP_X_FORWARDED_FOR', if the latter is set.
    Based on http://djangosnippets.org/snippets/1706/
    """
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
        request.META['REMOTE_ADDR'] = ip
    return request

def get_active_wrday():
    """
    Returns the Walk/Ride day object if today is within a valid range;
    time window is 10 days from Monday -> Walk/Ride Day -> Wednesday.
    """

    # expand time window for development
    if settings.DEBUG == True:
        timewindow = 5, 365
    else:
        timewindow = 5, 4

    today = date.today()
    start_date = today - timedelta(days=timewindow[0])
    end_date = today + timedelta(days=timewindow[1])

    # check if today is within a custom W/R day time window
    wrdays = Walkrideday.objects.filter(
        Q(end_date__gte=today),
        Q(start_date__lte=today)
    ).order_by('date')

    # if not, check if today is within a default W/R day time window
    if wrdays.exists() == False:
        wrdays = Walkrideday.objects.filter(date__range=(start_date, end_date)).order_by('date')

    return wrdays[0] if wrdays.exists() else False


def index(request):

    wrday = get_active_wrday()

    # find next Walk/Ride Day
    if wrday == False:
        wrday_next = Walkrideday.objects.filter(date__gt=date.today()).order_by('date')[0]
    
    return render_to_response('survey/index.html', locals(), context_instance=RequestContext(request))
    
def district(request, district_slug):
    
    district = Schooldistrict.objects.get(slug__iexact=district_slug)
    
    return render_to_response('survey/district.html', {
            'district': district,
            'MEDIA_URL': settings.MEDIA_URL,
            },
            context_instance=RequestContext(request))

def get_employer_list(employers):
    """
    Translates a given employer query object to a list containing employer objects with selected properties.
    """
    employer_list =[]
    
    for employer in employers:
        employer_name = "%s, %s" % (employer.name, employer.address)
        employer_location = "%f %f" % (employer.geometry.y, employer.geometry.x)
        employer_detail = dict(name = employer_name, latlon = employer_location, infousa_id = employer.infousa_id, )
        employer_list.append(employer_detail)

    return employer_list

def get_employers(request):
    """
    Accepts lat, lon and radius parameters and returns a JSON object of max. 500 found employers.
    """

    location = fromstr('POINT(%s %s)' % (request.GET['lng'], request.GET['lat']), srid=4326)

    radius = float(request.GET['radius'])

    # search for employers within radius and order by distance, limit to 500
    employers = Employer.objects.transform(4326).filter(geometry__distance_lte=(location, radius)).distance(location).order_by('distance')[:500]

    employer_list = get_employer_list(employers)
    
    return HttpResponse(simplejson.dumps(employer_list), mimetype='application/json')

def get_town_employers(request, slug):
    """
    Returns all employers and their location for a given town
    """
    
    town = get_object_or_404(Town.objects, slug=slug)
    employers = Employer.objects.transform(4326).filter(town=town)[:500]
     
    employer_list = get_employer_list(employers)
    
    return HttpResponse(simplejson.dumps(employer_list), mimetype='application/json')

def get_schools(request, slug):
    """
    Returns all schools for given district as JSON
    """
    
    # check if district exists
    district = get_object_or_404(Schooldistrict.objects, slug=slug)
    
    schools = School.objects.filter(districtid=district).order_by('name')
    
    # build response data
    response = []
    for school in schools:
        response.append(dict(name=school.name, id=school.id))

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')   
    
    
def get_streets(request, slug, regional_unit):
    """
    Returns all streets for given regional unit
    """
    
    # check for streets in regional unit
    if regional_unit == "town":
        town = get_object_or_404(Town.objects, slug=slug)
        streets = Street.objects.filter(town=town)
    elif regional_unit == "schooldistrict":
        schooldistrict = get_object_or_404(Schooldistrict.objects, slug=slug)
        streets = Street.objects.filter(schooldistrict=schooldistrict)
    
    street_list =[]
    
    for street in streets:
        street_list.append(street.name)
    
    return HttpResponse(simplejson.dumps(street_list), mimetype='application/json')


def student(request):
    """
    Renders Studentform or saves it and related Childforms in case of POST request. 
    """

    request = process_request(request)

    # get all districts with participating schools
    districts = Schooldistrict.objects.filter(school__survey_active=True).distinct()

    survey = Studentsurvey()
       
    SurveyFormset = inlineformset_factory(Studentsurvey, Child, form=ChildForm, extra=1, can_delete=False)
    
    if request.method == 'POST':
        surveyform = StudentForm(request.POST, instance=survey)
        surveyformset = SurveyFormset(request.POST, instance=survey)
        survey.walkrideday = Walkrideday.objects.filter(active=True).order_by('-date')[0]
        survey.ip = request.META['REMOTE_ADDR']

        if surveyformset.is_valid() and surveyform.is_valid():
            surveyform.save()
            surveyformset.save()
            
            return render_to_response('survey/thanks.html', locals(), context_instance=RequestContext(request))
            
        else:
            towns = Town.objects.filter(survey_active=True)
            return render_to_response('survey/studentform.html', locals(), context_instance=RequestContext(request))
    else:
        towns = Town.objects.filter(survey_active=True)
        
        surveyform = StudentForm(instance=survey)
        surveyformset = SurveyFormset(instance=survey)

        return render_to_response('survey/studentform.html', locals(), context_instance=RequestContext(request))


def commuter(request):
    """
    Renders Commuterform or saves it in case of POST request. 
    """

    wrday = get_active_wrday()

    # no Walk/Ride Day
    if wrday == False:
        return redirect('/')

    request = process_request(request)

    commutersurvey = Commutersurvey()

    employers = EmployerGSI.objects.filter(active=True)

    if request.method == 'POST':
        commuterform = CommuterForm(request.POST, instance=commutersurvey)
        commutersurvey.ip = request.META['REMOTE_ADDR']
        commutersurvey.walkrideday = wrday

        # add new employer to GSI Employer list
        employer = request.POST['other_employer']
        if employer != "" and not EmployerGSI.objects.filter(name__exact=employer):
            new_employer = EmployerGSI(name=employer)
            new_employer.save()

        if commuterform.is_valid():
            commuterform.save()
            return render_to_response('survey/thanks.html', locals(), context_instance=RequestContext(request))
        else:
            towns = Town.objects.filter(survey_active=True)
            return render_to_response('survey/commuterform.html', locals(), context_instance=RequestContext(request))
    else:
        commuterform = CommuterForm(instance=commutersurvey)
        towns = Town.objects.filter(survey_active=True)
        return render_to_response('survey/commuterform.html', locals(), context_instance=RequestContext(request))


def teacher(request):
    """ 
    Renders Teacherform or saves it if POST
    """

    request = process_request(request)

    # get all school districts with participating schools
    districts = Schooldistrict.objects.filter(school__survey_active=True).distinct()

    survey = Teachersurvey()

    SurveyFormset = inlineformset_factory(Teachersurvey, Studentgroup, form=StudentgroupForm, extra=1, can_delete=False)

    if request.method == 'POST':
        surveyform = TeacherForm(request.POST, instance=survey)
        surveyformset = SurveyFormset(request.POST, instance=survey)
        survey.ip = request.META['REMOTE_ADDR']

        if surveyformset.is_valid() and surveyform.is_valid():
            surveyform.save()
            surveyformset.save()
            
            return render_to_response('survey/thanks.html', locals(), context_instance=RequestContext(request))
            
        else:
            return render_to_response('survey/teacherform.html', locals(), context_instance=RequestContext(request))
    else:
        surveyform = TeacherForm(instance=survey)
        surveyformset = SurveyFormset(instance=survey)

    return render_to_response('survey/teacherform.html', locals(), context_instance=RequestContext(request))


