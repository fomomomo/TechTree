from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']

class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = '__all__'
        exclude = ['host', 'poll_takers', 'room']

class OptionForm(ModelForm):
    class Meta:
        model = Option
        fields = '__all__'
        exclude = ['question', 'user_selections']
