

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .forms import LoginForm, ProfileEditForm, RegistrationForm, PostCreateForm, VerificationTokenRequestForm, PasswordResetEmailForm, PasswordResetInput
from .models import Profile, Post, Token, PasswordResetToken
from django_q.tasks import async_task
from .tasks import send_verification_email, send_password_reset_email
import secrets

# Create your views here.

def index(request):
    return render(request, 'accounts/index.html')

def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        new_user = User.objects.create_user(username=data.get('username'), email=data.get('email'), password=data.get('password'), first_name=data.get('first_name'),last_name=data.get('last_name'), is_active=False)
        Profile.objects.create(user=new_user)
        token = Token.objects.create(user=new_user, token=secrets.token_urlsafe(32))
        url = reverse('accounts:verify_user',kwargs={'token':token.token})
        send_verification_email(new_user.id, request.build_absolute_uri(url))
        return render(request,'accounts/email_sent_message.html')

    return render(request, 'accounts/register.html', {'form':form})

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password, email=username)
            if user is not None:
                auth_login(request, user)
                return redirect('accounts:home')

        form.add_error(None, 'Invalid Username, Email, or Password.')

    return render(request,'accounts/login.html', {'form':form})

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                reset_token = PasswordResetToken.objects.create(user=user, token=secrets.token_urlsafe(32))
                url = reverse('accounts:password_reset_input', kwargs={'token':reset_token.token})
                send_password_reset_email, user.id, request.build_absolute_uri(url)
                return render(request,'accounts/password_reset_link_sent_success.html')
                
            else:
                form.add_error(None, 'Invalid Email')
                return render(request, 'accounts/password_reset_form.html', {'form':form})
    form = PasswordResetEmailForm()
    return render(request, 'accounts/password_reset_form.html', {'form':form})


def password_reset_input(request, token):
    form = PasswordResetEmailForm()
    if PasswordResetToken.objects.filter(token=token).exists():
        token = PasswordResetToken.objects.get(token=token)
        if token.is_valid():
            form = PasswordResetInput()
            return render(request, 'accounts/password_reset_password_input.html',{'form':form, 'token':token.token})
        else:
            token.delete()
            return render(request, 'accounts/password_reset_form.html', {'error':'Invalid Password Reset Token, Try Again!!', 'form':form})
    return render(request, 'accounts/password_reset_form.html', {'error':'Invalid Password Reset Token, Try Again!!', 'form':form})

def password_reset_handler(request, reset_token):
    token = PasswordResetToken.objects.get(token=reset_token)
    if request.method == 'POST':
        form = PasswordResetInput(request.POST)
        if form.is_valid():
            user = token.user
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            token.delete()
            return render(request,'accounts/password_reset_success.html')
        else:
            return render(request, 'accounts/password_reset_password_input.html', {'form':form, 'token':token.token})



def verify_user(request, token):
    form = VerificationTokenRequestForm()
    if Token.objects.filter(token=token).exists():
        token = Token.objects.get(token=token)
        if token.is_valid():
            user = token.user
            user.is_active = True
            user.save()
            token.delete()
            return render(request, 'accounts/success_verification.html')
        token.delete()
        return render(request,'accounts/token_verification_failed.html', {'form':form})
    else:
        return render(request,'accounts/token_verification_failed.html', {'form':form})

def request_new_verification_token(request):
    form = VerificationTokenRequestForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = Token.objects.create(user=user, token=secrets.token_urlsafe(32))
            url = reverse("accounts:verify_user", kwargs={'token':token.token})
            async_task(send_verification_email, user.id, request.build_absolute_uri(url))
            return render(request,'accounts/email_sent_message.html')
    form.add_error(None,"No user with the email supplied")
    return render(request,'accounts/token_verification_failed.html', {'form':form})


@login_required
def home(request):
    form = PostCreateForm()
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'accounts/home.html', {'form':form, 'posts':posts})

@login_required
def profile_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'accounts/profile.html', {'user':user, 'profile':profile, 'posts':posts})

@login_required
def profile_edit(request):

    user = request.user
    profile = Profile.objects.get(user=user)
    form = ProfileEditForm(initial={
        'first_name':user.first_name, 'last_name':user.last_name, 'about':profile.about, 'email':user.email,'location':profile.location,
        'username':user.username
    }, user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, user=request.user)
        old_picture = profile.profile_photo
        if form.is_valid():
            data = form.cleaned_data
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.email = data.get('email')
            user.username = data.get('username')
            profile.about = data.get('about')
            profile.profile_photo = data.get('profile_photo')
            profile.location = data.get('location')
            user.save()
            profile.save()
            return redirect('accounts:profile_view')
    
    return render(request, 'accounts/profile_edit.html', {'form': form, 'user': user, 'profile':profile})


@login_required
def search(request):
    users = User.objects.select_related('profile').all().exclude(username=request.user.username)
    return render(request, 'accounts/search_page.html', {'users':users})

@login_required
def view_others_profile(request, username):
    user = User.objects.get(username=username)
    profile = user.profile
    posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'accounts/other_user_profile.html', {'user':user, 'profile':profile, 'posts':posts})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:index')

@login_required
def search_user_query_handler(request):
    query = request.GET.get('query')
    users = User.objects.filter(Q(username__icontains=query)).select_related('profile').order_by(Lower('username'))
    html = render_to_string('partial/partial1_accounts.html#search-query-result', {'users':users}, request=request)
    return HttpResponse(html)


@login_required
def create_post(request):
    form = PostCreateForm(request.POST,request.FILES)
    if form.is_valid():
        clean_data = form.cleaned_data
        post = Post.objects.create(author=request.user, text=clean_data.get('text'), audio=clean_data.get('audio'), video=clean_data.get('video'), image=clean_data.get('image'))
        html= render_to_string('accounts/post.html', {'post':post})
        response = HttpResponse(html)
        response['HX-Trigger'] = 'postCreated'
        return response
    else:
        html = render_to_string('partial/partial1_accounts.html#failed-form',{'form':form}, request=request)
        response = HttpResponse(html)
        response['HX-Retarget'] = '#post-form'
        response['HX-Reswap'] = 'outerHTML'
        return response
    
    
        


