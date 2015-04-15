from __future__ import division

from survey.models import Commutersurvey, Employer, Leg, Month, Team, Mode
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.db.models import Sum,Count
from django.db.models import Q
from aggregate_if import Count, Sum
from datetime import date, datetime
import datetime


def calculate_metrics(company):

    #### TODO: Cap the percentages at 100.

    employee_engagement = {}
    employee_engagement["checkins"] = company.num_checkins
    employee_engagement["num_participants"] = company.num_participants

    if company.nr_employees > 0:
        employee_engagement["perc_participants"] = employee_engagement["num_participants"]*100 / company.nr_employees
    else:
        employee_engagement["perc_participants"] = 0

    # TODO: How does this update as the challenge goes? Use all challenges that have happened so far instead of 7
    # TODO count participants even if without an email or name OR make name and email required fields
    if company.num_participants > 0:
        employee_engagement["avg_frequency"] = employee_engagement["checkins"] / (employee_engagement["num_participants"] * 7)
    else: 
        employee_engagement["avg_frequency"] = 0

    green_momentum = {}
    green_momentum["num_already_green"] = company.num_already_green

    if company.num_checkins > 0:
        green_momentum["perc_already_green"] = green_momentum["num_already_green"]*100 / company.num_checkins
    else:
        green_momentum["perc_already_green"] = 0

    # green_momentum["carbon_saved"] = company.overall_carbon
    green_momentum["carbon_saved"] = company.saved_carbon

    behavior_change = {}

    behavior_change["calories_burned"] = company.overall_calories

    behavior_change["green_switches"] = company.num_switch_green

    behavior_change["healthy_switches"] = company.num_switch_healthy

    if company.num_checkins > 0:
        behavior_change["perc_green"] = behavior_change["green_switches"]*100 / company.num_checkins

        behavior_change["perc_healthy"] = behavior_change["healthy_switches"]*100 / company.num_checkins

    else:
        behavior_change["perc_green"] = 0
        behavior_change["perc_healthy"] = 0

    return {'engagement': employee_engagement, 'green': green_momentum, 'behavior': behavior_change }


def latest_leaderboard(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    d = {}

    ### TODO - filter related commutersurveys by MONTH

    companies = Employer.objects.only('id','name').filter(
        active2015=False, 
        commutersurvey__created__gte=datetime.date(2015, 04, 15), 
        commutersurvey__created__lte=datetime.date(2015, 11, 01)).annotate(
        overall_carbon=Sum('commutersurvey__carbon_change'),
        saved_carbon=Sum('commutersurvey__carbon_savings'),
        overall_calories=Sum('commutersurvey__calorie_change'),
        num_checkins=Count('commutersurvey'),
        num_participants=Count('commutersurvey__email', distinct=True),
        num_already_green=Count('commutersurvey', only=Q(commutersurvey__already_green=True)),
        num_switch_green=Count('commutersurvey', only=Q(commutersurvey__change_type='g')),
        num_switch_healthy=Count('commutersurvey', only=Q(commutersurvey__change_type='h'))
    )

    totals = companies.aggregate(
        total_carbon=Sum('overall_carbon'),
        total_calories=Sum('overall_calories'),
        total_checkins=Sum('num_checkins')
    )

    for company in companies:
        d[str(company.name)] = calculate_metrics(company)

    ranks = {}

    top_checkins = sorted(d.keys(), key=lambda x: d[x]['engagement']['checkins'], reverse=True)[:10]
    ranks['most checkins'] = []
    for key in top_checkins:
        ranks['most checkins'].append([key, d[key]['engagement']['checkins']])

    top_percent_green = sorted(d.keys(), key=lambda x: d[x]['green']['perc_already_green'], reverse=True)[:10]
    ranks['percent green commuters'] = []
    for key in top_percent_green:
        ranks['percent green commuters'].append([key, d[key]['green']['perc_already_green']])

    top_participation = sorted(d.keys(), key=lambda x: d[x]['engagement']['perc_participants'], reverse=True)[:10]
    ranks['percent participation'] = []
    for key in top_participation:
        ranks['percent participation'].append([key, d[key]['engagement']['perc_participants']])

    # TODO alter to represent carbon saved as if everyone drove.
    top_carbon = sorted(d.keys(), key=lambda x: d[x]['green']['carbon_saved'], reverse=False)[:10]
    ranks['most carbon saved'] = []
    for key in top_carbon:
        ranks['most carbon saved'].append([key, d[key]['green']['carbon_saved']])

    top_calories = sorted(d.keys(), key=lambda x: d[x]['behavior']['calories_burned'], reverse=True)[:10]
    ranks['most calories burned'] = []
    for key in top_calories:
        ranks['most calories burned'].append([key, d[key]['behavior']['calories_burned']])

    # # returns top 10 employers for green switches
    # ranks['top_green'] =sorted(d.keys(), key=lambda x: d[x]['behavior']['green_switches'], reverse=True)[:10]

    # # returns top 10 employers for healthy switches
    # ranks['top_healthy'] = sorted(d.keys(), key=lambda x: d[x]['behavior']['healthy_switches'], reverse=True)[:10]

    return render_to_response('leaderboard/leaderboard_new.html', { 'ranks': ranks, 'totals': totals }, context)

def latest_leaderboard_small(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    d = {}

    ### TODO - filter related commutersurveys by MONTH

    companies = Employer.objects.only('id','name').filter(
        nr_employees__lt=500,
        active2015=False, 
        commutersurvey__created__gte=datetime.date(2015, 04, 15), 
        commutersurvey__created__lte=datetime.date(2015, 11, 01)).annotate(
        overall_carbon=Sum('commutersurvey__carbon_change'),
        saved_carbon=Sum('commutersurvey__carbon_savings'),
        overall_calories=Sum('commutersurvey__calorie_change'),
        num_checkins=Count('commutersurvey'),
        num_participants=Count('commutersurvey__email', distinct=True),
        num_already_green=Count('commutersurvey', only=Q(commutersurvey__already_green=True)),
        num_switch_green=Count('commutersurvey', only=Q(commutersurvey__change_type='g')),
        num_switch_healthy=Count('commutersurvey', only=Q(commutersurvey__change_type='h'))
    )

    totals = companies.aggregate(
        total_carbon=Sum('overall_carbon'),
        total_calories=Sum('overall_calories'),
        total_checkins=Sum('num_checkins')
    )

    for company in companies:
        d[str(company.name)] = calculate_metrics(company)

    ranks = {}

    top_checkins = sorted(d.keys(), key=lambda x: d[x]['engagement']['checkins'], reverse=True)[:10]
    ranks['most checkins'] = []
    for key in top_checkins:
        ranks['most checkins'].append([key, d[key]['engagement']['checkins']])

    top_percent_green = sorted(d.keys(), key=lambda x: d[x]['green']['perc_already_green'], reverse=True)[:10]
    ranks['percent green commuters'] = []
    for key in top_percent_green:
        ranks['percent green commuters'].append([key, d[key]['green']['perc_already_green']])

    top_participation = sorted(d.keys(), key=lambda x: d[x]['engagement']['perc_participants'], reverse=True)[:10]
    ranks['percent participation'] = []
    for key in top_participation:
        ranks['percent participation'].append([key, d[key]['engagement']['perc_participants']])

    # TODO alter to represent carbon saved as if everyone drove.
    top_carbon = sorted(d.keys(), key=lambda x: d[x]['green']['carbon_saved'], reverse=False)[:10]
    ranks['most carbon saved'] = []
    for key in top_carbon:
        ranks['most carbon saved'].append([key, d[key]['green']['carbon_saved']])

    top_calories = sorted(d.keys(), key=lambda x: d[x]['behavior']['calories_burned'], reverse=True)[:10]
    ranks['most calories burned'] = []
    for key in top_calories:
        ranks['most calories burned'].append([key, d[key]['behavior']['calories_burned']])

    # # returns top 10 employers for green switches
    # ranks['top_green'] =sorted(d.keys(), key=lambda x: d[x]['behavior']['green_switches'], reverse=True)[:10]

    # # returns top 10 employers for healthy switches
    # ranks['top_healthy'] = sorted(d.keys(), key=lambda x: d[x]['behavior']['healthy_switches'], reverse=True)[:10]

    return render_to_response('leaderboard/leaderboard_new.html', { 'ranks': ranks, 'totals': totals }, context)

def latest_leaderboard_medium(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    d = {}

    ### TODO - filter related commutersurveys by MONTH

    companies = Employer.objects.only('id','name').filter(
        nr_employees__gte=500,
        nr_employees__lt=2000,
        active2015=False, 
        commutersurvey__created__gte=datetime.date(2015, 04, 15), 
        commutersurvey__created__lte=datetime.date(2015, 11, 01)).annotate(
        overall_carbon=Sum('commutersurvey__carbon_change'),
        saved_carbon=Sum('commutersurvey__carbon_savings'),
        overall_calories=Sum('commutersurvey__calorie_change'),
        num_checkins=Count('commutersurvey'),
        num_participants=Count('commutersurvey__email', distinct=True),
        num_already_green=Count('commutersurvey', only=Q(commutersurvey__already_green=True)),
        num_switch_green=Count('commutersurvey', only=Q(commutersurvey__change_type='g')),
        num_switch_healthy=Count('commutersurvey', only=Q(commutersurvey__change_type='h'))
    )

    totals = companies.aggregate(
        total_carbon=Sum('overall_carbon'),
        total_calories=Sum('overall_calories'),
        total_checkins=Sum('num_checkins')
    )

    for company in companies:
        d[str(company.name)] = calculate_metrics(company)

    ranks = {}

    top_checkins = sorted(d.keys(), key=lambda x: d[x]['engagement']['checkins'], reverse=True)[:10]
    ranks['most checkins'] = []
    for key in top_checkins:
        ranks['most checkins'].append([key, d[key]['engagement']['checkins']])

    top_percent_green = sorted(d.keys(), key=lambda x: d[x]['green']['perc_already_green'], reverse=True)[:10]
    ranks['percent green commuters'] = []
    for key in top_percent_green:
        ranks['percent green commuters'].append([key, d[key]['green']['perc_already_green']])

    top_participation = sorted(d.keys(), key=lambda x: d[x]['engagement']['perc_participants'], reverse=True)[:10]
    ranks['percent participation'] = []
    for key in top_participation:
        ranks['percent participation'].append([key, d[key]['engagement']['perc_participants']])

    # TODO alter to represent carbon saved as if everyone drove.
    top_carbon = sorted(d.keys(), key=lambda x: d[x]['green']['carbon_saved'], reverse=False)[:10]
    ranks['most carbon saved'] = []
    for key in top_carbon:
        ranks['most carbon saved'].append([key, d[key]['green']['carbon_saved']])

    top_calories = sorted(d.keys(), key=lambda x: d[x]['behavior']['calories_burned'], reverse=True)[:10]
    ranks['most calories burned'] = []
    for key in top_calories:
        ranks['most calories burned'].append([key, d[key]['behavior']['calories_burned']])

    # # returns top 10 employers for green switches
    # ranks['top_green'] =sorted(d.keys(), key=lambda x: d[x]['behavior']['green_switches'], reverse=True)[:10]

    # # returns top 10 employers for healthy switches
    # ranks['top_healthy'] = sorted(d.keys(), key=lambda x: d[x]['behavior']['healthy_switches'], reverse=True)[:10]

    return render_to_response('leaderboard/leaderboard_new.html', { 'ranks': ranks, 'totals': totals }, context)

def latest_leaderboard_large(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    d = {}

    ### TODO - filter related commutersurveys by MONTH

    companies = Employer.objects.only('id','name').filter(
        nr_employees__gte=2000,
        active2015=False, 
        commutersurvey__created__gte=datetime.date(2015, 04, 15), 
        commutersurvey__created__lte=datetime.date(2015, 11, 01)).annotate(
        overall_carbon=Sum('commutersurvey__carbon_change'),
        saved_carbon=Sum('commutersurvey__carbon_savings'),
        overall_calories=Sum('commutersurvey__calorie_change'),
        num_checkins=Count('commutersurvey'),
        num_participants=Count('commutersurvey__email', distinct=True),
        num_already_green=Count('commutersurvey', only=Q(commutersurvey__already_green=True)),
        num_switch_green=Count('commutersurvey', only=Q(commutersurvey__change_type='g')),
        num_switch_healthy=Count('commutersurvey', only=Q(commutersurvey__change_type='h'))
    )

    totals = companies.aggregate(
        total_carbon=Sum('overall_carbon'),
        total_calories=Sum('overall_calories'),
        total_checkins=Sum('num_checkins')
    )

    for company in companies:
        d[str(company.name)] = calculate_metrics(company)

    ranks = {}

    top_checkins = sorted(d.keys(), key=lambda x: d[x]['engagement']['checkins'], reverse=True)[:10]
    ranks['most checkins'] = []
    for key in top_checkins:
        ranks['most checkins'].append([key, d[key]['engagement']['checkins']])

    top_percent_green = sorted(d.keys(), key=lambda x: d[x]['green']['perc_already_green'], reverse=True)[:10]
    ranks['percent green commuters'] = []
    for key in top_percent_green:
        ranks['percent green commuters'].append([key, d[key]['green']['perc_already_green']])

    top_participation = sorted(d.keys(), key=lambda x: d[x]['engagement']['perc_participants'], reverse=True)[:10]
    ranks['percent participation'] = []
    for key in top_participation:
        ranks['percent participation'].append([key, d[key]['engagement']['perc_participants']])

    # TODO alter to represent carbon saved as if everyone drove.
    top_carbon = sorted(d.keys(), key=lambda x: d[x]['green']['carbon_saved'], reverse=False)[:10]
    ranks['most carbon saved'] = []
    for key in top_carbon:
        ranks['most carbon saved'].append([key, d[key]['green']['carbon_saved']])

    top_calories = sorted(d.keys(), key=lambda x: d[x]['behavior']['calories_burned'], reverse=True)[:10]
    ranks['most calories burned'] = []
    for key in top_calories:
        ranks['most calories burned'].append([key, d[key]['behavior']['calories_burned']])

    # # returns top 10 employers for green switches
    # ranks['top_green'] =sorted(d.keys(), key=lambda x: d[x]['behavior']['green_switches'], reverse=True)[:10]

    # # returns top 10 employers for healthy switches
    # ranks['top_healthy'] = sorted(d.keys(), key=lambda x: d[x]['behavior']['healthy_switches'], reverse=True)[:10]

    return render_to_response('leaderboard/leaderboard_new.html', { 'ranks': ranks, 'totals': totals }, context)


