from django.contrib import admin
from register.models import Business, Questions, Contact

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

def make_business_active(modeladmin, request, queryset, boolean):
    if not request.user.is_staff:
        raise PermissionDenied
    for business in queryset:
        business.make_active(boolean)

def activate(modeladmin, request, queryset):
    return make_business_active(modeladmin, request, queryset, True)

def deactivate(modeladmin, request, queryset):
    return make_business_active(modeladmin, request, queryset, False)

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'website', 'active')
    list_per_page = 200
    actions = ['delete_selected', activate, deactivate]


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('contact_name', 'business_name', 'heard_about', 'goals', 'sponsor', 'invoice')
    actions = ['delete_selected']


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'phone_number', 'applied', 'business_name')
    actions = ['delete_selected']


admin.site.register(Business, BusinessAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Contact, ContactAdmin)
