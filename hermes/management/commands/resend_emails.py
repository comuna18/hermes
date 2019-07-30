import json

from django.core.management.base import BaseCommand
from hermes.models import HermesEmailLogger as Logger

from hermes.services import init_sg_client


class Command(BaseCommand):
    help = "Resend Emails w/error"

    def handle(self, *args, **kwargs):
        sg = init_sg_client()
        for log in Logger.objects.filter(
            status=Logger.STATUS_ERROR,
            retry_number__lte=3
        ):
            try:
                data = json.loads(log.content)
                response = sg.client.mail.send.post(request_body=data)
                log.response = "{}".format(response.status_code, response.body)
                log.status = Logger.STATUS_OK
                log.save()
            except Exception as e:
                response = e
                log.response = "{}".format(e)
                log.status = Logger.STATUS_ERROR
                log.retry_number += 1
                log.save()
