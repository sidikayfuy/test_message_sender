
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response

from .models import *
from .serializers import *


class ClientAPI(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ClientSerializer


class MailListAPI(viewsets.ModelViewSet):
    queryset = MailList.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = MailListSerializer


class StatAPI(viewsets.ModelViewSet):
    queryset = MailList.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = StatSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StatCurSerializer(instance)
        return Response(serializer.data)
