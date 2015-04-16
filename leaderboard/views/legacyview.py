# File: leaderboard views
# Description: creates data for page at /leaderboard/. All pages are handled by
# the new_leaderboard() function. lb_redirect() is a target for the filter form
# which transforms parameters into a clean URL and redirects back to 
# new_leaderboard(). new_leaderboard() calls participation_rankings(),
# participation_pct(), getBreakdown(), and getCanvasJSChart() to fill in rankings,
# company breakdown, and chart data.
# Authors: John Freeman, Owen Lynch
# Date: 5/17/2014

from survey.models import Commutersurvey, Employer, EmplSector, Leg, Month
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from operator import itemgetter, attrgetter
import json
from django.shortcuts import redirect
from django.db import connections
from datetime import date
from django.db.models import Sum,Count
from django.db import connection


COLOR_SCHEME = {
        'gs': '#0096FF',
        'gc': '#65AB4B',
        'cc': '#FF2600',
        'us': '#9437FF',
        'hs': '#000000',
        'hc': '#f0f0f0',
        'rgs': '#0096FF',
        'rgc': '#65AB4B',
        'rcc': '#FF2600',
        'rus': '#9437FF',
        'ngs': '#00C8FF',
        'ngc': '#75FF57',
        'ncc': '#FF266E',
        'nus': '#9496FF',
        }

def lb_redirect(request):
    if request.GET['color'] == "sector":
        val = request.GET['sector_filter']
    elif request.GET['color'] == "size":
        val = request.GET['size_filter']
    elif request.GET['color'] == "nofilter":
        return redirect("/legacy-leaderboard/", permanent=True)
    url = "/legacy-leaderboard/"
    if 'empid' in request.GET:
        url += request.GET['empid']+'/'
    url += request.GET['color']+"/"+val+"/"
    if 'sort' in request.GET:
        url += request.GET['sort']+'/'
    if 'month' in request.GET:
        url += 'month_'
        url += request.GET['month']
    return redirect(url, permanent=True)

nmonths = 1

def new_leaderboard(request, empid=0, filter_by='sector', _filter=0, sort='participation', selmonth='all'):

    db = connections['default'].cursor()
    context = {}
    context['empid'] = empid
    
    if empid != 0:
        #workaround for the subteam parents
        if Employer.objects.filter(active=True,id=empid,is_parent='t'):
            #need to collect all the subteams to get right totals
            parentname = Employer.objects.filter(active=True,id=empid).values('name')
            childteams = Employer.objects.filter(active=True,sector__parent=parentname)
            checkins = Commutersurvey.objects.filter(wr_day_month__gte=32, wr_day_month__lte=38, employer__in=childteams)
        else:
            checkins = Commutersurvey.objects.filter(wr_day_month__gte=32, wr_day_month__lte=38, employer_id=empid)
        

        try:
            company = Employer.objects.filter(active=True,id=empid)[0]
        except:
            return json.dumps({"error" : "Invalid employer id"})
        mos = [m.id for m in Month.objects.filter(id__gte=32, id__lte=38)] # Get 2014 months
        firstMonth = min(mos)

        # Selects the count of distinct emails for a given month and employer (the case statement is to deal with subgroups)
        queryAll = """SELECT COUNT(DISTINCT email) FROM survey_commutersurvey WHERE survey_commutersurvey.wr_day_month_id = {1} AND CASE WHEN(SELECT is_parent FROM survey_employer WHERE id = {0}) = 't' THEN survey_commutersurvey.employer_id IN (SELECT survey_employer.id FROM survey_employer JOIN survey_emplsector ON survey_employer.sector_id = survey_emplsector.id WHERE survey_emplsector.parent = (SELECT name FROM survey_employer WHERE id = {0}) ) ELSE survey_commutersurvey.employer_id = {0} END"""

        # Same as above, but filters out emails used in previous months
        queryNew = """SELECT COUNT(DISTINCT email) FROM survey_commutersurvey WHERE survey_commutersurvey.wr_day_month_id = {2} AND CASE WHEN(SELECT is_parent FROM survey_employer WHERE id = {0}) = 't' THEN survey_commutersurvey.employer_id IN(SELECT survey_employer.id FROM survey_employer JOIN survey_emplsector ON survey_employer.sector_id = survey_emplsector.id WHERE survey_emplsector.parent = (SELECT name FROM survey_employer WHERE id = {0}) ) AND survey_commutersurvey.email NOT IN ( SELECT survey_commutersurvey.email FROM survey_commutersurvey WHERE wr_day_month_id BETWEEN {1} AND {2}-1 AND employer_id IN (SELECT survey_employer.id FROM survey_employer JOIN survey_emplsector ON survey_employer.sector_id = survey_emplsector.id WHERE survey_emplsector.parent = (SELECT name FROM survey_employer WHERE id = {0} ) ) ) ELSE survey_commutersurvey.employer_id = {0} AND email NOT IN (SELECT email FROM survey_commutersurvey WHERE employer_id = {0} AND wr_day_month_id BETWEEN {1} AND {2}-1 ) END"""

        c = connection.cursor()

        checkinData = [];

        for month in mos:
            c.execute(queryAll.format(empid, month))
            allCheckins = c.fetchone()[0] # Add count of all checkins for that month
            c.execute(queryNew.format(empid, firstMonth, month))
            newCheckins = c.fetchone()[0]
            checkinData.append({"month":month, "all": allCheckins, "new": newCheckins })

        employersNewVsReturning = json.dumps({"id" : company.id, "name": company.name, "size": company.nr_employees, "checkins": checkinData})
        
        context['empNVR'] = employersNewVsReturning


    non_companies = [1983,1105,1155] # none, Other employer, self
    context['active_companies'] = Employer.objects.filter(active=True).exclude(id__in=non_companies)

    if _filter == '0':
        _filter = 0
   
    if empid != 0:
        res = Employer.objects.filter(id=empid)
        emp = res[0]
        sector = emp.sector
    if empid != 0 and _filter == 0:
        _filter = sector.id

    context['filter_by'] = filter_by
    context['filt'] = _filter
    if filter_by == 'sector':
        context['sectorid'] = _filter
    context['sort'] = sort
    context['sectors'] = sorted(EmplSector.objects.all(), key=getSectorNum)
    context['subteams'] = get_subteams()
    months = Month.objects.filter(id__gte=32, id__lte=38)
    context['months'] = months
    for m in months:
        if m.url_month == selmonth:
            month = m.id
            context['display_month'] = m.month

    if selmonth == 'all':
        month = 'all'
        context['display_month'] = "all months"
        nmonths = len(months)
    else:
        nmonths = 1

    if filter_by == 'size':
        if _filter == 0:
            context['sizecat'] = 'all sizes';
        if _filter == '1':
            context['sizecat'] = 'small companies';
        if _filter == '2':
            context['sizecat'] = 'medium companies';
        if _filter == '3':
            context['sizecat'] = 'large companies';
        if _filter == '4':
            context['sizecat'] = 'largest companies';


    context['current_month'] = selmonth

    context['ranks'] = participation_rankings(month, filter_by, _filter)
    context['ranks_pct'] = participation_pct(month, filter_by, _filter)
    
    context['total_companies'] = len(context['ranks_pct'])
    context['total'] = 0
    for rank in context['ranks']:
        context['total'] += rank[0]
    
    if _filter == 0:
        context['emp_sector'] = 'all sectors'
    elif filter_by == 'sector' and empid == 0:
        sector = EmplSector.objects.filter(id=_filter)
        context['emp_sector'] = sector[0]

    # if a company detail page, fill in all data for selected company
    if empid != 0:
        # context['chart'] = json.dumps(getCanvasJSChart(emp) )
        nsurveys=0
        for count in context['ranks']:
            if count[2] == int(empid):
                nsurveys = count[0]
        for count in context['ranks_pct']:
            if count[2] == int(empid):
                context['participation'] = count[0]

        context['ncommutes'] = nsurveys*2
        context['employer'] = emp
        context['emp_sector'] = emp.sector
        context['sectorid'] = emp.sector.id
        
    return render(request, 'leaderboard/leaderboard_js.html', context)

def getSectorNum(sector):
        return sector.id


def get_subteams():
    sectors = sorted(EmplSector.objects.all(), key=getSectorNum)
    subteams = []
    for sector in sectors:
        if sector.id > 9:
            subteams.append(sector)

    return subteams


def participation_rankings(month, filter_by, _filter=0):
    db = connections['default'].cursor()
    args = []
    
    if month != 'all':
        monthq = "wr_day_month_id = %s";
        montharg = month
        args.append(montharg)
    else:
        monthq = " wr_day_month_id in (select id from survey_month where active = %s) "
        montharg = 't';
        args.append(montharg)
    if filter_by == 'size' and _filter != 0:
        filterq = " and e.size_cat_id = %s "
        subteam_filterq = " and e2.size_cat_id = %s "
        args.append(_filter)
    elif filter_by == 'sector' and _filter != 0:
        filterq = " and e.sector_id = %s "
        subteam_filterq = " and e2.sector_id = %s "
        args.append(_filter)
    else:
        filterq = ""
        subteam_filterq = ""

    if filter_by == 'sector' and _filter > 9:
        sectorq = ""
    else:
        sectorq = " and sector_id < 10 "

    if len(monthq) > 1:
        args.append(montharg)
    if len(filterq) > 1:
        args.append(_filter)

    db.execute("select count(cs.id) as nsurveys, e.name, e.id from survey_commutersurvey as cs join survey_employer as e on (employer_id = e.id) where " + monthq + sectorq + filterq + " and e.is_parent = 'f' and e.nr_employees > 0 group by e.name, e.id " +
    "union all select count(cs.id) as nsurveys, sec.parent, e2.id from survey_commutersurvey cs join survey_employer e on (cs.employer_id = e.id) join survey_emplsector sec on (e.sector_id = sec.id), survey_employer e2 where sec.parent is not null and e2.name = sec.parent and " + monthq + subteam_filterq + " group by sec.parent, e2.id order by nsurveys desc", args)
    return db.fetchall()


def participation_pct(month, filter_by, _filter=0):
    db = connections['default'].cursor() 
    args = []
    
    if month != 'all':
        monthq = "wr_day_month_id = %s";
        montharg = month
        args.append(montharg)
        pctq = "1"
    else:
        monthq = " wr_day_month_id in (select id from survey_month where active = %s) "
        montharg = 't';
        args.append(montharg)
        pctq="(select count(*) from survey_month where open_checkin < current_date and active = 't')"
    if filter_by == 'size' and _filter != 0:
        filterq = " and e.size_cat_id = %s "
        subteam_filterq = " and e2.size_cat_id = %s "
        args.append(_filter)
    elif filter_by == 'sector' and _filter != 0:
        filterq = " and e.sector_id = %s "
        subteam_filterq = " and e2.sector_id = %s "
        args.append(_filter)
    else:
        filterq = ""
        subteam_filterq = ""

    if filter_by == 'sector' and _filter > 9:
        sectorq = ""
    else:
        sectorq = " and sector_id < 10 "

    if len(monthq) > 1:
        args.append(montharg)
    if len(filterq) > 1:
        args.append(_filter)

    db.execute("select count(cast(cs.id as float8) ) / (cast(e.nr_employees*"+pctq+" as float8) ) * 100 as pct, e.name, e.id from survey_commutersurvey as cs join survey_employer as e on (employer_id = e.id) where " + monthq + sectorq + filterq + " and e.is_parent = 'f' and e.nr_employees > 0 group by e.name, e.id " + 
    "union all select count(cast(cs.id as float8) ) / (cast(e2.nr_employees*"+pctq+" as float8) ) * 100 as pct, sec.parent, e2.id from survey_commutersurvey cs join survey_employer e on (cs.employer_id = e.id) join survey_emplsector sec on (e.sector_id = sec.id), survey_employer e2 where sec.parent is not null and e2.name = sec.parent and e2.nr_employees > 0 and " + monthq + subteam_filterq + " group by sec.parent, e2.id, e2.nr_employees order by pct desc", args)
    return db.fetchall()

