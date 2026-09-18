from django.urls import path
from . import views, routing

app_name = 'chats'

urlpatterns = [
    path('list/', views.chat_list, name='chat_list'),
    path('individual/<str:friend_username>/', views.individual_chat, name='chat_user'),
    path('send-file-to/<str:friend_username>/', views.send_file, name='send_file'),
    
]
