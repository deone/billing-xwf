from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import *

help_text = "Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only."

class SubscriberInline(admin.StackedInline):
    model = Subscriber
    can_delete = False
    verbose_name_plural = 'subscribers'

class AccountsUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(AccountsUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = help_text

class AccountsUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(AccountsUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = help_text

class AccountsUserAdmin(UserAdmin):
    form = AccountsUserChangeForm
    add_form = AccountsUserCreationForm
    inlines = (SubscriberInline, )

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
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

class AccessPointAdminForm(forms.ModelForm):

    def clean(self):
        if self.cleaned_data['group'] is not None and self.cleaned_data['status'] == 'PUB':
            raise forms.ValidationError("Group Access Points cannot be public.")

        return self.cleaned_data

class AccessPointAdmin(admin.ModelAdmin):
    form = AccessPointAdminForm

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, AccountsUserAdmin)
admin.site.register(GroupAccount)
admin.site.register(AccessPoint, AccessPointAdmin)
