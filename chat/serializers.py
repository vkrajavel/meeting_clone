from rest_framework import serializers
from .models import Message, File

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'meeting', 'content', 'timestamp']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'uploader', 'meeting', 'file', 'uploaded_at']