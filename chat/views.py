from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Message, File
from .serializers import MessageSerializer, FileSerializer
from meetings.models import Meeting
from django.http import FileResponse

bearer_auth = openapi.Parameter(
    name='Authorization',
    in_=openapi.IN_HEADER,
    description='JWT Bearer token. Example: "Bearer <your_token>"',
    type=openapi.TYPE_STRING,
)


class MessageSendView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'meeting_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'content': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['meeting_id', 'content']
        ),
        responses={201: 'Message sent', 400: 'Invalid data', 404: 'Meeting not found'},
        tags=['Chat']
    )
    def post(self, request):
        meeting_id = request.data.get('meeting_id')
        content = request.data.get('content')
        try:
            meeting = Meeting.objects.get(id=meeting_id, participants=request.user)
            Message.objects.create(sender=request.user, meeting=meeting, content=content)
            return Response({'message': 'Message sent'}, status=status.HTTP_201_CREATED)
        except Meeting.DoesNotExist:
            return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

class MessageListView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: MessageSerializer(many=True), 404: 'Meeting not found'},
        tags=['Chat']
    )
    def get(self, request, meeting_id):
        try:
            meeting = Meeting.objects.get(id=meeting_id, participants=request.user)
            messages = Message.objects.filter(meeting=meeting)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except Meeting.DoesNotExist:
            return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'meeting_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'file': openapi.Schema(type=openapi.TYPE_FILE),
            },
            required=['meeting_id', 'file']
        ),
        responses={201: 'File uploaded', 400: 'Invalid data', 404: 'Meeting not found'},
        tags=['Chat']
    )
    def post(self, request):
        meeting_id = request.data.get('meeting_id')
        file = request.FILES.get('file')
        try:
            meeting = Meeting.objects.get(id=meeting_id, participants=request.user)
            File.objects.create(uploader=request.user, meeting=meeting, file=file)
            return Response({'message': 'File uploaded'}, status=status.HTTP_201_CREATED)
        except Meeting.DoesNotExist:
            return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: 'File download', 404: 'File not found'},
        tags=['Chat']
    )
    def get(self, request, file_id):
        try:
            file = File.objects.get(id=file_id, meeting__participants=request.user)
            return FileResponse(file.file, as_attachment=True)
        except File.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)