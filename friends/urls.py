from django.urls import path
from . import views

app_name = 'friends'
urlpatterns = [
    path('requests/', views.friend_requests, name='friend_requests'),
    path('list/', views.friends_list, name='friends_list'),
    path('send-friend-request/<str:receiver_username>/', views.send_friendrequest, name='send_friendrequest'),
    path('accept-or-decline-friend-request/<str:sender_username>/<str:action>/', views.accept_or_decline_friendrequest,name='handle_friendrequest'),
    path('cancel-friend-request/<str:receiver_username>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('remove-friend/<str:friend_username>', views.remove_friend, name='remove_friend')
]