from django.contrib import admin

from .models import HermesEmailLogger as Logger


@admin.register(Logger)
class LoggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipients', 'status', 'response', 'create_date', 'retry_number', )
    list_filter = ('status', )
    search_fields = ['recipients',]

