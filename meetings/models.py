from django.db import models
from users.models import User

class Meeting(models.Model):
    title = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_meetings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participants = models.ManyToManyField(User, related_name='meetings')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title