
import csv
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from django.db.models import Sum, Count

from django.forms import ModelForm

from survey.models import Commutersurvey, Employer, EmplSector, EmplSizeCategory, Leg, Month
# from django.contrib import admin
from django.contrib.gis import admin
# disable deletion of records
admin.site.disable_action('delete_selected')

# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7915039
admin.GeoModelAdmin.default_lat = 5216500
admin.GeoModelAdmin.default_zoom = 12

def export_as_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.
    """

    if not request.user.is_staff:
        raise PermissionDenied

    opts = modeladmin.model._meta
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
    writer = csv.writer(response)
    
    field_names = [field.name for field in opts.fields]
    
    # Write a first row with header information
    writer.writerow(field_names)
    
    # Write data rows
    for obj in queryset:
        try:
            writer.writerow([getattr(obj, field) for field in field_names])
        except UnicodeEncodeError:
            print "Could not export data row."
    return response

export_as_csv.short_description = "Export selected rows as csv file"


class EmployerAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display_links = ['id']
    list_display = ['id', 'name', 'active', 'nr_employees', 'size_cat', 'sector', 'nr_surveys']
    list_editable = ['name', 'active', 'nr_employees', 'size_cat', 'sector', ]
    list_filter = ['size_cat', 'sector', 'active']
    actions = [export_as_csv]


class EmployerLookupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']
    actions = [export_as_csv]

class EmployerSectorAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'parent']
	list_editable = ['name', 'parent']
	actions = [export_as_csv]

class CommutersurveyAdmin(admin.OSMGeoAdmin):
    fieldsets = [
        (None, 
            {'fields': ['wr_day_month', 'name', 'email', 'employer', 'share', 'comments', ]}),
        ('Commute', 
            {'fields': ['home_address', 'work_address', 'from_work_switch', 'to_work_switch']}),
        ('Optional Questions', 
            {'fields': ['health', 'weight', 'height', 'gender', 'gender_other', 'outsidechanges', 'affectedyou', 'volunteer', 'cdays', 'caltdays', 'cpdays', 'tdays', 'bdays', 'rdays', 'wdays', 'odays', 'tcdays', 'lastweek', 'cdaysaway', 'caltdaysaway', 'cpdaysaway', 'tdaysaway', 'bdaysaway', 'rdaysaway', 'wdaysaway', 'odaysaway', 'tcdaysaway', ]}),
    ]
    list_display = ('id', 'wr_day_month', 'email', 'name', 'share', 'employer', 'from_work_switch', 'to_work_switch', 'home_address', 'work_address', )
    list_filter = ['wr_day_month', 'employer', 'share', 'volunteer']
    search_fields = ['name', 'email', 'employer__name']
    actions = [export_as_csv]

class LegAdmin(admin.ModelAdmin):
    list_display = ['id', 'mode', 'direction', 'day', 'commutersurvey', ]
    list_filter = ('commutersurvey__wr_day_month', )
    readonly_fields = ('commutersurvey', )
    actions = [export_as_csv]

class MonthsAdmin(admin.ModelAdmin):
    list_display = ['id', 'wr_day', 'open_checkin', 'close_checkin', 'active', 'url_month', 'short_name']
    list_editable = ['wr_day', 'open_checkin', 'close_checkin', 'active']
    actions = [export_as_csv]


admin.site.register(Commutersurvey, CommutersurveyAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(EmplSizeCategory, EmployerLookupAdmin)
admin.site.register(EmplSector, EmployerSectorAdmin)
admin.site.register(Month, MonthsAdmin)
admin.site.register(Leg, LegAdmin)
