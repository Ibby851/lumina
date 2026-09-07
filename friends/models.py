from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendrequest_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendrequest_receiver')
    sent_at = models.DateTimeField(auto_now_add=True)