from django.contrib import admin
from register.models import Business, Questions, Contact

# Register your models here.
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'website')
    list_per_page = 200
    actions = ['delete_selected']


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('heard_about', 'goals', 'sponsor')
    actions = ['delete_selected']


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'phone_number', 'applied', 'business_name')
    actions = ['delete_selected']


admin.site.register(Business, BusinessAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Contact, ContactAdmin)
