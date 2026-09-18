from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import IndividualChat
from .forms import FileMessageForm, MessageCreateForm

# Create your views here.

@login_required
def chat_list(request):
    friends = request.user.friends.prefetch_related('user', 'user__profile').all()
    return render(request, 'chat/chat_list.html', {'friends':friends})

@login_required
def individual_chat(request, friend_username):
    form = MessageCreateForm()
    file_form = FileMessageForm()
    friend = User.objects.get(username=friend_username)
    friend_profile = friend.profile
    chats = IndividualChat.objects.filter(Q(sender=request.user, receiver=friend) | Q(sender=friend, receiver=request.user)).order_by('created_at')
    return render(request, 'chat/individual_chat_page.html', {'friend':friend, 'friend_profile':friend_profile, 'chats':chats, 'form':form, 'file_form':file_form})


@login_required
def send_file(request, friend_username):
    form = FileMessageForm(request.POST, request.FILES)
    friend = User.objects.get(username=friend_username)
    if form.is_valid():
        file_obj = form.save(commit=False)
        file_obj.sender = request.user
        file_obj.receiver = friend
        file_obj.save()
        channel_layer = get_channel_layer()
        ids = sorted([request.user.id, friend.id])
        group_name = f"chat_{ids[0]}_{ids[1]}"
        async_to_sync(channel_layer.group_send)(group_name,{'type':'broadcast_message', 'message_id':file_obj.id, 'sender_id':request.user.id})
        return HttpResponse('')
    else:
        response = HttpResponse('Select a file to send please')
        response['HX-Retarget'] = '#error'
        response['HX-Reswap'] = 'innerHTML'
        return response