from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [

    path('',views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('home/', views.home, name='home'),
    path('view-my-profile/', views.profile_view, name='profile_view'),
    path('edit-profile/', views.profile_edit, name='profile_edit'),
    path('logout/', views.logout, name='logout'),
    path('view-profile/<str:username>/', views.view_others_profile, name='view_others_profile'),
    path('search-users/', views.search, name='search'),
    path('find-user/', views.search_user_query_handler, name='search_query_handler'),
    path('create-post/', views.create_post, name='create_post')
]