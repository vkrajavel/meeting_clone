from django.urls import path
from .views import NotificationSendView, NotificationListView

urlpatterns = [
    path('send/', NotificationSendView.as_view(), name='notification_send'),
    path('', NotificationListView.as_view(), name='notification_list'),
]