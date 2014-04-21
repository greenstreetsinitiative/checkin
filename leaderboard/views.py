# Create your views here.
from survey.models import Commutersurvey, Employer, EmplSector, Leg, Month
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from operator import itemgetter, attrgetter
import json
from django.shortcuts import redirect

COLOR_SCHEME = {
        'gs': '#0096FF',
        'gc': '#65AB4B',
        'cc': '#FF2600',
        'us': '#9437FF',
        'rgs': '#0096FF',
        'rgc': '#65AB4B',
        'rcc': '#FF2600',
        'rus': '#9437FF',
        'ngs': '#00C8FF',
        'ngc': '#75FF57',
        'ncc': '#FF266E',
        'nus': '#9496FF',
        }

def index(request):
    latest_check_ins = Commutersurvey.objects.order_by('month')[:5]
    reply_data = leaderboard_reply_data('perc', month, 'sector', '2');
    context = {'latest_check_ins' : latest_check_ins, 'reply_data' : reply_data }
    return render(request, 'leaderboard/index.html', context)

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
#    context = leaderboard_reply_data('perc', month, filter_by, _filter);
    context = {}
    context['empid'] = empid
 
    if _filter == '0':
        _filter = 0
   
    if empid != 0:
        res = Employer.objects.filter(id=empid)
        emp = res[0]
        sector = emp.sector
    if empid != 0 and _filter == 0:
        _filter = sector

    context['filter_by'] = filter_by
    context['filt'] = _filter
    if filter_by == 'sector':
        context['sectorid'] = _filter
    context['sort'] = sort
    context['sectors'] = sorted(EmplSector.objects.all(), key=getSectorNum)
    context['subteams'] = get_subteams()
    months = Month.objects.active_months()
    context['months'] = months
    for m in months:
        if m.url_month == selmonth:
            month = m.month
    if selmonth == 'all':
        global nmonths
        month = 'all'
        nmonths = len(months)

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
    if selmonth == 'all':
        context['display_month'] = "all months"
    else:
        context['display_month'] = month
    if sort == 'gs':
        context['ranks'] = green_switch_rankings(month, filter_by, _filter)
        context['ranks_pct'] = rankings_by_pct(month, filter_by, _filter)
    elif sort == 'gc':
        context['ranks'] = gc_rankings(month, filter_by, _filter)
        context['ranks_pct'] = gc_by_pct(month, filter_by, _filter)
    else:
        context['ranks'] = participation_rankings(month, filter_by, _filter)
        context['ranks_pct'] = participation_pct(month, filter_by, _filter)

    context['total_companies'] = len(context['ranks_pct'])
    context['total'] = 0
    for rank in context['ranks']:
        context['total'] += rank['val']
    
    if _filter == 0:
        context['emp_sector'] = 'all sectors'
    elif filter_by == 'sector' and empid == 0:
        sector = EmplSector.objects.filter(id=_filter)
        context['emp_sector'] = sector[0]
    if empid != 0:
        context['chart'] = json.dumps(getCanvasJSChart(emp) )
        emp_stats = getBreakDown(emp, month)
        nsurveys = len(get_lb_surveys(emp, month) )
        try: 
            context['participation'] = ( float(nsurveys) / (float(emp.nr_employees)*nmonths) ) * 100
        except TypeError, ZeroDivisionError:
            context['participation'] = 0
        context['ncommutes'] = nsurveys*2
        context['gc'] = emp_stats['gc']
        context['gs'] = emp_stats['gs']
        context['cc'] = emp_stats['cc']
        context['other'] = emp_stats['us']
        if nsurveys != 0:
            context['gc_pct'] = ( ( emp_stats['gc']*1.0) / (nsurveys*2.0) ) * 100
            context['gs_pct'] = ( ( emp_stats['gs']*1.0) / (nsurveys*2.0) ) * 100
        else:
            context['gs_pct'] = 0
            context['gc_pct'] = 0
        context['stats'] = emp_stats
        context['employer'] = emp
        context['emp_sector'] = emp.sector
        context['sectorid'] = emp.sector.id
        context['m'] = getEmpCheckinMatrix(emp, month)
        
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

def getTopCompanies(vvp, month, svs, sos):
    emps = Employer.objects.filter(sector__in=EmplSector.objects.filter(parent=None))
    if svs == 'size':
        emps = emps.filter(size_cat=sos)
    elif svs == 'sector':
        sector = EmplSector.objects.get(pk=sos)
        if sector.parent != None:
            emps = Employer.objects.filter(sector=sos)
        else:
            emps = emps.filter(sector=sos)
    elif svs == 'name':
        nameList = []
        for emp in sorted(emps, key=attrgetter('name')):
            nameList += [(emp.name, 0, 0, emp.nr_employees),]
        return nameList
    companyList = []
    if vvp == 'perc':
        for company in emps:
            try:
                percent = (100 * float(company.get_nr_surveys(month))/float(company.nr_employees))
                if month == 'all':
                    percent /= Month.objects.active_months().count()
                companyList += [(company.name, percent, ('%.1f' % percent), company.nr_employees),]
            except TypeError:
                pass
    else:
        for company in emps:
            nr_surveys = company.get_nr_surveys(month)
            companyList += [(company.name, nr_surveys, str(nr_surveys), company.nr_employees),]
    topEmps = sorted(companyList, key=itemgetter(1), reverse=True)
    return topEmps

def getEmpCheckinMatrix(emp, month):

    checkinMatrix = {}
    modes = [ 'c', 'cp', 'dalt', 'w', 'b', 'r', 't', 'o', 'tc' ]
    for mode in modes:
        checkinMatrix[mode] = {}
        for mode2 in modes:
            checkinMatrix[mode][mode2] = 0

    empCommutes = get_lb_surveys(emp, month)
    for emp in empCommutes:
        if from_work_normally(emp) and from_work_today(emp) and to_work_normally(emp) and to_work_today(emp):
            checkinMatrix[from_work_today(emp)][from_work_normally(emp)] += 1
            checkinMatrix[to_work_today(emp)][to_work_normally(emp)] += 1
    return checkinMatrix

def participation_rankings(month, filter_by, _filter=0):
    rank = []
    pct = 0.0
    participation = 0.0
    if _filter == 0 and filter_by == 'sector':
        employers = Employer.objects.filter(active=True)
    elif filter_by == 'sector':
        employers = Employer.objects.filter(sector=_filter, active=True)

    if _filter == 0 and filter_by == 'size':
        employers = Employer.objects.filter(active=True)
    elif filter_by == 'size':
        employers = Employer.objects.filter(size_cat=_filter, active=True)

    for emp in employers:
        nsurveys = emp.get_surveys(month=month).count()
        rank.append({'val': nsurveys, 'name': emp.name, 'id': emp.id })
    
    return sorted(rank, key=lambda idx: idx['val'], reverse=True);

def participation_pct(month, filter_by, _filter=0):
    rank = []
    pct = 0.0
    participation = 0.0
    if _filter == 0 and filter_by == 'sector':
        employers = Employer.objects.filter(active=True)
    elif filter_by == 'sector':
        employers = Employer.objects.filter(sector=_filter, active=True)

    if _filter == 0 and filter_by == 'size':
        employers = Employer.objects.filter(active=True)
    elif filter_by == 'size':
        employers = Employer.objects.filter(size_cat=_filter, active=True)

    for emp in employers:
        nsurveys = emp.get_surveys(month=month).count()
        if not emp.nr_employees:
            continue
        participation = ( (nsurveys*1.0) / (emp.nr_employees*1.0*nmonths) ) * 100
        rank.append({'pct': participation, 'name': emp.name, 'id': emp.id })
    
    return sorted(rank, key=lambda idx: idx['pct'], reverse=True);


def rankings_by_pct(month, filter_by, _filter=0):
    rank = []
    pct = 0.0
    if _filter == 0 and filter_by == 'sector':
        employers = Employer.objects.filter(active=True)
    elif filter_by == 'sector':
        employers = Employer.objects.filter(sector=_filter, active=True)

    if _filter == 0 and filter_by == 'size':
        employers = Employer.objects.filter(active=True)
    elif filter_by == 'size':
        employers = Employer.objects.filter(size_cat=_filter, active=True)

    for emp in employers:
        breakdown = getBreakDown(emp, month)
        total = Employer.get_nr_surveys(emp, month)
        if total == 0:
            pct = 0
        else:
            pct = ( (breakdown['gs']*1.0) / (total*2.0) ) * 100
        rank.append({'pct' : pct, 'name' : emp.name, 'id' : emp.id })

    return sorted(rank, key=lambda idx: idx['pct'], reverse=True);


def green_switch_rankings(month, filter_by, _filter=0):

    rank = []
    if filter_by == 'sector' and _filter == 0:
        employers = Employer.objects.filter(active=True)
    elif filter_by == 'sector':
        employers = Employer.objects.filter(sector=_filter, active=True)
    
    if filter_by == 'size' and _filter == 0:
        employers = Employer.objects.filter(active=True)
    elif filter_by == 'size':
        employers = Employer.objects.filter(size_cat=_filter, active=True)

    for emp in employers:
        breakdown = getBreakDown(emp, month)
        rank.append({'val' : breakdown['gs'], 'name' : emp.name, 'id' : emp.id })

    return sorted(rank, key=lambda idx: idx['val'], reverse=True);

def gc_by_pct(month, filter_by, _filter=0):
    rank = []
    pct = 0.0
    if _filter == 0 and filter_by == 'sector':
        employers = Employer.objects.filter(active=True)
    elif filter_by == 'sector':
        employers = Employer.objects.filter(sector=_filter, active=True)

    if _filter == 0 and filter_by == 'size':
        employers = Employer.objects.filter(active=True)
    elif filter_by == 'size':
        employers = Employer.objects.filter(size_cat=_filter, active=True)

    for emp in employers:
        breakdown = getBreakDown(emp, month)
        total = Employer.get_nr_surveys(emp, month)
        if total == 0:
            pct = 0
        else:
            pct = ( (breakdown['gc']*1.0) / (total*2.0) ) * 100
        rank.append({'pct' : pct, 'name' : emp.name, 'id' : emp.id })

    return sorted(rank, key=lambda idx: idx['pct'], reverse=True);


def gc_rankings(month, filter_by, _filter=0):

    rank = []
    if filter_by == 'sector' and _filter == 0:
        employers = Employer.objects.filter(active=True)
    elif filter_by == 'sector':
        employers = Employer.objects.filter(sector=_filter, active=True)
    
    if filter_by == 'size' and _filter == 0:
        employers = Employer.objects.filter(active=True)
    elif filter_by == 'size':
        employers = Employer.objects.filter(size_cat=_filter, active=True)

    for emp in employers:
        breakdown = getBreakDown(emp, month)
        rank.append({'val' : breakdown['gc'], 'name' : emp.name, 'id' : emp.id })

    return sorted(rank, key=lambda idx: idx['val'], reverse=True);

breakdown = {}
surveys_cache = {}

def get_lb_surveys(emp, month):
    global surveys_cache
    surveys = []

    sectorEmps = Employer.objects.filter(sector=EmplSector.objects.get(parent=emp.name))
    if emp.name not in surveys_cache:
        if emp.is_parent:
            surveys_cache[emp.name] = Commutersurvey.objects.prefetch_related("leg_set").filter(employer__in=sectorEmps, wr_day_month__in=Month.objects.filter(active='t') )
        else:
            surveys_cache[emp.name] = Commutersurvey.objects.prefetch_related("leg_set").filter(employer=emp, wr_day_month__in=Month.objects.filter(active='t') )
    if month == 'all':
        return surveys_cache[emp.name]
    for survey in surveys_cache[emp.name]:
        if survey.wr_day_month.month == month:
            surveys.append(survey)
    return surveys

def getBreakDown(emp, bd_month):
    global breakdown
    if emp.name + bd_month in breakdown:
        return breakdown[emp.name, bd_month.month]

    empSurveys = get_lb_surveys(emp, bd_month)
    unhealthySwitches = 0
    carCommuters = 0
    greenCommuters = 0
    greenSwitches = 0
    newUS = 0
    newCC = 0
    newGC = 0
    newGS = 0
    for survey in empSurveys:
        #if survey.email not i
        to_code = survey.to_work_switch
        from_code = survey.from_work_switch
        if to_code == 1:
            unhealthySwitches += 1
        elif to_code == 2:
            carCommuters += 1
        elif to_code == 3:
            greenCommuters += 1
        elif to_code == 4:
            greenSwitches += 1
        if from_code == 1:
            unhealthySwitches += 1
        elif from_code == 2:
            carCommuters += 1
        elif from_code == 3:
            greenCommuters += 1
        elif from_code == 4:
            greenSwitches += 1

    breakdown[emp.name, bd_month] = { 'us': unhealthySwitches, 'cc': carCommuters, 'gc': greenCommuters, 'gs': greenSwitches, 'total':(len(empSurveys)*2) }

    return { 'us': unhealthySwitches, 'cc': carCommuters, 'gc': greenCommuters, 'gs': greenSwitches, 'total':(len(empSurveys)*2) }

def getNewVOldBD(emp, month):
    nvoBD = {'nus':0, 'ncc':0, 'ngc':0, 'ngs':0, 'rus':0, 'rcc':0, 'rgc':0, 'rgs':0, 'ntotal':0, 'rtotal':0} # new vs. old breakdown
    for survey in emp.get_new_surveys(month):
        tws = survey.to_work_switch
        fws = survey.from_work_switch
        if tws == 1: nvoBD['nus'] += 1
        elif tws == 2: nvoBD['ncc'] += 1
        elif tws == 3: nvoBD['ngc'] += 1
        elif tws == 4: nvoBD['ngs'] += 1
        elif fws == 2: nvoBD['ncc'] += 1
        elif fws == 3: nvoBD['ngc'] += 1
        elif fws == 4: nvoBD['ngs'] += 1
    for survey in emp.get_returning_surveys(month):
        tws = survey.to_work_switch
        fws = survey.from_work_switch
        if tws == 1: nvoBD['rus'] += 1
        elif tws == 2: nvoBD['rcc'] += 1
        elif tws == 3: nvoBD['rgc'] += 1
        elif tws == 4: nvoBD['rgs'] += 1
        if fws == 1: nvoBD['rus'] += 1
        elif fws == 2: nvoBD['rcc'] += 1
        elif fws == 3: nvoBD['rgc'] += 1
        elif fws == 4: nvoBD['rgs'] += 1
    nvoBD['ntotal'] = nvoBD['nus'] + nvoBD['ncc'] + nvoBD['ngc'] + nvoBD['ngs']
    nvoBD['rtotal'] = nvoBD['rus'] + nvoBD['rcc'] + nvoBD['rgc'] + nvoBD['rgs']
    return nvoBD

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
    intToModeConversion = ['gs', 'gc', 'cc', 'us']
    iTMSConv = ['Green Switches','Green Commutes', 'Car Commutes', 'Other']
    for m in Month.objects.active_months():
        breakDown = getBreakDown(emp, m.month)
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

def leaderboard_nvo_data(empName):
    emp = Employer.objects.get(name__exact=empName)
    return getCanvasJSChart(emp, new=True)

def leaderboard_reply_data(vol_v_perc, month, svs, sos, focusEmployer=None):
    topEmps = getTopCompanies(vol_v_perc, month, svs, sos)

    if focusEmployer is None and len(topEmps) > 0:
        focusEmployer = topEmps[0]
        emp = Employer.objects.get(name=focusEmployer[0])
    elif type(focusEmployer) is str:
        emp = Employer.objects.get(name=focusEmployer)
    elif type(focusEmployer) is Employer:
        emp = focusEmployer
    reply_data = {
            'chart_data': getCanvasJSChart(emp),
            'top_companies': topEmps,
            'checkin_matrix': getEmpCheckinMatrix(emp),
            'total_breakdown': getBreakDown(emp, "all"),
            'vol_v_perc': vol_v_perc,
            'month': month,
            'svs': svs,
            'sos': sos,
            'emp_sector': emp.sector.name,
            }
    if emp.size_cat is not None:
        reply_data['emp_size_cat'] = emp.size_cat.name
    return reply_data

def leaderboard_company_detail(empName):
    emp = Employer.objects.get(name=empName)
    reply_data = {
            'chart_data': getCanvasJSChart(emp),
            'checkin_matrix': getEmpCheckinMatrix(emp),
            'total_breakdown': getBreakDown(emp, "all"),
            'emp_sector': emp.sector.name,
            }
    if emp.size_cat is not None:
        reply_data['emp_size_cat'] = emp.size_cat.name
    return reply_data

def leaderboard_context():
    context = {
            'sectors': sorted(EmplSector.objects.all(), key=getSectorNum),
            'months': Month.objects.filter(active=True).order_by('-id'),
            }
    return context

def leaderboard(request):
    emps = Employer.objects.all()
    if request.method == "POST":
        if request.POST['just_emp'] == 'false':
            reply_data = leaderboard_reply_data(request.POST['selVVP'], request.POST['selMonth'], request.POST['selSVS'], request.POST['selSOS'],)
        elif request.POST['just_emp'] == 'true':
            reply_data = leaderboard_company_detail(request.POST['focusEmployer'])
        response = HttpResponse(json.dumps(reply_data), content_type='application/json')
        return response
    else:
        context = leaderboard_context()
        return render(request, 'leaderboard/leaderboard_js.html', context)

def leaderboard_bare(request, vol_v_perc='all', month='all', svs='all', sos='1', focusEmployer=None):
    context = leaderboard_context(request, vol_v_perc, month, svs, sos, focusEmployer)
    return render(request, 'leaderboard/leaderboard_bare.html', context)

def testchart(request):
    context = { 'CHART_DATA': getCanvasJSChart(Employer.objects.get(name="Dana-Farber Cancer Institute")) }
    return render(request, 'leaderboard/testchart.html', context)

def from_work_normally(survey):
    longest_dur = 0
    longest_mode = ''
    for leg in survey.legs:
        if not leg.duration and leg.day == 'n' and leg.direction == 'fw':
            longest_mode = leg.mode
        elif leg.duration > longest_dur and leg.day == 'n' and leg.direction == 'fw':
            longest_dur = leg.duration
            longest_mode = leg.mode
    if longest_mode == 'da':
        longest_mode == 'c'

    return longest_mode

def to_work_normally(survey):
    longest_dur = 0
    longest_mode = ''
    for leg in survey.legs:
        if not leg.duration and leg.day == 'n' and leg.direction == 'tw':
            longest_mode = leg.mode
        elif leg.duration > longest_dur and leg.day == 'n' and leg.direction == 'tw':
            longest_dur = leg.duration
            longest_mode = leg.mode
    if longest_mode == 'da':
        longest_mode == 'c'
    return longest_mode
   
def from_work_today(survey):
    longest_dur = 0
    longest_mode = ''
    for leg in survey.legs:
        if not leg.duration and leg.day == 'w' and leg.direction == 'fw':
            longest_mode = leg.mode
        elif leg.duration > longest_dur and leg.day == 'w' and leg.direction == 'fw':
            longest_dur = leg.duration
            longest_mode = leg.mode
    
    if longest_mode == 'da':
        longest_mode == 'c'

    return longest_mode

def to_work_today(survey):
    longest_dur = 0
    longest_mode = ''
    for leg in survey.legs:
        if not leg.duration and leg.day == 'w' and leg.direction == 'tw':
            longest_mode = leg.mode
        elif leg.duration > longest_dur and leg.day == 'w' and leg.direction == 'tw':
            longest_dur = leg.duration
            longest_mode = leg.mode
    if longest_mode == 'da':
        longest_mode == 'c'

    return longest_mode

def numNewCheckins(company, month1, month2):
    month1Checkins = Commutersurvey.objects.filter(employer=company, month=month1)
    month2Checkins = Commutersurvey.objects.filter(employer=company, month=month2)
    month1emails = []
    newCount = 0
    for checkin in month1Checkins:
        month1emails += checkin.email
    for checkin in month2Checkins:
        if checkin.email not in month1emails:
            newCount += 1
            month1emails += checkin.email
    return str(round(((newCount*1.0)/(len(month1emails)*1.0))*100, 2)) + "%"

def nvobreakdown(request, selEmpID=None):
    if selEmpID is None:
        context = {'emps': Employer.objects.all()}
        return render(request, 'leaderboard/chooseEmp.html', context)
    else:
        selEmp = Employer.objects.get(id=selEmpID)
        context = {'CHART_DATA': getCanvasJSChart(selEmp, new=True), 'emp': selEmp}
        return render(request, 'leaderboard/nvobreakdown.html', context)
