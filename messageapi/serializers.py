from rest_framework import serializers
from .models import *


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class MailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailList
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'date_create', 'status', 'client']
        depth = 1


class StatSerializer(serializers.ModelSerializer):
    full = serializers.IntegerField(source='mails.count', read_only=True)

    class Meta:
        model = MailList
        fields = ['id',
                  'date_start',
                  'text',
                  'filter_client',
                  'date_stop',
                  'full',
                  'mails_info',
                  ]


class StatCurSerializer(serializers.ModelSerializer):
    mails = MessageSerializer(read_only=True, many=True)
    class Meta:
        model = MailList
        fields = ['id',
                  'date_start',
                  'text',
                  'filter_client',
                  'date_stop',
                  'mails'
                  ]



