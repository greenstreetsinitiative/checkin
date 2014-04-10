# Create your views here.
from survey.models import Employer, Commutersurvey, Month
from leaderboard.views import getBreakDown
from django.shortcuts import render
import json

def getCJSEmplList(month):
    chart = {
        'title': { 'text': 'Alphabetical Employer Breakdown for %s' % (month,), 'fontSize': 20 },
        'creditText': 'gogreenstreets.org',
        'creditHref': 'http://gogreenstreets.org',
        'axisX': {
            'labelFontSize': 12,
            'margin': 0,
        },
        'axisY': {
            'labelFontSize': 12,
        },
        'legend': {
            'fontSize': 12,
        },
        'data': [
            {
                'type': 'stackedBar',
                'color': '#0096FF',
                'legendText': 'Green Switches',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y} ({perc}%)',
                'dataPoints': [
                ]
            },
            {
                'type': 'stackedBar',
                'color': '#65AB4B',
                'legendText': 'Green Commutes',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y} ({perc}%)',
                'dataPoints': [
                ]
            },
            {
                'type': 'stackedBar',
                'color': '#FF2600',
                'legendText': 'Car Commutes',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y} ({perc}%)',
                'dataPoints': [
                ]
            },
            {
                'type': 'stackedBar',
                'color': '#9437FF',
                'legendText': 'Other',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y} ({perc}%)',
                'dataPoints': [
                ]
            },
        ]
    }
    breakDownTranslator = [ 'gs', 'gc', 'cc', 'us' ]
    longBDT = [ 'Green Switches', 'Green Commutes', 'Car Commutes', 'Other' ]
    for emp in Employer.objects.filter(active=True).reverse():
        breakDown = getBreakDown(emp, month)
        for i in range(0, 4):
            y = breakDown[breakDownTranslator[i]]
            print breakDown['total']
            if breakDown['total'] != 0:
                perc = "%.1f" % (100*(float(y)/float(breakDown['total'])),)
            else:
                perc = "0"
            chart['data'][i]['dataPoints'] += [{ 'label': emp.name, 'name': longBDT[i], 'y': y, 'perc': perc },]
    return json.dumps(chart)

def empBreakDown(request, month):
    fullMonth = Month.objects.get(url_month=month)
    context = { 'month': month, 'CHART_DATA': getCJSEmplList(fullMonth.month) }
    return render(request, 'leaderboardlist/leaderboardlist.html', context)
    
def chooseMonth(request):
    months = Month.active_months.values_list('month', flat=True)
    context = { 'months': months }
    return render(request, 'leaderboardlist/chooseMonths.html', context)
