from django.urls import path
from . import views
from rest_framework import routers
from .api import *

router = routers.DefaultRouter()
router.register('api/v1/clients', ClientAPI, 'clients')
router.register('api/v1/maillist', MailListAPI, 'maillist')
router.register('api/v1/stat', StatAPI, 'stat')

urlpatterns = router.urls

