
import csv
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from django.db.models import Sum, Count

from django.forms import ModelForm

from survey.models import Commutersurvey, Employer, EmplSector, EmplSizeCategory
from leaderboard.models import Month
# from django.contrib import admin
from django.contrib.gis import admin


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
            {'fields': ['month', 'name', 'email', 'employer', 'newsletter']}),
        ('Commute', 
            {'fields': ['home_address', 'work_address', 'to_work_today', 'from_work_today', 'to_work_normally', 'from_work_normally']}),
        ('Maps',
            {'fields': ['geom', ]}),
        ('Meta',
            {'fields': ['ip']}),
    ]
    list_display = ('month', 'email', 'employer', 'home_address', 'work_address', 'to_work_switch', 'from_work_switch', 'to_work_today', 'from_work_today', 'to_work_normally', 'from_work_normally')
    list_display_links = ['email']
    list_editable = ['employer']
    list_filter = ['month', 'to_work_today', 'from_work_today', 'to_work_normally', 'from_work_normally']
    search_fields = ['name', 'employer']
    actions = [export_as_csv]

class MonthsAdmin(admin.ModelAdmin):
    search_fields = ['month']
    list_display_links = ['id']
    list_display = ['id', 'month', 'url_month', 'short_name', 'active']
    list_editable = ['month', 'url_month', 'short_name', 'active']
    actions = [export_as_csv]


admin.site.register(Commutersurvey, CommutersurveyAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(EmplSizeCategory, EmployerLookupAdmin)
admin.site.register(EmplSector, EmployerSectorAdmin)
admin.site.register(Month, MonthsAdmin)
