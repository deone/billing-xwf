from django import forms
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader

from .models import *
from .helpers import md5_password, send_api_request

from utils import get_balance

import requests

class CreateUserForm(forms.Form):
    username = forms.CharField(label='Phone Number', max_length=10, validators=[phone_regex],
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='Confirm Password', max_length=20, 
      widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateUserForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        cleaned_data = super(CreateUserForm, self).clean()
        username = cleaned_data.get('username')
        if username[:3] not in settings.PHONE_NUMBER_PREFIXES:
            raise forms.ValidationError('Provide a valid phone number.', code='number_invalid')

        return username

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("username")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError("User already exists")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match", code="password_mismatch")

        if not self.user.is_anonymous() and self.user.subscriber.group is not None:
            group = self.user.subscriber.group
            # Refactor this. It is repeated in BulkUserUploadForm
            if group.max_user_count_reached():
                if not settings.EXCEED_MAX_USER_COUNT:
                    raise forms.ValidationError(
                        "You are not allowed to create more users than your group threshold. Your group threshold is set to %s."
                      % str(group.max_no_of_users))
            
    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        country = 'GHA'
        phone_number = Subscriber.COUNTRY_CODES_MAP[country] + self.cleaned_data['username'][1:]

        user = User.objects.create_user(username, username, password)

        if not self.user.is_anonymous():
            if self.user.subscriber and self.user.subscriber.is_group_admin:
                Subscriber.objects.create(user=user, group=self.user.subscriber.group,
                    country=country, phone_number=phone_number)
        else:
            Subscriber.objects.create(user=user, country=country, phone_number=phone_number)

        Radcheck.objects.create(user=user,
                                username=username,
                                attribute='MD5-Password',
                                op=':=',
                                value=md5_password(password))
        return user

class EditUserForm(forms.Form):
    username = forms.EmailField(label='Email Address', max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', max_length=20, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=20, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Phone Number', required=False, validators=[phone_regex],
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditUserForm, self).__init__(*args, **kwargs)

    def save(self, user):
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']

        user.username = username
        user.email = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Save subscriber
        if self.cleaned_data['phone_number']:
            country_code = Subscriber.COUNTRY_CODES_MAP[user.subscriber.country]
            user.subscriber.phone_number = country_code + self.cleaned_data['phone_number'][1:]
            user.subscriber.save()

        # Save radcheck
        user.radcheck.username = username
        user.radcheck.save()

        return user

class ResetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def save(self):
        user = super(ResetPasswordForm, self).save()
        subscriber = Radcheck.objects.get(username=user.username)
        subscriber.value = md5_password(self.cleaned_data['new_password1'])
        subscriber.save()

class PasswordResetSMSForm(forms.Form):
    username = forms.CharField(label='Phone Number', max_length=10, validators=[phone_regex],
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super(PasswordResetSMSForm, self).clean()
        username = cleaned_data.get('username')

        model = get_user_model()
        try:
            if username is not None:
                user = model._default_manager.get(username__iexact=username)
        except model.DoesNotExist:
            raise forms.ValidationError("Phone number does not exist.")

    def send_sms(self, sms_template, custom_sms_sender, context):
        phone_number = '+233' + context['username'][1:]
        message = loader.render_to_string(sms_template, context)
        params = settings.SMS_PARAMS

        params.update({'To': phone_number, 'Content': message})
        if custom_sms_sender:
            params.update({'From': custom_sms_sender})

        response = requests.get(settings.SMS_URL, params)
        return response
        
    def get_users(self, username, action=None):
        active_users = get_user_model()._default_manager.filter(
            username__iexact=username, is_active=True)
        if action is not None:
            return (u for u in active_users)
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name=None,
             email_template_name=None,
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             sms_template=None, custom_sms_sender=None):

        username = self.cleaned_data["username"]

        if sms_template is None:
            sms_template = 'accounts/sms_reset_password.txt'
            users = self.get_users(username)
        else:
            users = self.get_users(username, action='create')

        for user in users:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'username': user.username,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            
            return self.send_sms(sms_template, custom_sms_sender, context)

class CambiumLoginForm(AuthenticationForm):
    ga_user = forms.CharField(label='Phone Number', max_length=10, validators=[phone_regex], 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    ga_pass = forms.CharField(label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Phone Number', max_length=10, validators=[phone_regex], 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class BulkUserUploadForm(forms.Form):
    user_list = forms.FileField(label='User List')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BulkUserUploadForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(BulkUserUploadForm, self).clean()
        _file = cleaned_data.get('user_list')

        if not _file.name.endswith('.csv'):
            raise forms.ValidationError("Please upload a CSV file.")

        lines = _file.readlines()
        line_count = len(lines)

        if line_count > settings.MAX_FILE_LENGTH:
            raise forms.ValidationError(
                "Uploaded file should not have more than %s lines. It has %s." % (
                  str(settings.MAX_FILE_LENGTH), str(line_count)))

        group = self.user.subscriber.group

        if group.max_user_count_reached() or line_count > group.available_user_slots_count():
            if not settings.EXCEED_MAX_USER_COUNT:
                raise forms.ValidationError(
                    "You are not allowed to create more users than your group threshold. Your group threshold is set to %s."
                  % str(group.max_no_of_users))

        lst = []
        created_user_emails = [user.email for user in User.objects.filter(
          subscriber__group__name=self.user.subscriber.group.name)]

        for line in lines:
            dct = {}
            try:
                first_name, last_name, email = line.split(',')
            except ValueError:
                raise forms.ValidationError("File line has too many or too few values. Please check file.")
            else:
                email = email.strip()
                first_name = first_name.strip()
                last_name = last_name.strip()

                if email in created_user_emails:
                    raise forms.ValidationError("Duplicate email found. %s already exists." % email)

                dct.update({
                  'username': email,
                  'email': email,
                  'first_name': first_name.title(),
                  'last_name': last_name.title()
                })

            lst.append(dct)

        return lst

    def save(self):
        lst = self.cleaned_data

        now = timezone.now()
        user_list = []

        for dct in lst:
            user = User.objects.create(**dct)
            Subscriber.objects.create(group=self.user.subscriber.group,
                country=self.user.subscriber.country, email_verified=True, user=user, date_verified=now)
            Radcheck.objects.create(user=user, username=user.email, attribute='MD5-Password', op=':=', value="")
            user_list.append(user)

        return user_list

""" class RechargeAccountForm(forms.Form):
    pin = forms.CharField(label="PIN", max_length=14, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RechargeAccountForm, self).__init__(*args, **kwargs)

    def clean_pin(self):
        cleaned_data = super(RechargeAccountForm, self).clean()

        pin = cleaned_data.get('pin')

        if len(pin) != 14:
            raise forms.ValidationError("PINs cannot be shorter than 14 characters.", code="invalid-pin-length")

        # Redeem voucher
        url = settings.VOUCHER_REDEEM_URL
        recharge = send_api_request(url, {'pin': pin})

        if recharge['code'] == 500:
            raise forms.ValidationError(recharge['message'], code="used-pin")
        elif recharge['code'] == 404:
            raise forms.ValidationError(recharge['message'], code="invalid-pin")

        return pin

    def save(self):
        voucher = send_api_request(settings.VOUCHER_REDEEM_URL, self.cleaned_data)
        balance = get_balance(self.user.radcheck)

        amount = voucher['value']
        balance = balance + amount
        activity_id = voucher['serial_number']

        RechargeAndUsage.objects.create(
            radcheck=self.user.radcheck,
            amount=amount,
            balance=balance,
            action='REC',
            activity_id=activity_id
        )

        return voucher """