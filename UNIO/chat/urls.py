from django.urls import path
from .views import MessageSendView, MessageListView, FileUploadView, FileDownloadView

urlpatterns = [
    path('send/', MessageSendView.as_view(), name='message_send'),
    path('messages/<int:meeting_id>/', MessageListView.as_view(), name='message_list'),
    path('file/upload/', FileUploadView.as_view(), name='file_upload'),
    path('file/download/<int:file_id>/', FileDownloadView.as_view(), name='file_download'),
]