from django.contrib import admin
from retail.models import partner

# Register your models here.
class partnerAdmin(admin.ModelAdmin): 
	fieldsets = [
		('Business Information',	{'fields' : ['name', 'phone', 'website', 'offer']}),
		('Address', 				{'fields' : ['street', 'city', 'zipcode']}),
		('Coordinates', 			{'fields' : ['latitude', 'longitude']}),
		('Contact Information', 	{'fields' : ['contact_name', 'contact_phone', 'contact_email']}),
		('Other', 					{'fields' : ['category', 'notes']}),
		( None, 					{'fields' : ['approved']})
	]

	list_display = ('name', 'address', 'contact_name', 'contactPhoneNumber', 'contact_email', 'notes', 'approved')
	list_filter = ['approved', 'city']
	search_fields = ['name']
	list_per_page = 200

admin.site.register(partner, partnerAdmin)