import datetime
import requests

from celery import Celery
from django.db import models
from django.db.models import signals
from django.utils.text import slugify
from .tasks import *


class MailList(models.Model):
    date_start = models.DateTimeField()
    text = models.CharField(max_length=250)
    filter_client = models.CharField(max_length=50)
    date_stop = models.DateTimeField()

    def __str__(self):
        return self.text

    def mails_info(self):
        return {'send': self.mails.filter(status=True).count(), 'process': self.mails.filter(status=False).count()}


def sending(sender, instance, created, **kwargs):
    date_start = instance.date_start
    text = instance.text
    filter_client = instance.filter_client
    date_stop = instance.date_stop

    if date_start < datetime.datetime.now(date_start.tzinfo) and datetime.datetime.now(date_stop.tzinfo) < date_stop:
        if filter_client in [i.tag for i in Client.objects.all()]:
            clients = Client.objects.filter(tag=filter_client)
        else:
            clients = Client.objects.filter(operator_code=filter_client)
        for i in clients:
            if Message.objects.filter(client=i, mail_list_obj=instance).count()>0:
                mes = Message.objects.get(client=i, mail_list_obj=instance)
                mes.status = False
                mes.date_create = datetime.datetime.now(date_start.tzinfo)
                mes.save()
            else:
                mes = Message()
                mes.client = i
                mes.status = False
                mes.date_create = datetime.datetime.now(date_start.tzinfo)
                mes.mail_list_obj = instance
                mes.save()
        for i in Message.objects.filter(mail_list_obj=instance):
            url = 'https://probe.fbrq.cloud/v1/send/' + str(i.id)
            data = {'id': i.id, 'phone': i.client.number, 'text': i.mail_list_obj.text}
            headers = {
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTUyOTE0MzQsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6InNpZGlrYXlmdXkifQ.N3ptqnOhx67CeCk2M1k3ntS5HmvnecVMWQr4XeGS9Fk',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
            send_request.apply_async((url, headers, data, i.id), ignore_result=True)

    elif date_start>datetime.datetime.now(date_start.tzinfo):
        if filter_client in [i.tag for i in Client.objects.all()]:
            clients = Client.objects.filter(tag=filter_client)
        else:
            clients = Client.objects.filter(operator_code=filter_client)

        for i in clients:
            if Message.objects.filter(client=i, mail_list_obj=instance).count()>0:
                mes = Message.objects.get(client=i, mail_list_obj=instance)
                mes.status = False
                mes.date_create = datetime.datetime.now(date_start.tzinfo)
                mes.save()
            else:
                mes = Message()
                mes.client = i
                mes.status = False
                mes.date_create = datetime.datetime.now(date_start.tzinfo)
                mes.mail_list_obj = instance
                mes.save()
        for i in Message.objects.filter(mail_list_obj=instance):
            url = 'https://probe.fbrq.cloud/v1/send/' + str(i.id)
            data = {'id': i.id, 'phone': i.client.number, 'text': i.mail_list_obj.text}
            headers = {
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTUyOTE0MzQsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6InNpZGlrYXlmdXkifQ.N3ptqnOhx67CeCk2M1k3ntS5HmvnecVMWQr4XeGS9Fk',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
            task = send_request.apply_async((url, headers, data, i.id), countdown=(date_start-datetime.datetime.now(date_start.tzinfo)).total_seconds())



signals.post_save.connect(sending, sender=MailList)


class Client(models.Model):
    TIME_ZONES=(
        ('GMT+3', 'Москва'),
        ('GMT+10', 'Владивосток')
    )
    number = models.CharField(max_length=250)
    operator_code = models.CharField(max_length=3, blank=True)
    tag = models.CharField(max_length=50)
    time_zone = models.CharField(max_length=10, choices=TIME_ZONES)

    def save(self, *args, **kwargs):
        self.operator_code = slugify(self.number)[1:4]
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return self.number


class Message(models.Model):
    date_create = models.DateTimeField()
    status = models.BooleanField()
    mail_list_obj = models.ForeignKey(MailList, related_name='mails', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

