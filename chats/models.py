from django.db import models
from django.contrib.auth.models import User
import mimetypes

# Create your models here.

class IndividualChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='messages/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_image(self):
        mime_type = mimetypes.guess_type(self.file.name)[0] if self.file else None
        return bool(mime_type and mime_type.startswith('image/'))

    @property
    def is_video(self):
        mime_type = mimetypes.guess_type(self.file.name)[0] if self.file else None
        return bool(mime_type and mime_type.startswith('video/'))

    @property
    def is_audio(self):
        mime_type = mimetypes.guess_type(self.file.name)[0] if self.file else None
        return bool(mime_type and mime_type.startswith('audio/'))


    