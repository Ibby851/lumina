from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class IndividualChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='messages/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    


    