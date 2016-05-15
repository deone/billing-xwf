from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django import forms

from .models import *
from .helpers import send_verification_mail, md5_password

help_text = "Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only."

class SubscriberAdminForm(forms.ModelForm):

    class Meta:
        model = Subscriber
        exclude = ()

    def clean(self):
        cleaned_data = super(SubscriberAdminForm, self).clean()

        if cleaned_data['group'] is None and cleaned_data['is_group_admin'] is True:
            raise forms.ValidationError("User must belong to a group to be group admin.")

        return cleaned_data

    def save(self, commit=True):
        subscriber = super(SubscriberAdminForm, self).save(commit=False)
        try:
            existing_subscriber = Subscriber.objects.get(pk=subscriber.id)
        except Subscriber.DoesNotExist:
            is_new = True
        else:
            is_new = False
            
        country_code = Subscriber.COUNTRY_CODES_MAP[subscriber.country]

        if not subscriber.phone_number.startswith(country_code):
            subscriber.phone_number = country_code + subscriber.phone_number[1:]

        subscriber.save()

        if is_new:
            send_verification_mail(subscriber.user)

        return subscriber

class SubscriberInline(admin.StackedInline):
    model = Subscriber
    form = SubscriberAdminForm
    can_delete = False
    verbose_name_plural = 'subscribers'

class AccountsUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(AccountsUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Email Address"
        self.fields['username'].help_text = help_text

    def save(self, commit=True):
        user = super(AccountsUserCreationForm, self).save(commit=False)
        user.email = user.username
        user.save()

        # This should happen only if user is a subscriber. But we haven't been able
        # to figure that out because user.save() is called before subscriber.save().
        # For now, we have to create Radcheck objects even for Spectra admin users.
        md5 = md5_password(self.cleaned_data['password1'])
        Radcheck.objects.create(user=user,
                                username=self.cleaned_data['username'],
                                attribute='MD5-Password',
                                op=':=',
                                value=md5)

        return user

class AccountsUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(AccountsUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Email Address"
        self.fields['username'].help_text = help_text

def user_group(obj):
    if obj.subscriber is not None:
        if obj.subscriber.group is not None:
            return obj.subscriber.group.name
user_group.short_description = 'Group'
user_group.admin_order_field = 'subscriber__group__name'

class AccountsUserAdmin(UserAdmin):
    form = AccountsUserChangeForm
    add_form = AccountsUserCreationForm
    inlines = (SubscriberInline, )
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'date_joined', user_group)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'subscriber__is_group_admin')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'subscriber__group__name')
    ordering = ('-date_joined',)

    """
    Original
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    ) """
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

class AccessPointAdminForm(forms.ModelForm):

    class Meta:
        model = AccessPoint
        fields = ('name', 'group', 'mac_address', 'status')

def ap_group(obj):
    if obj.group is not None:
        return obj.group.name

ap_group.short_description = 'Group'
ap_group.admin_order_field = 'group__name'

class AccessPointAdmin(admin.ModelAdmin):
    form = AccessPointAdminForm
    list_display = ('name', 'mac_address', 'status', ap_group)
    search_fields = ('name', 'status', 'group__name')

class GroupAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_no_of_users')
    search_fields = ('name',)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, AccountsUserAdmin)
admin.site.register(GroupAccount, GroupAccountAdmin)
admin.site.register(AccessPoint, AccessPointAdmin)
