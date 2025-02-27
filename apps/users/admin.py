from django.contrib import admin

from apps.users.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined')
    list_filter = ('username', )
    search_fields = ('username', 'first_name', 'last_name', 'email', 'date_joined')
    list_per_page = 20
