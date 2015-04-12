from __future__ import division

from survey.models import Commutersurvey, Employer, Leg, Month, Team, Mode
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Sum,Count

def calculate_metrics(company):
    employee_engagement = {}
    employee_engagement["checkins"] = company.nr_checkins
    employee_engagement["num_participants"] = company.nr_participants

    if company.nr_employees > 0:
        employee_engagement["perc_participants"] = employee_engagement["num_participants"]*100 / company.nr_employees
    else:
        employee_engagement["perc_participants"] = ''

    # TODO: How does this update as the challenge goes? Use all challenges that have happened so far instead of 7
    # TODO count participants even if without an email or name OR make name and email required fields
    if company.nr_participants > 0:
        employee_engagement["avg_frequency"] = employee_engagement["checkins"] / (employee_engagement["num_participants"] * 7)
    else: 
        employee_engagement["avg_frequency"] = ''

    green_momentum = {}
    green_momentum["num_already_green"] = company.nr_already_green

    if company.nr_checkins > 0:
        green_momentum["perc_already_green"] = green_momentum["num_already_green"]*100 / company.nr_checkins
    else:
        green_momentum["perc_already_green"] = ''

    green_momentum["carbon_saved"] = company.overall_carbon

    behavior_change = {}

    behavior_change["calories_burned"] = company.overall_calories

    behavior_change["green_switches"] = company.nr_green_switches

    behavior_change["healthy_switches"] = company.nr_healthy_switches

    behavior_change["positive_switches"] = company.nr_positive_switches

    if company.nr_checkins > 0:
        behavior_change["perc_green"] = behavior_change["green_switches"]*100 / company.nr_checkins

        behavior_change["perc_healthy"] = behavior_change["healthy_switches"]*100 / company.nr_checkins

        behavior_change["perc_positive"] = behavior_change["positive_switches"]*100 / company.nr_checkins
    else:
        behavior_change["perc_green"] = ''
        behavior_change["perc_healthy"] = ''
        behavior_change["perc_positive"] = ''

    return {'engagement': employee_engagement, 'green': green_momentum, 'behavior': behavior_change }


def latest_leaderboard(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    d = {}

    companies = Employer.objects.only('id','name').filter(active=True).annotate(overall_carbon=Sum('commutersurvey__carbon_change'),overall_calories=Sum('commutersurvey__calorie_change'),nr_checkins=Count('commutersurvey'))

    for company in companies:
        d[str(company.name)] = calculate_metrics(company)

    ranks = {}
    # returns top 10 employers for checkins
    ranks['top_checkins'] = sorted(d.keys(), key=lambda x: d[x]['engagement']['checkins'], reverse=True)[:10]

    # returns top 10 employers for % of company participating
    ranks['top_perc_participants'] = sorted(d.keys(), key=lambda x: d[x]['engagement']['perc_participants'], reverse=True)[:10]

    # returns top 10 employers for carbon dioxide saved
    ranks['top_carbon'] = sorted(d.keys(), key=lambda x: d[x]['green']['carbon_saved'], reverse=True)[:10]

    # returns top 10 employers for calories burned
    ranks['top_calories'] = sorted(d.keys(), key=lambda x: d[x]['behavior']['calories_burned'], reverse=True)[:10]

    # returns top 10 employers for green switches
    ranks['top_green'] =sorted(d.keys(), key=lambda x: d[x]['behavior']['green_switches'], reverse=True)[:10]

    # returns top 10 employers for healthy switches
    ranks['top_healthy'] = sorted(d.keys(), key=lambda x: d[x]['behavior']['healthy_switches'], reverse=True)[:10]

    # returns top 10 employers for positive switches
    ranks['top_positive'] = sorted(d.keys(), key=lambda x: d[x]['behavior']['positive_switches'], reverse=True)[:10]


    return render_to_response('leaderboard/leaderboard_new.html', {'context_dict': d, 'ranks': ranks }, context)


