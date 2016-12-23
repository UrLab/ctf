from django.contrib import admin
from .models import User, Team


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'team', 'email', 'created', 'first_name', 'last_name')
    list_filter = ('team',)
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass
