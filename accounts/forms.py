import hashlib

from django import forms

from .models import *

class Common(forms.Form):
    # Using EmailField for username is intentional. Username must always be an email address.
    username = forms.EmailField(label='Email Address', max_length=100, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    # We need to ensure strong passwords later.
    password = forms.CharField(label='Password', max_length=100, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class CreateAccountForm(Common):
    first_name = forms.CharField(label='First Name', max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    # We should figure out user's country code somehow, later.
    country = forms.ChoiceField(label='Country', choices=Subscriber.COUNTRY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}))
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', label='Phone Number', max_length=15,
        error_messages = {"invalid": "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."}, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +233567823341'}))
    confirm_password = forms.CharField(label='Confirm Password', max_length=100, 
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super(CreateAccountForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")

    def save(self):
        data = self.cleaned_data
        m = hashlib.md5()
        byte_encode = bytes(data['password'], 'utf-8')
        m.update(byte_encode)
        Radcheck.objects.create(username=data['username'],
                                attribute='MD5-Password',
                                op=':=',
                                value=m.hexdigest())
        return True

class LoginForm(Common):
    pass
