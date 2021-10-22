from django.contrib import admin

from .models import *

admin.site.register(Founder)
admin.site.register(Institution)
admin.site.register(Category)
admin.site.register(Equipment)
admin.site.register(Application)
admin.site.register(ApplicationEquipment)
