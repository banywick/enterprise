from django.contrib import admin

from .models import UserIP

@admin.register(UserIP)
class UserIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'name')
    
    

# class UserIPAdmin(admin.ModelAdmin):
#     list_display = ('ip_address', 'name')

# admin.site.register(UserIP, UserIPAdmin)
