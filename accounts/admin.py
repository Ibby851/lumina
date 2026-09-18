from django.contrib import admin
from .models import Profile, Post, Token, PasswordResetToken

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Token)
admin.site.register(PasswordResetToken)