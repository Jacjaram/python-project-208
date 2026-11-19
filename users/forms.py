from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label='Nombre')
    last_name = forms.CharField(max_length=150, required=True, label='Apellidos')

    username = forms.CharField(
        label='Nombre de usuario',
        help_text='Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.'
    )

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        help_text='Tu contraseña no puede ser demasiado similar a tu otra información personal.'
    )

    password2 = forms.CharField(
        label='Contraseña (confirmación)',
        widget=forms.PasswordInput,
        help_text='Ingresa la misma contraseña que antes, para verificación.'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, label='Nombre')
    last_name = forms.CharField(max_length=150, required=True, label='Apellidos')
    username = forms.CharField(label='Nombre de usuario')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
