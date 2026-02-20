from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from users.models import User

class UserLoginForm(AuthenticationForm):
    username =  forms.CharField(widget=forms.TextInput(attrs={
        'type' : 'text',
        'name' : "text_name",
        'placeholder' : "Логин",
        "style": "width: 90%; line-height: 28px; ",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type' : 'password',
        'name' : "text_name",
        'placeholder' : "Пароль",
        "style": "width: 90%; line-height: 28px; ",
    }))

    class Meta:
        model = User
        fields = ('username', 'password')

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "type" : "text",
        "name" : "text_name",
        "placeholder" : "Имя",
        "style" : "width: 90%; line-height: 28px; "
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "name": "text_name",
        "placeholder": "Фамилия",
        "style": "width: 90%; line-height: 28px; "
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "name": "text_name",
        "placeholder": "Логин",
        "style": "width: 90%; line-height: 28px; "
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "name": "text_name",
        "placeholder": "Пароль",
        "style": "width: 90%; line-height: 28px; "
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "name": "text_name",
        "placeholder": "Подтверждение пароля",
        "style": "width: 90%; line-height: 28px; "
    }))
    roles = forms.Select(attrs={
        "font-size":"15px",
    })
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'password1', 'password2', 'roles')
class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'type':'text',
        'name':'text_name',
        'placeholder':'Изменить имя',
        'style':'width: 50%; line-height: 28px;'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'name': 'text_name',
        'placeholder': 'Изменить фамилию',
        'style': 'width: 50%; line-height: 28px;',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'readonly': True,
        'type': 'text',
        'name': 'text_name',
        'style': 'width: 50%; line-height: 28px;',
    }))
    roles = forms.CharField(widget=forms.TextInput({
        'readonly': True,
        'type': 'text',
        'name': 'text_name',
        'style': 'width: 50%; line-height: 28px;'
    }))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'roles')