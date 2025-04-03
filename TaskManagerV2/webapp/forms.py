from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        label="First Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        label="Last Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )
    address = forms.CharField(
        max_length=255, 
        required=True, 
        label="Address",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )
    telephone = forms.CharField(
        max_length=20, 
        required=True, 
        label="Telephone",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )

    # Override labels for username/password fields if you like
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 
            'address', 'telephone', 'password1', 'password2'
        )

class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap form-control class and placeholder for floating labels
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' '
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' '
        })