from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import IndividualChat
from .forms import MessageCreateForm

# Create your views here.

@login_required
def chat_list(request):
    friends = request.user.friends.prefetch_related('user', 'user__profile').all()
    return render(request, 'chat/chat_list.html', {'friends':friends})

@login_required
def individual_chat(request, friend_username):
    form = MessageCreateForm()
    friend = User.objects.get(username=friend_username)
    friend_profile = friend.profile
    chats = IndividualChat.objects.filter(Q(sender=request.user, receiver=friend) | Q(sender=friend, receiver=request.user)).order_by('created_at')
    return render(request, 'chat/individual_chat_page.html', {'friend':friend, 'friend_profile':friend_profile, 'chats':chats, "form":form})

# @login_required
# def create_message(request, friend_username):

#     form = MessageCreateForm(request.POST)
#     if form.is_valid():
#         content = form.cleaned_data.get('content')
#         friend = User.objects.get(username=friend_username)
#         message = IndividualChat.objects.create(sender=request.user, receiver=friend, content=content)
#         html = render_to_string('partial/message-return.html#created-message', {'chat':message})
#         response = HttpResponse(html)
#         response["HX-Trigger"] = 'messageCreated'
#         return response