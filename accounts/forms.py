from django import forms
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm, AuthenticationForm

from .models import *
from .helpers import md5_password

class CreateAccountForm(forms.Form):
    username = forms.EmailField(label='Email Address', max_length=254,
        widget=forms.EmailInput(attrs={'class': 'mdl-textfield__input'}))
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))
    first_name = forms.CharField(label='First Name', max_length=20, 
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'pattern': '[A-Z,a-z, ]*'}))
    last_name = forms.CharField(label='Last Name', max_length=20, 
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'pattern': '[A-Z,a-z, ]*'}))
    confirm_password = forms.CharField(label='Confirm Password', max_length=20, 
      widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))
    country = forms.ChoiceField(label='Country', choices=Subscriber.COUNTRY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Phone Number', widget=forms.NumberInput(attrs={'class': 'mdl-textfield__input'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateAccountForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CreateAccountForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.", code="password_mismatch")

    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        country = self.cleaned_data['country']
        country_code = Subscriber.COUNTRY_CODES_MAP[country]
        phone_number = country_code + self.cleaned_data['phone_number'][1:]

        user = User.objects.create_user(username, username, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        if not self.user.is_anonymous():
            if self.user.subscriber and self.user.subscriber.is_group_admin:
                Subscriber.objects.create(user=user, group=self.user.subscriber.group,
                    country=country, phone_number=phone_number)
            else:
                Subscriber.objects.create(user=user, country=country, phone_number=phone_number)

        Radcheck.objects.create(username=username,
                                attribute='MD5-Password',
                                op=':=',
                                value=md5_password(password))
        return user

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

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email Address', max_length=254,
        widget=forms.EmailInput(attrs={'class': 'mdl-textfield__input'}))
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))
