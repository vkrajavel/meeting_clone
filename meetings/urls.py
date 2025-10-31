from django.urls import path
from .views import (
    MeetingCreateView,
    MeetingListView,
    MeetingDetailView,
    MeetingUpdateView,
    MeetingDeleteView,
    MeetingInviteView,
    MeetingHistoryView
)

urlpatterns = [
    path('', MeetingListView.as_view(), name='meeting_list'),
    path('<int:id>/', MeetingDetailView.as_view(), name='meeting_detail'),
    path('create/', MeetingCreateView.as_view(), name='meeting_create'),
    path('<int:id>/update/', MeetingUpdateView.as_view(), name='meeting_update'),
    path('<int:id>/delete/', MeetingDeleteView.as_view(), name='meeting_delete'),
    path('invite/', MeetingInviteView.as_view(), name='meeting_invite'),
    path('history/', MeetingHistoryView.as_view(), name='meeting_history'),
]