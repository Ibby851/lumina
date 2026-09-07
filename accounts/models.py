from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

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