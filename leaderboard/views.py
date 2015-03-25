# # File: leaderboard views
# # Description: creates data for page at /leaderboard/. All pages are handled by
# # the new_leaderboard() function. lb_redirect() is a target for the filter form
# # which transforms parameters into a clean URL and redirects back to
# # new_leaderboard(). new_leaderboard() calls participation_rankings(),
# # participation_pct(), getBreakdown(), and getCanvasJSChart() to fill in rankings,
# # company breakdown, and chart data.
# # Authors: John Freeman, Owen Lynch
# # Date: 5/17/2014
from __future__ import division
from survey.models import Commutersurvey, Employer, EmplSector, Leg, Month, Team, Mode
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.http import HttpResponse
# from operator import itemgetter, attrgetter
# import json
# from django.shortcuts import redirect
# from django.db import connections
# from datetime import date
from django.db.models import Sum,Count
# from django.db import connection


def calculate_engagement(company):
    employee_engagement = {}
    employee_engagement["checkins"] = company.nr_surveys
    employee_engagement["num_participants"] = company.nr_participants

    if company.nr_employees is not None:
        employee_engagement["perc_participants"] = employee_engagement["num_participants"] / company.nr_employees

    employee_engagement["avg_frequency"] = employee_engagement["checkins"] / (employee_engagement["num_participants"] * 7)

    return employee_engagement

def calculate_green(company):
    surveys = Commutersurvey.objects.filter(employer=company)

    overall_carbon_change = 0.00 # will be negative if saved, positive if gained


    for survey in surveys:
        overall_carbon_change += survey.carbon_change

    green = surveys.filter(already_green=True).count()
    checkins = surveys.count()

    green_momentum = {}
    green_momentum["num_already_green"] = green
    green_momentum["perc_already_green"] = green / checkins
    green_momentum["carbon_saved"] = overall_carbon_change

    return green_momentum



def calculate_behavior(qs):
    behavior_change = {}
    # behavior_change["green_switches"] =
    # behavior_change["perc_green"] =
    # behavior_change["healthy_switches"] =
    # behavior_change["perc_healthy"] =
    # behavior_change["positive_switches"] =
    # behavior_change["perc_positive"] =
    return behavior_change


def new_leaderboard(request, selected_months='all'):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)

    context_dict = {}

    for company in Employer.objects.all():
        context_dict[str(company.name)] = {'engagement': calculate_engagement(company), 'green': calculate_green(company), 'behavior': calculate_behavior(company) }

    # Render the response and send it back!
    return render_to_response('leaderboard/leaderboard_new.html', {'context_dict': context_dict}, context)














# COLOR_SCHEME = {
#         'gs': '#0096FF',
#         'gc': '#65AB4B',
#         'cc': '#FF2600',
#         'us': '#9437FF',
#         'hs': '#000000',
#         'hc': '#f0f0f0',
#         'rgs': '#0096FF',
#         'rgc': '#65AB4B',
#         'rcc': '#FF2600',
#         'rus': '#9437FF',
#         'ngs': '#00C8FF',
#         'ngc': '#75FF57',
#         'ncc': '#FF266E',
#         'nus': '#9496FF',
#         }

# def lb_redirect(request):
#     if request.GET['color'] == "sector":
#         val = request.GET['sector_filter']
#     elif request.GET['color'] == "size":
#         val = request.GET['size_filter']
#     elif request.GET['color'] == "nofilter":
#         return redirect("/leaderboard/", permanent=True)
#     url = "/leaderboard/"
#     if 'empid' in request.GET:
#         url += request.GET['empid']+'/'
#     url += request.GET['color']+"/"+val+"/"
#     if 'sort' in request.GET:
#         url += request.GET['sort']+'/'
#     if 'month' in request.GET:
#         url += 'month_'
#         url += request.GET['month']
#     return redirect(url, permanent=True)

# nmonths = 1

# def new_leaderboard(request, empid=0, filter_by='sector', _filter=0, sort='participation', selmonth='all'):

#     db = connections['default'].cursor()
#     context = {}
#     context['empid'] = empid

#     if empid != 0:
#         #workaround for the subteam parents
#         if Employer.objects.filter(id=empid,is_parent='t'):
#             #need to collect all the subteams to get right totals
#             parentname = Employer.objects.filter(id=empid).values('name')
#             childteams = Employer.objects.filter(sector__parent=parentname,active='t')
#             checkins = Commutersurvey.objects.filter(wr_day_month__gte=32, employer__in=childteams)
#         else:
#             checkins = Commutersurvey.objects.filter(wr_day_month__gte=32, employer_id=empid)

#         # allmodes = ['w','b','r','t','cp','tc','da','dalt','o']
#         greenmodes = ['w','b','r','t','cp']
#         yellowmodes = ['tc']
#         redmodes = ['da','dalt']
#         othermodes = ['o']

#         modesplitG = {}
#         modesplitY = {}
#         modesplitR = {}
#         modesplitO = {}

#         for m in greenmodes:
#             modesplitG[m] = {}
#             num_mode_n = checkins.filter(leg__mode=m,leg__day__exact='n').distinct().count()
#             num_mode_w = checkins.filter(leg__mode=m,leg__day__exact='w').distinct().count()
#             modesplitG[m]['onmode_n']= num_mode_n
#             modesplitG[m]['onmode_w']= num_mode_w
#             diff = float(num_mode_w - num_mode_n)
#             if num_mode_n > 0:
#                 modesplitG[m]['diff']=  round(diff*100/(num_mode_n),1)
#             else:
#                 modesplitG[m]['diff']= 0.0

#         for m in yellowmodes:
#             modesplitY[m] = {}
#             num_mode_n = checkins.filter(leg__mode=m,leg__day__exact='n').distinct().count()
#             num_mode_w = checkins.filter(leg__mode=m,leg__day__exact='w').distinct().count()
#             modesplitY[m]['onmode_n']= num_mode_n
#             modesplitY[m]['onmode_w']= num_mode_w
#             diff = float(num_mode_w - num_mode_n)
#             if num_mode_n > 0:
#                 modesplitY[m]['diff']=  round(diff*100/(num_mode_n),1)
#             else:
#                 modesplitY[m]['diff']= 0.0

#         for m in redmodes:
#             modesplitR[m] = {}
#             num_mode_n = checkins.filter(leg__mode=m,leg__day__exact='n').distinct().count()
#             num_mode_w = checkins.filter(leg__mode=m,leg__day__exact='w').distinct().count()
#             modesplitR[m]['onmode_n']= num_mode_n
#             modesplitR[m]['onmode_w']= num_mode_w
#             diff = float(num_mode_w - num_mode_n)
#             if num_mode_n > 0:
#                 modesplitR[m]['diff']=  round(diff*100/(num_mode_n),1)
#             else:
#                 modesplitR[m]['diff']= 0.0

#         for m in othermodes:
#             modesplitO[m] = {}
#             num_mode_n = checkins.filter(leg__mode=m,leg__day__exact='n').distinct().count()
#             num_mode_w = checkins.filter(leg__mode=m,leg__day__exact='w').distinct().count()
#             modesplitO[m]['onmode_n']= num_mode_n
#             modesplitO[m]['onmode_w']= num_mode_w
#             diff = float(num_mode_w - num_mode_n)
#             if num_mode_n > 0:
#                 modesplitO[m]['diff']=  round(diff*100/(num_mode_n),1)
#             else:
#                 modesplitO[m]['diff']= 0.0


#         context['thismodeG'] = modesplitG
#         context['thismodeY'] = modesplitY
#         context['thismodeR'] = modesplitR
#         context['thismodeO'] = modesplitO

#         # allmonths = [32,33,34,35,36,37,38]
#         # allmonths2 = [{32: 'April'},{33: 'May'},{},{},{},{},]

#         # monthsplit = {}

#         # for month in allmonths:
#         #     monthsplit[month] = {}
#         #     checkinsdone = checkins.filter(wr_day_month=month,leg__day__exact='w').distinct().count()
#         #     monthsplit[month] = checkinsdone

#         # context['monthlycheckin'] = monthsplit


#         try:
#             company = Employer.objects.filter(id=empid)[0]
#         except:
#             return json.dumps({"error" : "Invalid employer id"})
#         mos = [m.id for m in Month.objects.active_months().reverse().exclude(open_checkin__gt=date.today())] # Get valid months
#         firstMonth = min(mos)

#         # Selects the count of distinct emails for a given month and employer (the case statement is to deal with subgroups)
#         queryAll = """SELECT COUNT(DISTINCT email) FROM survey_commutersurvey WHERE survey_commutersurvey.wr_day_month_id = {1} AND CASE WHEN(SELECT is_parent FROM survey_employer WHERE id = {0}) = 't' THEN survey_commutersurvey.employer_id IN (SELECT survey_employer.id FROM survey_employer JOIN survey_emplsector ON survey_employer.sector_id = survey_emplsector.id WHERE survey_emplsector.parent = (SELECT name FROM survey_employer WHERE id = {0}) ) ELSE survey_commutersurvey.employer_id = {0} END"""

#         # Same as above, but filters out emails used in previous months
#         queryNew = """SELECT COUNT(DISTINCT email) FROM survey_commutersurvey WHERE survey_commutersurvey.wr_day_month_id = {2} AND CASE WHEN(SELECT is_parent FROM survey_employer WHERE id = {0}) = 't' THEN survey_commutersurvey.employer_id IN(SELECT survey_employer.id FROM survey_employer JOIN survey_emplsector ON survey_employer.sector_id = survey_emplsector.id WHERE survey_emplsector.parent = (SELECT name FROM survey_employer WHERE id = {0}) ) AND survey_commutersurvey.email NOT IN ( SELECT survey_commutersurvey.email FROM survey_commutersurvey WHERE wr_day_month_id BETWEEN {1} AND {2}-1 AND employer_id IN (SELECT survey_employer.id FROM survey_employer JOIN survey_emplsector ON survey_employer.sector_id = survey_emplsector.id WHERE survey_emplsector.parent = (SELECT name FROM survey_employer WHERE id = {0} ) ) ) ELSE survey_commutersurvey.employer_id = {0} AND email NOT IN (SELECT email FROM survey_commutersurvey WHERE employer_id = {0} AND wr_day_month_id BETWEEN {1} AND {2}-1 ) END"""

#         c = connection.cursor()

#         checkinData = [];

#         for month in mos:
#             c.execute(queryAll.format(empid, month))
#             allCheckins = c.fetchone()[0] # Add count of all checkins for that month
#             c.execute(queryNew.format(empid, firstMonth, month))
#             newCheckins = c.fetchone()[0]
#             checkinData.append({"month":month, "all": allCheckins, "new": newCheckins })

#         employersNewVsReturning = json.dumps({"id" : company.id, "name": company.name, "size": company.nr_employees, "checkins": checkinData})

#         context['empNVR'] = employersNewVsReturning

#         # query_modes = "SELECT survey_leg.day, survey_leg.mode, survey_commutersurvey.wr_day_month_id, COUNT(DISTINCT survey_commutersurvey.id) FROM survey_leg JOIN survey_commutersurvey ON survey_leg.commutersurvey_id = survey_commutersurvey.id WHERE survey_commutersurvey.wr_day_month_id BETWEEN {0} AND {1} AND survey_leg.mode IN ('da','dalt','w','b','t','o','r','tc') AND CASE WHEN (SELECT is_parent FROM survey_employer WHERE id = {2}) = 't' THEN survey_commutersurvey.employer_id IN (SELECT survey_employer.id FROM survey_employer JOIN survey_emplsector ON survey_employer.sector_id = survey_emplsector.id WHERE survey_emplsector.parent = (  SELECT name FROM survey_employer WHERE id = {2} ) ) ELSE survey_commutersurvey.employer_id = {2} END GROUP BY survey_leg.day, survey_leg.mode, survey_commutersurvey.wr_day_month_id"

#         # c.execute(query_modes.format(min(mos), max(mos), empid))
#         # checkinsByMode = json.dumps(c.fetchall())

#         # context['checkinsByMode'] = checkinsByMode

#     non_companies = [1983,1105,1155] # none, Other employer, self
#     context['active_companies'] = Employer.objects.filter(active=True).exclude(id__in=non_companies)

#     if _filter == '0':
#         _filter = 0

#     if empid != 0:
#         res = Employer.objects.filter(id=empid)
#         emp = res[0]
#         sector = emp.sector
#     if empid != 0 and _filter == 0:
#         _filter = sector.id

#     context['filter_by'] = filter_by
#     context['filt'] = _filter
#     if filter_by == 'sector':
#         context['sectorid'] = _filter
#     context['sort'] = sort
#     context['sectors'] = sorted(EmplSector.objects.all(), key=getSectorNum)
#     context['subteams'] = get_subteams()
#     months = Month.objects.active_months().reverse().exclude(open_checkin__gt=date.today() )
#     context['months'] = months
#     for m in months:
#         if m.url_month == selmonth:
#             month = m.id
#             context['display_month'] = m.month

#     if selmonth == 'all':
#         month = 'all'
#         context['display_month'] = "all months"
#         nmonths = len(months)
#     else:
#         nmonths = 1

#     if filter_by == 'size':
#         if _filter == 0:
#             context['sizecat'] = 'all sizes';
#         if _filter == '1':
#             context['sizecat'] = 'small companies';
#         if _filter == '2':
#             context['sizecat'] = 'medium companies';
#         if _filter == '3':
#             context['sizecat'] = 'large companies';
#         if _filter == '4':
#             context['sizecat'] = 'largest companies';


#     context['current_month'] = selmonth

#     context['ranks'] = participation_rankings(month, filter_by, _filter)
#     context['ranks_pct'] = participation_pct(month, filter_by, _filter)

#     context['total_companies'] = len(context['ranks_pct'])
#     context['total'] = 0
#     for rank in context['ranks']:
#         context['total'] += rank[0]

#     if _filter == 0:
#         context['emp_sector'] = 'all sectors'
#     elif filter_by == 'sector' and empid == 0:
#         sector = EmplSector.objects.filter(id=_filter)
#         context['emp_sector'] = sector[0]

#     # if a company detail page, fill in all data for selected company
#     if empid != 0:
#         # context['chart'] = json.dumps(getCanvasJSChart(emp) )
#         stats_month = getBreakDown(emp, month)
#         stats_all = stats_month
#         nsurveys=0
#         if month != 'all':
#             stats_all = getBreakDown(emp, 'all')
#         for count in context['ranks']:
#             if count[2] == int(empid):
#                 nsurveys = count[0]
#         for count in context['ranks_pct']:
#             if count[2] == int(empid):
#                 context['participation'] = count[0]

#         context['ncommutes'] = nsurveys*2
#         context['gc'] = stats_month['gc']
#         context['gs'] = stats_month['gs']

#         context['gs_total'] = stats_all['gs']
#         context['gc_total'] = stats_all['gc']
#         context['cc_total'] = stats_all['cc']
#         context['other_total'] = stats_all['us']
#         context['ncommutes_total'] = stats_all['total']

#         if nsurveys != 0:
#             context['gc_pct'] = ( ( stats_month['gc']*1.0) / (nsurveys*2.0) ) * 100
#             context['gs_pct'] = ( ( stats_month['gs']*1.0) / (nsurveys*2.0) ) * 100
#         else:
#             context['gs_pct'] = 0
#             context['gc_pct'] = 0
#         context['stats'] = stats_month
#         context['employer'] = emp
#         context['emp_sector'] = emp.sector
#         context['sectorid'] = emp.sector.id

#     return render(request, 'leaderboard/leaderboard_js.html', context)

# def getSectorNum(sector):
#         return sector.id


# def get_subteams():
#     sectors = sorted(EmplSector.objects.all(), key=getSectorNum)
#     subteams = []
#     for sector in sectors:
#         if sector.id > 9:
#             subteams.append(sector)

#     return subteams


# def participation_rankings(month, filter_by, _filter=0):
#     db = connections['default'].cursor()
#     args = []

#     if month != 'all':
#         monthq = "wr_day_month_id = %s";
#         montharg = month
#         args.append(montharg)
#     else:
#         monthq = " wr_day_month_id in (select id from survey_month where active = %s) "
#         montharg = 't';
#         args.append(montharg)
#     if filter_by == 'size' and _filter != 0:
#         filterq = " and e.size_cat_id = %s "
#         subteam_filterq = " and e2.size_cat_id = %s "
#         args.append(_filter)
#     elif filter_by == 'sector' and _filter != 0:
#         filterq = " and e.sector_id = %s "
#         subteam_filterq = " and e2.sector_id = %s "
#         args.append(_filter)
#     else:
#         filterq = ""
#         subteam_filterq = ""

#     if filter_by == 'sector' and _filter > 9:
#         sectorq = ""
#     else:
#         sectorq = " and sector_id < 10 "

#     if len(monthq) > 1:
#         args.append(montharg)
#     if len(filterq) > 1:
#         args.append(_filter)

#     db.execute("select count(cs.id) as nsurveys, e.name, e.id from survey_commutersurvey as cs join survey_employer as e on (employer_id = e.id) where " + monthq + sectorq + filterq + " and e.is_parent = 'f' and e.nr_employees > 0 group by e.name, e.id " +
#     "union all select count(cs.id) as nsurveys, sec.parent, e2.id from survey_commutersurvey cs join survey_employer e on (cs.employer_id = e.id) join survey_emplsector sec on (e.sector_id = sec.id), survey_employer e2 where sec.parent is not null and e2.name = sec.parent and " + monthq + subteam_filterq + " group by sec.parent, e2.id order by nsurveys desc", args)
#     return db.fetchall()


# def participation_pct(month, filter_by, _filter=0):
#     db = connections['default'].cursor()
#     args = []

#     if month != 'all':
#         monthq = "wr_day_month_id = %s";
#         montharg = month
#         args.append(montharg)
#         pctq = "1"
#     else:
#         monthq = " wr_day_month_id in (select id from survey_month where active = %s) "
#         montharg = 't';
#         args.append(montharg)
#         pctq="(select count(*) from survey_month where open_checkin < current_date and active = 't')"
#     if filter_by == 'size' and _filter != 0:
#         filterq = " and e.size_cat_id = %s "
#         subteam_filterq = " and e2.size_cat_id = %s "
#         args.append(_filter)
#     elif filter_by == 'sector' and _filter != 0:
#         filterq = " and e.sector_id = %s "
#         subteam_filterq = " and e2.sector_id = %s "
#         args.append(_filter)
#     else:
#         filterq = ""
#         subteam_filterq = ""

#     if filter_by == 'sector' and _filter > 9:
#         sectorq = ""
#     else:
#         sectorq = " and sector_id < 10 "

#     if len(monthq) > 1:
#         args.append(montharg)
#     if len(filterq) > 1:
#         args.append(_filter)

#     db.execute("select count(cast(cs.id as float8) ) / (cast(e.nr_employees*"+pctq+" as float8) ) * 100 as pct, e.name, e.id from survey_commutersurvey as cs join survey_employer as e on (employer_id = e.id) where " + monthq + sectorq + filterq + " and e.is_parent = 'f' and e.nr_employees > 0 group by e.name, e.id " +
#     "union all select count(cast(cs.id as float8) ) / (cast(e2.nr_employees*"+pctq+" as float8) ) * 100 as pct, sec.parent, e2.id from survey_commutersurvey cs join survey_employer e on (cs.employer_id = e.id) join survey_emplsector sec on (e.sector_id = sec.id), survey_employer e2 where sec.parent is not null and e2.name = sec.parent and e2.nr_employees > 0 and " + monthq + subteam_filterq + " group by sec.parent, e2.id, e2.nr_employees order by pct desc", args)
#     return db.fetchall()


# def getBreakDown(emp, month):
#     hs = 0
#     hc = 0
#     gs = 0
#     gc = 0
#     cc = 0
#     other = 0

#     # tw = from work, fw = from work, n/w normal day or WR day
#     highest_fw_n = 0
#     highest_fw_w = 0
#     highest_tw_n = 0
#     highest_tw_w = 0

#     tw_w_mode = ''
#     tw_n_mode = ''
#     fw_w_mode = ''
#     fw_n_mode = ''

#     db = connections['default'].cursor()
#     args = []
#     if emp.is_parent == True:
#         eid = " employer_id in (select id from survey_employer where sector_id in (select id from survey_emplsector where parent = %s) ) "
#         args.append(emp.name)
#     else:
#         eid = " employer_id = %s "
#         args.append(emp.id)

#     if month == 'all':
#         monthq = " wr_day_month_id in (select id from survey_month where active = %s) "
#         args.append('t')
#     else:
#         monthq = " wr_day_month_id = %s "
#         args.append(month)

#     db.execute("select commutersurvey_id, direction, day,  mode, case when mode in ('b', 'r', 'w', 'o') then 5 when mode = 'tc' then 4 when mode = 't' then 3 when mode = 'cp' then 2 when mode in ('c', 'da') then 1 end as rank, wr_day_month_id from survey_leg join survey_commutersurvey cs on (commutersurvey_id = cs.id) where " + eid + " and " + monthq + " order by commutersurvey_id", args);
#     surveys = db.fetchall()

#     breakdown = {}
#     modes = [ 'c', 'cp', 'da', 'dalt', 'w', 'b', 'r', 't', 'o', 'tc' ]
#     for mode in modes:
#         breakdown[mode] = {}
#         for mode2 in modes:
#             breakdown[mode][mode2] = 0
#     breakdown['total'] = 0

#     i = 1
#     if len(surveys) != 0:
#         lastid = surveys[0][0]
#         for survey in surveys:
#             if survey[0] != lastid or i == len(surveys):
#                 breakdown['total'] += 2
#                 if highest_fw_w > highest_fw_n and highest_fw_w == 5:
#                     gs += 1 # formerly healthy switch, now green
#                 elif highest_fw_w == 5:
#                     gc += 1 # formerly healthy commute, now green
#                 elif highest_fw_w > highest_fw_n:
#                     gs += 1 # green switch
#                 elif highest_fw_w > 1:
#                     gc += 1 # green commute
#                 elif highest_fw_w < highest_fw_n:
#                     other += 1 # other (less healthy/green switch)
#                 elif highest_fw_w == 1:
#                     cc += 1 # car commute

#                 if highest_tw_w > highest_tw_n and highest_tw_w == 5:
#                     gs += 1 # former healthy switch
#                 elif highest_tw_w == 5:
#                     gc += 1 # former healthy commute
#                 elif highest_tw_w > highest_tw_n:
#                     gs += 1 # green switch
#                 elif highest_tw_w > 1:
#                     gc += 1 # green commute
#                 elif highest_tw_w < highest_tw_n:
#                     other += 1 # other (less healthy/green switch)
#                 elif highest_tw_w == 1:
#                     cc += 1 # car commute

#                 if tw_w_mode and tw_n_mode and fw_w_mode and fw_n_mode:
#                     breakdown[fw_w_mode][fw_n_mode] += 1
#                     breakdown[tw_w_mode][tw_n_mode] += 1

#                 highest_fw_w = 0
#                 highest_tw_w = 0
#                 highest_fw_n = 0
#                 highest_tw_n = 0

#             if survey[1] == 'fw' and survey[2] == 'n' and survey[4] > highest_fw_n:
#                 highest_fw_n = survey[4]
#                 fw_n_mode = survey[3]
#             elif survey[1] == 'tw' and survey[2] == 'n' and survey[4] > highest_tw_n:
#                 highest_tw_n = survey[4]
#                 tw_n_mode = survey[3]
#             elif survey[1] == 'fw' and survey[2] == 'w' and survey[4] > highest_fw_w:
#                 highest_fw_w = survey[4]
#                 fw_w_mode = survey[3]
#             elif survey[1] == 'tw' and survey[2] == 'w' and survey[4] > highest_tw_w:
#                 highest_tw_w = survey[4]
#                 tw_w_mode = survey[3]


#             lastid = survey[0]
#             i += 1

#     breakdown['gs'] = gs
#     breakdown['gc'] = gc
#     breakdown['us'] = other
#     breakdown['cc'] = cc

#     modes = ['da','dalt','cp','w','b','r','t','o','tc']

#     #workaround for the subteam parents
#     if Employer.objects.filter(id=emp.id,is_parent='t'):
#         #need to collect all the subteams to get right totals
#         parentname = Employer.objects.filter(id=emp.id).values('name')
#         childteams = Employer.objects.filter(sector__parent=parentname,active='t')
#         checkins = Commutersurvey.objects.filter(wr_day_month__gte=32, employer__in=childteams)
#     else:
#         checkins = Commutersurvey.objects.filter(wr_day_month__gte=32, employer_id=emp.id)

#     for m in modes:
#         breakdown[mode] = checkins.filter(leg__mode=m,leg__day__exact='w').distinct().count()

#     return breakdown

# # def makeChart():

# #     return month_breakdown


# # def getCanvasJSChart(emp, new=False):
# #     if new:
# #         chartData = getNvRcJSChartData(emp)
# #     else:
# #         chartData = getCanvasJSChartData(emp)
# #     barChart = {
# #             'title': {
# #                 'text': "Walk Ride Day Participation Over Time",
# #                 'fontSize': 20 },
# #             'data': chartData
# #             }
# #     if new:
# #         barChart['title']['text'] = "New And Returning Walk Ride Day Participation Over Time"
# #     return barChart

# # def getCanvasJSChartData(emp):
# #     chartData = [
# #             {
# #                 'type': "stackedColumn",
# #                 'color': '#aa0000',
# #                 'legendText': "Driving alone",
# #                 'showInLegend': "true",
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ]
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': '#ff0000',
# #                 'legendText': "Driving (alt)",
# #                 'showInLegend': "true",
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ]
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': '#ff5500',
# #                 'legendText': "Carpooling",
# #                 'showInLegend': "true",
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ]
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': '#00ff00',
# #                 'legendText': "Walking",
# #                 'showInLegend': "true",
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ]
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': '#00bb00',
# #                 'legendText': "Biking",
# #                 'showInLegend': "true",
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ]
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': '#009900',
# #                 'legendText': "Running/jogging",
# #                 'showInLegend': "true",
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ]
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': '#33cc33',
# #                 'legendText': "Public transit",
# #                 'showInLegend': "true",
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ]
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': '#aaaaaa',
# #                 'legendText': "Other",
# #                 'showInLegend': "true",
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ]
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': '#0000aa',
# #                 'legendText': "Telecommuting",
# #                 'showInLegend': "true",
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ]
# #                 }

# #             ]

# #     modes = [ 'da', 'dalt', 'cp', 'w', 'b', 'r', 't', 'o', 'tc' ]
# #     # intToModeConversion = ['gs', 'gc', 'cc', 'us' ]
# #     # iTMSConv = ['Green Switches','Green Commutes', 'Car Commutes', 'Other', 'Healthy Switch', 'Healthy Commute']
# #     for m in Month.objects.active_months().reverse():
# #         breakDown = getBreakDown(emp, m.id)
# #         for i in range(0, 4):
# #             chartData[i]['dataPoints'] += [{ 'label': modes[i], 'y': breakDown[modes[i]], 'name': modes[i] },]

# #     return chartData

# # def getNvRcJSChartData(emp):
# #     chartData = [
# #             {
# #                 'type': "stackedColumn",
# #                 'color': COLOR_SCHEME['ngs'],
# #                 'legendText': 'New Green Switches',
# #                 'showInLegend': 'true',
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ],
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': COLOR_SCHEME['rgs'],
# #                 'legendText': 'Returning Green Switches',
# #                 'showInLegend': 'true',
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ],
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': COLOR_SCHEME['ngc'],
# #                 'legendText': 'New Green Commutes',
# #                 'showInLegend': 'true',
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ],
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': COLOR_SCHEME['rgc'],
# #                 'legendText': 'Returning Green Commutes',
# #                 'showInLegend': 'true',
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ],
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': COLOR_SCHEME['ncc'],
# #                 'legendText': 'New Car Commutes',
# #                 'showInLegend': 'true',
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ],
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': COLOR_SCHEME['rcc'],
# #                 'legendText': 'Returning Car Commutes',
# #                 'showInLegend': 'true',
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ],
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': COLOR_SCHEME['nus'],
# #                 'legendText': 'New Other Commutes',
# #                 'showInLegend': 'true',
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ],
# #                 },
# #             {
# #                 'type': "stackedColumn",
# #                 'color': COLOR_SCHEME['rus'],
# #                 'legendText': 'Returning Other Commutes',
# #                 'showInLegend': 'true',
# #                 'toolTipContent': '{name}: {y}',
# #                 'dataPoints': [
# #                     ],
# #                 },
# #             ]
# #     intToModeConversion = ['ngs', 'rgs', 'ngc', 'rgc', 'ncc', 'rcc', 'nus', 'rus']
# #     iTMSConv = ['New Green Switches', 'Returning Green Switches', 'New Green Commutes', 'Returning Green Commutes', 'New Car Commutes', 'Returning Car Commutes', 'New Other', 'Returning Other']
# #     for month in reversed(Month.objects.active_months_list()):
# #         breakDown = getNewVOldBD(emp, month)
# #         for i in range(0, 8):
# #             chartData[i]['dataPoints'] += [{ 'label': str(month), 'y': breakDown[intToModeConversion[i]], 'name': str(iTMSConv[i]) },]
# #     return chartData



# # def leaderboard_bare(request, vol_v_perc='all', month='all', svs='all', sos='1', focusEmployer=None):
# #     context = leaderboard_context(request, vol_v_perc, month, svs, sos, focusEmployer)
# #     return render(request, 'leaderboard/leaderboard_bare.html', context)

# # def testchart(request):
# #     context = { 'CHART_DATA': getCanvasJSChart(Employer.objects.get(name="Dana-Farber Cancer Institute")) }
# #     return render(request, 'leaderboard/testchart.html', context)


# # def nvobreakdown(request, selEmpID=None):
# #     if selEmpID is None:
# #         context = {'emps': Employer.objects.all()}
# #         return render(request, 'leaderboard/chooseEmp.html', context)
# #     else:
# #         selEmp = Employer.objects.get(id=selEmpID)
# #         context = {'CHART_DATA': getCanvasJSChart(selEmp, new=True), 'emp': selEmp}
# #         return render(request, 'leaderboard/nvobreakdown.html', context)
