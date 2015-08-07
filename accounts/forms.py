
from django import forms
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm

from .models import *
from .helpers import md5_password

class Common(forms.Form):
    # Using EmailField for username is intentional. Username must always be an email address.
    username = forms.EmailField(label='Email Address', max_length=50, 
        widget=forms.EmailInput(attrs={'class': 'mdl-textfield__input'}))
    # We need to ensure strong passwords later.
    password = forms.CharField(label='Password', max_length=20, 
        widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))

class CreateAccountForm(Common):
    first_name = forms.CharField(label='First Name', max_length=20, 
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'pattern': '[A-Z,a-z, ]*'}))
    last_name = forms.CharField(label='Last Name', max_length=20, 
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'pattern': '[A-Z,a-z, ]*'}))
    confirm_password = forms.CharField(label='Confirm Password', max_length=20, 
      widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))
    country = forms.ChoiceField(label='Country', choices=Subscriber.COUNTRY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    phone_number = forms.IntegerField(label='Phone Number', widget=forms.NumberInput(attrs={'class': 'mdl-textfield__input'}))

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
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))

    def save(self):
        user = super(ResetPasswordForm, self).save()
        subscriber = Radcheck.objects.get(username=user.username)
        subscriber.value = md5_password(self.cleaned_data['new_password1'])
        subscriber.save()

class PasswordResetEmailForm(PasswordResetForm):
    email = forms.EmailField(label='Email Address', max_length=50, widget=forms.EmailInput(attrs={'class': 'mdl-textfield__input'}))

class LoginForm(Common):
    pass
