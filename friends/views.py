from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from friends.models import FriendRequest
from django.template.loader import render_to_string
# Create your views here.

@login_required
def friend_requests(request):
    sent_requests = FriendRequest.objects.filter(sender = request.user).select_related('receiver', 'receiver__profile')
    received_requests = FriendRequest.objects.filter(receiver=request.user).select_related('sender', 'receiver__profile')
    return render(request, 'friends/friend_requests.html', {'sent_requests':sent_requests, 'received_requests':received_requests})

@login_required
def friends_list(request):
    friends_list = request.user.profile.friends.all().prefetch_related('profile')
    return render(request, 'friends/friends_list.html', {'friends':friends_list})

@login_required
def send_friendrequest(request, receiver_username):
    sender = request.user
    receiver = User.objects.get(username=receiver_username)
    if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists() or FriendRequest.objects.filter(sender=receiver, receiver=sender).exists():
        return HttpResponse('Request Sent Already')
    else:
        FriendRequest.objects.create(sender=sender, receiver=receiver)
        return HttpResponse('Request Sent')

@login_required
def accept_or_decline_friendrequest(request, sender_username ,action):
    sender = User.objects.get(username=sender_username)
    receiver = request.user
    friend_request_obj = FriendRequest.objects.get(sender=sender, receiver=receiver)
    if action == 'decline':
        friend_request_obj.delete()
        return HttpResponse('')
    else:
        receiver.profile.friends.add(sender)
        sender.profile.friends.add(receiver)
        friend_request_obj.delete()
        return HttpResponse('Accepted ✓')

@login_required
def cancel_friend_request(request, receiver_username):
    receiver = User.objects.get(username=receiver_username)
    friend_request_obj = FriendRequest.objects.get(sender=request.user, receiver=receiver)
    friend_request_obj.delete()
    return HttpResponse('')

@login_required
def remove_friend(request, friend_username):
    enemy = User.objects.get(username=friend_username)
    request.user.profile.friends.remove(enemy)
    enemy.profile.friends.remove(request.user)

    html = render_to_string('partial/partial1.html#friend-request-btn', {'user':enemy})
    
    return HttpResponse(html)




