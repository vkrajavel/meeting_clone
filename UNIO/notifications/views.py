from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Notification
from .serializers import NotificationSerializer
from meetings.models import Meeting

bearer_auth = openapi.Parameter(
    name='Authorization',
    in_=openapi.IN_HEADER,
    description='JWT Bearer token. Example: "Bearer <your_token>"',
    type=openapi.TYPE_STRING,
)


class NotificationSendView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'meeting_id': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
            },
            required=['message']
        ),
        responses={201: 'Notification sent', 400: 'Invalid data'},
        tags=['Notifications']
    )
    def post(self, request):
        message = request.data.get('message')
        meeting_id = request.data.get('meeting_id')
        meeting = Meeting.objects.get(id=meeting_id) if meeting_id else None
        Notification.objects.create(user=request.user, message=message, meeting=meeting)
        return Response({'message': 'Notification sent'}, status=status.HTTP_201_CREATED)

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: NotificationSerializer(many=True)},
        tags=['Notifications']
    )
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)