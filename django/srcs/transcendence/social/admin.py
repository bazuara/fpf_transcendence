from django.contrib import admin
from social.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'alias', 'win_ratio']
    search_fields = ['name', 'alias']

admin.site.register(User, UserAdmin)
# Register your models here.
