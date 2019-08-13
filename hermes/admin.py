import json
from django.contrib import admin

from .models import HermesEmailLogger as Logger
from .services import send_raw_email


def resend_email(modeladmin, request, queryset):
    for log in queryset:
        error = None
        log.retry_number += 1

        try:
            data = json.loads(log.content)
        except Exception as e:
            data = None
            error = e
            
        if data:
            res = send_raw_email(data)

            log.response = res["response"]
            log.status = res["code"]

        else:
            log.response = e
            log.status = Logger.STATUS_ERROR

        log.save()

resend_email.short_description = "Volver a enviar emails"


@admin.register(Logger)
class LoggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipients', 'status', 'response', 'create_date', 'retry_number', )
    list_filter = ('status', )
    search_fields = ['recipients',]
    actions = [resend_email]

