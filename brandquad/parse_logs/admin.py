from django.contrib import admin

from parse_logs.models import DataLog


class DataLogAdmin(admin.ModelAdmin):
    list_filter = ['date', 'method', 'response_status']
    search_fields = ['ip', 'date', 'method', 'uri', 'response_status', 'response_size']
    list_display = ['ip', 'date', 'method', 'uri', 'response_status', 'response_size']

admin.site.register(DataLog, DataLogAdmin)
