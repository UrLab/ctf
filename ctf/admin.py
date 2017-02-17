from django.contrib import admin
from .models import IPLog


@admin.register(IPLog)
class IpAdmin(admin.ModelAdmin):
    list_display = ('ip', 'user')
