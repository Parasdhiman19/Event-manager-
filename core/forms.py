from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
from django import forms
class MyUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    model = MyUser
    fields =( 'username' , 'email' )


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

