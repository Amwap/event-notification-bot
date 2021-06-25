from django.contrib import admin
from .models import *


@admin.register(User)
class searchUser(admin.ModelAdmin):
    search_fields = ('ticket_code',)

# admin.site.register([User, searchUser])
admin.site.register(Event)
admin.site.register(Admin)