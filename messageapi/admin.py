from django.contrib import admin
from .models import *


admin.site.register(MailList)
admin.site.register(Client)
admin.site.register(Message)

