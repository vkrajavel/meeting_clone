from django.urls import re_path
from meetings.consumers import MeetingConsumer

websocket_urlpatterns = [
    re_path(r'ws/meeting/(?P<meeting_id>\w+)/$', MeetingConsumer.as_asgi()),
]