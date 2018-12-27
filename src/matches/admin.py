from django.contrib import admin
from .models import ( Matches,PositionMatch , LocationMatch , EmployerMatch )
# Register your models here.

admin.site.register(Matches)
admin.site.register(PositionMatch)
admin.site.register(EmployerMatch)
admin.site.register(LocationMatch)