from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    location = models.CharField(max_length=100, blank=True, null=True)
    about = models.CharField(max_length=255, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    profile_photo = models.ImageField(upload_to='photos/%Y/%m/%d', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])], null=True, blank=True)
    friends = models.ManyToManyField(to=User, blank=True, related_name='friends')

    def count_friends(self):
        return self.friends.count()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(blank=True,null=True)
    audio = models.FileField(upload_to='posts/audios/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Token(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User,related_name='token', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() - self.created_at <= timedelta(minutes=5)
    
class PasswordResetToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, related_name='password_reset_token', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() - self.created_at <= timedelta(minutes=1)