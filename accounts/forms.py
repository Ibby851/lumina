from xml.parsers.expat import model

from django import forms
from django.conf.locale import de
from django.contrib.auth.models import User
from .models import Profile, Post

class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'password2']

    def clean_username(self):
        form_fields = self.cleaned_data
        if User.objects.filter(username=form_fields.get('username')).exists():
            self.add_error('username', 'Username Already Exists')
        elif len(form_fields.get('username')) < 5:
            self.add_error('username', 'Username is less that five characters')
        else:
            pass
        return form_fields.get('username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Username Already Exists')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 5:
            self.add_error('password', 'Password Too Short')
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            self.add_error('password', 'Password Mismatch')
            self.add_error('password2', 'Password Mismatch')
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)



class ProfileEditForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    about = forms.CharField()
    email = forms.CharField()
    location = forms.CharField()
    profile_photo = forms.ImageField(required=False)

    def __init__(self, *args, user,**kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_first_name(self):
        fn = self.cleaned_data.get('first_name')
        if len(fn) < 5:
            self.add_error('first_name', 'First Name cannot have less than five characters')
        return fn

    def clean_last_name(self):
        ln = self.cleaned_data.get('last_name')
        if len(ln) < 5:
            self.add_error('first_name', 'Last Name cannot have less than five characters')
        return ln

    def clean_about(self):
        about = self.cleaned_data.get('about')
        if len(about) == 0:
            self.add_error('about', "Bio cannot be empty")
        return about

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(username=self.user.username).filter(email=email).exists():
            self.add_error('email', 'User with the email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(username=self.user.username).filter(username=username):
            self.add_error('username', "User with the username already exists")
        return username



class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'audio', 'video', 'image']

    def clean(self):
        data = super().clean()
        if not any([data.get('text'), data.get('audio'), data.get('video'), data.get('image')]):
            raise forms.ValidationError('Your post must contain at least a text, an image, a video or an audio.')
        return data

class VerificationTokenRequestForm(forms.Form):
    email = forms.EmailField()

class PasswordResetEmailForm(forms.Form):
    email = forms.EmailField()

class PasswordResetInput(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_password1(self):
        value = self.cleaned_data.get('password1')
        if len(value) < 5:
            self.add_error('password1', 'Password too short')
        return value

    def clean_password2(self):
        value = self.cleaned_data.get('password2')
        if len(value) < 5:
            self.add_error('password2', 'Password too short')
        return value

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            self.add_error(None,'Password did not match.')
        return cleaned_data
        
