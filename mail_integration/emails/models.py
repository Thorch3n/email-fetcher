# models.py

from django.db import models
from django.utils import timezone


class EmailAccount(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    provider = models.CharField(
        max_length=100,
        choices=[
            ('gmail', 'Gmail'),
            ('yandex', 'Yandex'),
            ('mail', 'Mail.ru')
        ])
    last_fetched = models.DateTimeField(
        null=True, blank=True,
        default=timezone.now
    )


class Message(models.Model):
    email_account = models.ForeignKey(
        EmailAccount,
        on_delete=models.CASCADE
    )
    subject = models.CharField(max_length=255)
    sent_date = models.DateTimeField(null=True, blank=True)
    received_date = models.DateTimeField(null=True, blank=True)
    body = models.TextField()
    attachments = models.JSONField(default=list)  # для хранения списка файлов
