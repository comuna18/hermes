from django.db import models
from django.utils import timezone


class HermesEmailLogger(models.Model):
    class Meta:
        verbose_name = 'Email Logger'
        verbose_name_plural = 'Emails Loggers'

    STATUS_NEW = 'NEW'
    STATUS_ERROR = 'ERROR'
    STATUS_OK = 'OK'

    EMAIL_STATUS = (
        (STATUS_NEW, 'Nuevo'),
        (STATUS_ERROR, 'Error'),
        (STATUS_OK, 'OK'),
    )

    recipients  = models.TextField('Recipients', max_length=1024)
    subject = models.CharField('Subject', max_length=512)
    content = models.TextField('Content', default='', blank=True)
    status = models.CharField('Status', max_length=16, choices=EMAIL_STATUS, default=STATUS_NEW)
    response = models.CharField('Reponse', max_length=256, default='', blank=True)
    retry_number = models.PositiveSmallIntegerField('Retry Number', default=0)

    create_date = models.DateTimeField(
        'Creado',
        auto_now_add=True,
        editable=False
    )
    modified_date = models.DateTimeField(
        'Modificado',
        auto_now_add=True,
        editable=False
    )

    def save(self, *args, **kwargs):
        if self.id:
            self.modified_date = timezone.now()
        else:
            self.create_date = timezone.now()

        super().save(*args, **kwargs) 


