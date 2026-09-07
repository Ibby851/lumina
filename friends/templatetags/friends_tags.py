from django import template
from ..models import FriendRequest

register = template.Library()

@register.simple_tag
def check_friendship(user1, user2):

    if FriendRequest.objects.filter(sender=user1, receiver=user2):
        return 'Request Sent'
    return '+ Add Friend'

@register.filter
def check_already_friend(user1, user2):
    if user1 in user2.profile.friends.all() and user2 in user1.profile.friends.all():
        return True
    return False
