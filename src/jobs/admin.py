from django.contrib import admin

from .models import Job,Location,Employer
# Register your models here.

admin.site.register(Job)
admin.site.register(Location)
admin.site.register(Employer)
