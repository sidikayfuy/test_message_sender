import json
from django.apps import apps
import requests
from django.http import JsonResponse
from test_message.celery import app


@app.task(bind=True, default_retry_delay=60)
def send_request(self, url, headers, data, id):
    try:
        status = requests.post(url=url, headers=headers, json=data)
        if status.status_code == 200:
            model = apps.get_model(app_label='messageapi', model_name='Message')
            mes = model.objects.get(pk=id)
            mes.status = True
            mes.save()
            return 'done'
        else:
            return status.content
    except Exception as exc:
        raise self.retry(exc=exc)



