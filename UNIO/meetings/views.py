from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Meeting
from .serializers import MeetingSerializer
from users.models import User
from django.utils import timezone

bearer_auth = openapi.Parameter(
    name='Authorization',
    in_=openapi.IN_HEADER,
    description='JWT Authorization header. Example: "Bearer <your_token>"',
    type=openapi.TYPE_STRING,
)

class MeetingCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=MeetingSerializer,
        responses={201: 'Meeting created', 400: 'Invalid data'},
        tags=['Meeting Management']
    )
    def post(self, request):
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)
            return Response({'message': 'Meeting created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeetingListView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: MeetingSerializer(many=True)},
        tags=['Meeting Management']
    )
    def get(self, request):
        meetings = Meeting.objects.filter(participants=request.user)
        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data)

class MeetingDetailView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: MeetingSerializer(), 404: 'Meeting not found'},
        tags=['Meeting Management']
    )
    def get(self, request, id):
        try:
            meeting = Meeting.objects.get(id=id, participants=request.user)
            serializer = MeetingSerializer(meeting)
            return Response(serializer.data)
        except Meeting.DoesNotExist:
            return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

class MeetingUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=MeetingSerializer,
        responses={200: 'Meeting updated', 400: 'Invalid data', 404: 'Meeting not found'},
        tags=['Meeting Management']
    )
    def put(self, request, id):
        try:
            meeting = Meeting.objects.get(id=id, organizer=request.user)
            serializer = MeetingSerializer(meeting, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Meeting updated'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Meeting.DoesNotExist:
            return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

class MeetingDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={204: 'Meeting deleted', 404: 'Meeting not found'},
        tags=['Meeting Management']
    )
    def delete(self, request, id):
        try:
            meeting = Meeting.objects.get(id=id, organizer=request.user)
            meeting.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Meeting.DoesNotExist:
            return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

class MeetingInviteView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'meeting_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'user_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)),
            },
            required=['meeting_id', 'user_ids']
        ),
        responses={200: 'Invites sent', 400: 'Invalid data', 404: 'Meeting not found'},
        tags=['Meeting Management']
    )
    def post(self, request):
        meeting_id = request.data.get('meeting_id')
        user_ids = request.data.get('user_ids', [])
        try:
            meeting = Meeting.objects.get(id=meeting_id, organizer=request.user)
            users = User.objects.filter(id__in=user_ids)
            meeting.participants.add(*users)
            return Response({'message': 'Invites sent'})
        except Meeting.DoesNotExist:
            return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

class MeetingHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: MeetingSerializer(many=True)},
        tags=['Meeting Management']
    )
    def get(self, request):
        meetings = Meeting.objects.filter(participants=request.user, end_time__lt=timezone.now())
        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data)