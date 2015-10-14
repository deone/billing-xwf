from django import forms
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm, AuthenticationForm
from django.conf import settings
from django.utils import timezone

from .models import *
from .helpers import md5_password, exceeds_max_user_count, get_group_name_max_allowed_users

class CreateUserForm(forms.Form):
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
    country = forms.ChoiceField(label='Country', choices=Subscriber.COUNTRY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Phone Number', validators=[phone_regex],
        widget=forms.NumberInput(attrs={'class': 'mdl-textfield__input'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateUserForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.", code="password_mismatch")

        if not self.user.is_anonymous() and self.user.subscriber.group is not None:
            group_name, max_user_count = get_group_name_max_allowed_users(self.user.subscriber.group)
            if exceeds_max_user_count(self.user.pk, group_name, max_user_count):
                if not settings.EXCEED_MAX_USER_COUNT:
                    raise forms.ValidationError(
                        "You are not allowed to create more users than your group threshold. Your group threshold is set to %s."
                      % str(self.user.subscriber.group.max_no_of_users), code="exceeds_threshold")

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

        Radcheck.objects.create(user=user,
                                username=username,
                                attribute='MD5-Password',
                                op=':=',
                                value=md5_password(password))
        return user

class EditUserForm(forms.Form):
    username = forms.EmailField(label='Email Address', max_length=254,
        widget=forms.EmailInput(attrs={'class': 'mdl-textfield__input'}))
    first_name = forms.CharField(label='First Name', max_length=20, 
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'pattern': '[A-Z,a-z, ]*'}))
    last_name = forms.CharField(label='Last Name', max_length=20, 
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'pattern': '[A-Z,a-z, ]*'}))
    phone_number = forms.CharField(label='Phone Number', required=False, validators=[phone_regex],
        widget=forms.NumberInput(attrs={'class': 'mdl-textfield__input'}))

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
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))

    def save(self):
        user = super(ResetPasswordForm, self).save()
        subscriber = Radcheck.objects.get(username=user.username)
        subscriber.value = md5_password(self.cleaned_data['new_password1'])
        subscriber.save()

class PasswordResetEmailForm(PasswordResetForm):
    email = forms.EmailField(label='Email Address', max_length=50, widget=forms.EmailInput(attrs={'class': 'mdl-textfield__input'}))

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        email = cleaned_data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Email does not exist.")

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email Address', max_length=254,
        widget=forms.EmailInput(attrs={'class': 'mdl-textfield__input'}))
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))

class BulkUserUploadForm(forms.Form):
    user_list = forms.FileField()

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

        group_name, max_user_count = get_group_name_max_allowed_users(self.user.subscriber.group)

        if exceeds_max_user_count(self.user.pk, group_name, max_user_count, line_count):
            if not settings.EXCEED_MAX_USER_COUNT:
                raise forms.ValidationError(
                    "You are not allowed to create more users than your group threshold. Your group threshold is set to %s."
                  % str(self.user.subscriber.group.max_no_of_users))

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
