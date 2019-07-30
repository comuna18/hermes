import json
import sendgrid

from .models import HermesEmailLogger as Logger
from django.conf import settings


SENDGRID_KEY = getattr(settings, "SENDGRID_API_KEY", None)
SENDGRID_DEFAULT_SENDER = getattr(settings, "SENDGRID_DEFAULT_SENDER", None)
BCC_RECIPIENTS_LIST = getattr(settings, "BCC_RECIPIENTS_LIST", None)


def init_sg_client():
    return sendgrid.SendGridAPIClient(apikey=SENDGRID_KEY)


def parse_recipients(recipients_list):
    rl = []
    for recipient in recipients_list:
        recipient_name = recipient.split("@")[0]
        rl.append({
            "email": recipient,
            "name": recipient_name
        })

    return rl


def parse_content(content, ctype="text/html"):
    return [
        {
            "type": ctype,
            "value": content
        }
    ]


def bcc_get_recipients_list():
    if BCC_RECIPIENTS_LIST:
        return parse_recipients(BCC_RECIPIENTS_LIST)

    return []


def send_email(recipients_list, subject, content, sender=None):
    """
    :param recipients_list: List with dicts, ex:
        [
            {
                "email": "test@example.com",
                "name": "Test Example",
            }
        ],
    :param subject: String
    :param content: List w/dict, ex:
    [
        {
            "type": "text/plain",
            "value": "and easy to do anywhere, even with Python"
        }
    ]
    :param sender: String, optional
    :return response: Sendgrid response object
    """

    if not sender:
        sender = SENDGRID_DEFAULT_SENDER

    bcc_list = bcc_get_recipients_list()

    sg = init_sg_client()

    data = {
        "personalizations": [
            {
                "to": recipients_list,
                "subject": subject
            }
        ],
        "from": {
            "email": sender
        },
        "content": content
    }

    if bcc_list:
        data["personalizations"][0]["bcc"] = bcc_list

    # initialize loggers
    recipients = json.dumps(data["personalizations"])
    content = json.dumps(data)

    log = Logger(
        recipients=recipients,
        subject=subject,
        content=content
    )

    log.save()

    try:
        response = sg.client.mail.send.post(request_body=data)
        log.response = "{}".format(response.status_code, response.body)
        log.status = Logger.STATUS_OK
        log.save()
    except Exception as e:
        response = e
        log.response = "{}".format(e)
        log.status = Logger.STATUS_ERROR
        log.save()

    return response


