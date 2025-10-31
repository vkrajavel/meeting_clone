from django.contrib import admin
from .models import Message, File

admin.site.register(Message)
admin.site.register(File)