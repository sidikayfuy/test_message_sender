from django.urls import path
from . import views
from rest_framework import routers
from .api import *


from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework import renderers

router = routers.DefaultRouter()
router.register('api/v1/clients', ClientAPI, 'clients')
router.register('api/v1/maillist', MailListAPI, 'maillist')
router.register('api/v1/stat', StatAPI, 'stat')

urlpatterns = [
    path('docs/', TemplateView.as_view(
        template_name='messageapi/swagger-ui.html',
        extra_context={'schema_url':'openapi-schema-yaml'}
    ), name='swagger-ui'),
    path('openapi.yaml', get_schema_view(
            title="Best API Service",
            renderer_classes=[renderers.OpenAPIRenderer]
        ), name='openapi-schema-yaml'),
]

urlpatterns += router.urls

