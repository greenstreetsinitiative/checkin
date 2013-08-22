# Create your views here.
from survey.models import Commutersurvey, Employer, EmplSector
from leaderboard.models import Month, getMonths
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from operator import itemgetter, attrgetter
import json

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
	context = {'latest_check_ins' : latest_check_ins}
	return render(request, 'leaderboard/index.html', context)

def getSectorNum(sector):
	if sector.name[1] == ' ':
		return int(sector.name[0])
	elif sector.name[2] == ' ':
		return int(sector.name[:2])
	else:
		return int(sector.name[:3])

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
					percent /= len(getMonths())
				companyList += [(company.name, percent, ('%.1f' % percent), company.nr_employees),]
			except TypeError:
				pass
	else:
		for company in emps:
			nr_surveys = company.get_nr_surveys(month)
			companyList += [(company.name, nr_surveys, str(nr_surveys), company.nr_employees),]
	topEmps = sorted(companyList, key=itemgetter(1), reverse=True)
	return topEmps

def getEmpCheckinMatrix(emp):
	commuterModes = ['c', 'cp', 'w', 'b', 't', 'tc', 'o']
	checkinMatrix = []
	todayPos = -1
	empCommutes = emp.get_surveys('all')
	for todayWM in commuterModes:
		todayPos += 1
		checkinMatrix += [[],]
		for normalWM in commuterModes:
			numTypeCommutes = empCommutes.filter(to_work_today=todayWM, to_work_normally=normalWM).count() + empCommutes.filter(from_work_today=todayWM, from_work_normally=normalWM).count()
			checkinMatrix[todayPos] += [numTypeCommutes,]
	return checkinMatrix

def getBreakDown(emp, month):
	empSurveys = emp.get_surveys(month)
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
		if survey.to_work_switch == 1:
			unhealthySwitches += 1
		elif survey.to_work_switch == 2:
			carCommuters += 1
		elif survey.to_work_switch == 3:
			greenCommuters += 1
		elif survey.to_work_switch == 4:
			greenSwitches += 1
		if survey.from_work_switch == 1:
			unhealthySwitches += 1
		elif survey.from_work_switch == 2:
			carCommuters += 1
		elif survey.from_work_switch == 3:
			greenCommuters += 1
		elif survey.from_work_switch == 4:
			greenSwitches += 1
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
	for month in Month.objects.filter(active=True).order_by('id'):
		breakDown = getBreakDown(emp, month.month)
		for i in range(0, 4):
			chartData[i]['dataPoints'] += [{ 'label': month.short_name, 'y': breakDown[intToModeConversion[i]], 'name': iTMSConv[i] },]
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
	for month in reversed(getMonths()):
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
			'months': Month.objects.filter(active=True),
			}
	return context

def leaderboard(request):
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

def whichSwitch(checkin): # 1=Unhealthy, 2=Car Commuter, 3=Green Commuter, 4=Green Switch
	"""returns a tuple of (to_work, from_work)"""
	if checkin.to_work_today == 'c': tw = 1
	else: tw = 3
	if checkin.to_work_normally == 'c': tw += 1
	if checkin.from_work_today == 'c': fw = 1
	else: fw = 3
	if checkin.from_work_normally == 'c': fw += 1
	return (tw, fw)

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
