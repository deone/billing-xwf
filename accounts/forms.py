
from django import forms
from django.contrib.auth.forms import SetPasswordForm

from .models import *
from .helpers import md5_password

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
        error_messages = {"invalid": "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."}, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 0567823341'}))
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
        Radcheck.objects.create(username=data['username'],
                                attribute='MD5-Password',
                                op=':=',
                                value=md5_password(self.cleaned_data['password']))
        return True

class ResetPasswordForm(SetPasswordForm):

  def save(self):
      user = super(ResetPasswordForm, self).save()
      subscriber = Radcheck.objects.get(username=user.username)
      subscriber.value = md5_password(self.cleaned_data['new_password1'])
      subscriber.save()

class LoginForm(Common):
    pass
