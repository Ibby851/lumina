from .models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
def send_verification_email(user_id, verification_url):
    user = User.objects.get(id=user_id)
    html = render_to_string('accounts/verification_email_message.html', {'user':user, 'verification_url':verification_url})
    email = EmailMessage('Lumina Account Verification',html,"lumina@gmail.com",[user.email])
    email.content_subtype = 'html'
    email.send(fail_silently=True)


def send_password_reset_email(user_id, reset_url):
    user = User.objects.get(id=user_id)
    html = render_to_string('accounts/password_reset_email.html', {'user':user, 'reset_url':reset_url})
    email = EmailMessage('Lumina Password Reset Email', html,'lumina@gmail.com', [user.email])
    email.content_subtype = 'html'
    email.send(fail_silently=True)
