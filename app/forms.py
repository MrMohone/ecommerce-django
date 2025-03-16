from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput
                               (attrs={'autofocus ' : 'True',
                                       'class' : 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput
                                (attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput
                                (attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confrim Password', widget=forms.PasswordInput
                                (attrs={'class' : 'form-control'}))
    
    class Meta:#for displaying Users in admin db like admn.py .......
        model = User
        fields = ['username', 'email', 'password1', 'password2']