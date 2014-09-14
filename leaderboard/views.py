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
import graphos
from graphos import *
# from graphos.sources.model import ModelDataSource
# from graphos.renderers import gchart
from graphos.sources.model import *
from graphos.renderers import *
from django.db.models import Count

# queryset = Commutersurvey.objects.filter(wr_day_month__gte=32).filter(employer_id=1905) #dana farber in April
# # queryset = Commutersurvey.objects.filter(wr_day_month__gte=32).filter(employer_id=1905).values('wr_day_month').annotate(total=Count('wr_day_month')).order_by('-wr_day_month')
# data_source = ModelDataSource(queryset, fields=['wr_day_month','employer_id'])

# # chart = gchart.LineChart(data_source)

# Chart = LineChart(SimpleDataSource(data=data_data_source), html_id="line_chart")

data =  [
        ['Year', 'Sales', 'Expenses'],
        [2004, 1000, 400],
        [2005, 1170, 460],
        [2006, 660, 1120],
        [2007, 1030, 540]
    ]
Chart = LineChart(SimpleDataSource(data=data), html_id="line_chart")


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
        return redirect("/leaderboard/", permanent=True)
    url = "/leaderboard/"
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
    months = Month.objects.active_months().reverse().exclude(open_checkin__gt=date.today() )
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
        context['chart'] = json.dumps(getCanvasJSChart(emp) )
        stats_month = getBreakDown(emp, month)
        stats_all = stats_month
        if month != 'all':
            stats_all = getBreakDown(emp, 'all')
        for count in context['ranks']:
            if count[2] == int(empid):
                nsurveys = count[0]
        for count in context['ranks_pct']:
            if count[2] == int(empid):
                context['participation'] = count[0]

        context['ncommutes'] = nsurveys*2
        context['gc'] = stats_month['gc']
        context['gs'] = stats_month['gs']

        context['gs_total'] = stats_all['gs']
        context['gc_total'] = stats_all['gc']
        context['cc_total'] = stats_all['cc']
        context['other_total'] = stats_all['us']
        context['ncommutes_total'] = stats_all['total']

        if nsurveys != 0:
            context['gc_pct'] = ( ( stats_month['gc']*1.0) / (nsurveys*2.0) ) * 100
            context['gs_pct'] = ( ( stats_month['gs']*1.0) / (nsurveys*2.0) ) * 100
        else:
            context['gs_pct'] = 0
            context['gc_pct'] = 0
        context['stats'] = stats_month
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


def getBreakDown(emp, month):
    hs = 0
    hc = 0
    gs = 0
    gc = 0
    cc = 0
    other = 0

    # tw = from work, fw = from work, n/w normal day or WR day
    highest_fw_n = 0
    highest_fw_w = 0
    highest_tw_n = 0
    highest_tw_w = 0

    tw_w_mode = ''
    tw_n_mode = ''
    fw_w_mode = ''
    fw_n_mode = ''

    db = connections['default'].cursor()
    args = []
    if emp.is_parent == True:
        eid = " employer_id in (select id from survey_employer where sector_id in (select id from survey_emplsector where parent = %s) ) "
        args.append(emp.name)
    else:
        eid = " employer_id = %s "
        args.append(emp.id)

    if month == 'all':
        monthq = " wr_day_month_id in (select id from survey_month where active = %s) "
        args.append('t')
    else:
        monthq = " wr_day_month_id = %s "
        args.append(month)

    db.execute("select commutersurvey_id, direction, day,  mode, case when mode in ('b', 'r', 'w', 'o') then 5 when mode = 'tc' then 4 when mode = 't' then 3 when mode = 'cp' then 2 when mode in ('c', 'da') then 1 end as rank, wr_day_month_id from survey_leg join survey_commutersurvey cs on (commutersurvey_id = cs.id) where " + eid + " and " + monthq + " order by commutersurvey_id", args);
    surveys = db.fetchall()

    breakdown = {}
    modes = [ 'c', 'cp', 'da', 'dalt', 'w', 'b', 'r', 't', 'o', 'tc' ]
    for mode in modes:
        breakdown[mode] = {}
        for mode2 in modes:
            breakdown[mode][mode2] = 0
    breakdown['total'] = 0

    i = 1
    if len(surveys) != 0:
        lastid = surveys[0][0]
        for survey in surveys:
            if survey[0] != lastid or i == len(surveys):
                breakdown['total'] += 2
                if highest_fw_w > highest_fw_n and highest_fw_w == 5:
                    gs += 1 # formerly healthy switch, now green
                elif highest_fw_w == 5:
                    gc += 1 # formerly healthy commute, now green
                elif highest_fw_w > highest_fw_n:
                    gs += 1 # green switch
                elif highest_fw_w > 1:
                    gc += 1 # green commute
                elif highest_fw_w < highest_fw_n:
                    other += 1 # other (less healthy/green switch)
                elif highest_fw_w == 1:
                    cc += 1 # car commute
                
                if highest_tw_w > highest_tw_n and highest_tw_w == 5:
                    gs += 1 # former healthy switch
                elif highest_tw_w == 5:
                    gc += 1 # former healthy commute
                elif highest_tw_w > highest_tw_n:
                    gs += 1 # green switch
                elif highest_tw_w > 1:
                    gc += 1 # green commute
                elif highest_tw_w < highest_tw_n:
                    other += 1 # other (less healthy/green switch)
                elif highest_tw_w == 1:
                    cc += 1 # car commute

                if tw_w_mode and tw_n_mode and fw_w_mode and fw_n_mode:
                    breakdown[fw_w_mode][fw_n_mode] += 1
                    breakdown[tw_w_mode][tw_n_mode] += 1

                highest_fw_w = 0
                highest_tw_w = 0
                highest_fw_n = 0
                highest_tw_n = 0

            if survey[1] == 'fw' and survey[2] == 'n' and survey[4] > highest_fw_n:
                highest_fw_n = survey[4]
                fw_n_mode = survey[3]
            elif survey[1] == 'tw' and survey[2] == 'n' and survey[4] > highest_tw_n:
                highest_tw_n = survey[4]
                tw_n_mode = survey[3]
            elif survey[1] == 'fw' and survey[2] == 'w' and survey[4] > highest_fw_w:
                highest_fw_w = survey[4]
                fw_w_mode = survey[3]
            elif survey[1] == 'tw' and survey[2] == 'w' and survey[4] > highest_tw_w:
                highest_tw_w = survey[4]
                tw_w_mode = survey[3]


            lastid = survey[0]
            i += 1

    breakdown['gs'] = gs
    breakdown['gc'] = gc
    breakdown['us'] = other
    breakdown['cc'] = cc

    return breakdown



def getCanvasJSChart(emp, new=False):
    if new:
        chartData = getNvRcJSChartData(emp)
    else:
        chartData = getCanvasJSChartData(emp)
    barChart = {
            'title': {
                'text': "Walk Ride Day Participation Over Time",
                'fontSize': 20 },
            'data': chartData
            }
    if new:
        barChart['title']['text'] = "New And Returning Walk Ride Day Participation Over Time"
    return barChart

def getCanvasJSChartData(emp):
    chartData = [
            {
                'type': "stackedColumn",
                'color': COLOR_SCHEME['gs'],
                'legendText': "Green Switches",
                'showInLegend': "true",
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                    ]
                },
            {
                'type': "stackedColumn",
                'color': COLOR_SCHEME['gc'],
                'legendText': "Green Commutes",
                'showInLegend': "true",
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                    ]
                },
            {
                'type': "stackedColumn",
                'color': COLOR_SCHEME['cc'],
                'legendText': "Car Commutes",
                'showInLegend': "true",
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                    ]
                },
            {
                'type': "stackedColumn",
                'color': COLOR_SCHEME['us'],
                'legendText': "Other",
                'showInLegend': "true",
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                    ]
                }
            
            ]
    intToModeConversion = ['gs', 'gc', 'cc', 'us' ]
    iTMSConv = ['Green Switches','Green Commutes', 'Car Commutes', 'Other', 'Healthy Switch', 'Healthy Commute']
    for m in Month.objects.active_months().reverse():
        breakDown = getBreakDown(emp, m.id)
        for i in range(0, 4):
            chartData[i]['dataPoints'] += [{ 'label': m.short_name, 'y': breakDown[intToModeConversion[i]], 'name': iTMSConv[i] },]
    return chartData

def getNvRcJSChartData(emp):
    chartData = [
            {
                'type': "stackedColumn",
                'color': COLOR_SCHEME['ngs'],
                'legendText': 'New Green Switches',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                    ],
                },
            {
                'type': "stackedColumn",
                'color': COLOR_SCHEME['rgs'],
                'legendText': 'Returning Green Switches',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                    ],
                },
            {
                'type': "stackedColumn",
                'color': COLOR_SCHEME['ngc'],
                'legendText': 'New Green Commutes',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                    ],
                },
            {
                'type': "stackedColumn",
                'color': COLOR_SCHEME['rgc'],
                'legendText': 'Returning Green Commutes',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                    ],
                },
            {
                'type': "stackedColumn",
                'color': COLOR_SCHEME['ncc'],
                'legendText': 'New Car Commutes',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                    ],
                },
            {
                'type': "stackedColumn",
                'color': COLOR_SCHEME['rcc'],
                'legendText': 'Returning Car Commutes',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                    ],
                },
            {
                'type': "stackedColumn",
                'color': COLOR_SCHEME['nus'],
                'legendText': 'New Other Commutes',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                    ],
                },
            {
                'type': "stackedColumn",
                'color': COLOR_SCHEME['rus'],
                'legendText': 'Returning Other Commutes',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                    ],
                },
            ]
    intToModeConversion = ['ngs', 'rgs', 'ngc', 'rgc', 'ncc', 'rcc', 'nus', 'rus']
    iTMSConv = ['New Green Switches', 'Returning Green Switches', 'New Green Commutes', 'Returning Green Commutes', 'New Car Commutes', 'Returning Car Commutes', 'New Other', 'Returning Other']
    for month in reversed(Month.objects.active_months_list()):
        breakDown = getNewVOldBD(emp, month)
        for i in range(0, 8):
            chartData[i]['dataPoints'] += [{ 'label': str(month), 'y': breakDown[intToModeConversion[i]], 'name': str(iTMSConv[i]) },]
    return chartData



def leaderboard_bare(request, vol_v_perc='all', month='all', svs='all', sos='1', focusEmployer=None):
    context = leaderboard_context(request, vol_v_perc, month, svs, sos, focusEmployer)
    return render(request, 'leaderboard/leaderboard_bare.html', context)

def testchart(request):
    context = { 'CHART_DATA': getCanvasJSChart(Employer.objects.get(name="Dana-Farber Cancer Institute")) }
    return render(request, 'leaderboard/testchart.html', context)


def nvobreakdown(request, selEmpID=None):
    if selEmpID is None:
        context = {'emps': Employer.objects.all()}
        return render(request, 'leaderboard/chooseEmp.html', context)
    else:
        selEmp = Employer.objects.get(id=selEmpID)
        context = {'CHART_DATA': getCanvasJSChart(selEmp, new=True), 'emp': selEmp}
        return render(request, 'leaderboard/nvobreakdown.html', context)
