from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.conf import settings
from django.http import Http404
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.generic import ListView

from .forms import CreateUserForm, LoginForm, BulkUserUploadForm, EditUserForm
from .models import Subscriber
from .helpers import *

from packages.forms import PackageSubscriptionForm
from packages.models import Package

def captive(request):
    context = {'form': LoginForm()}

    if 'error_message' in request.GET:
        context.update({
            'error_message': request.GET['error_message']
        })

    if 'login_url' in request.GET:
        context.update({
          'login_url': request.GET['login_url'],
          'success_url': settings.SUCCESS_URL,
        })
    else:
        raise Http404("Login URL is incorrect. Please disconnect and reconnect to the WiFi network to get an accurate URL.")

    return render(request, 'accounts/login.html', context)

def success(request):
    if 'logout_url' in request.GET:
        context = {'logout_url': request.GET['logout_url']}
    else:
        context = {}

    return render(request, 'accounts/success.html', context)

def index(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST, user=AnonymousUser())
        if form.is_valid():
            user = form.save()

            # Send verification mail here - we might
            # need to wrap this in a try - except block
            send_verification_mail(user)

            # We need to call login here so that our
            # dashboard can have user's details.
            auth = auth_and_login(request, user.username,
                form.cleaned_data['password'])
            if auth:
                return redirect('accounts:dashboard')
    else:
        form = CreateUserForm(user=request.user)
  
    context = {'form': form}

    return render(request, 'accounts/index.html', context)

@login_required
def dashboard(request):
    # Let's remember to use User methods here and in the template, instead of attributes.
    """
    if new_user:
        welcome_msg = ""
        context = {'message': welcome_msg}
    else:
        context = {}"""

    context = {}

    if request.user.subscriber.email_verified:
        context.update({'verified': True})

    return render(request, 'accounts/dashboard.html', context)

def verify_email(request, uidb64=None, token=None):
    assert uidb64 is not None and token is not None
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    a, b = token.split('-')

    if user is not None and len(b) == 20:
        subscriber = user.subscriber
        subscriber.email_verified = True
        subscriber.date_verified = timezone.now()
        subscriber.save()

        return redirect('accounts:dashboard')
    else:
        raise Http404("Verification link incorrect.")

@login_required
def resend_mail(request):
    send_verification_mail(request.user)
    return redirect('accounts:dashboard')

@login_required
def add_user(request):
    context = {}

    if request.method == 'POST':
        form = CreateUserForm(request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            success = send_group_welcome_mail([user])
            messages.success(request, 'User added successfully.')
            return redirect('accounts:add_user')
    else:
        form = CreateUserForm(user=request.user)

    context.update({'form': form})
    return render(request, 'accounts/add_user.html', context)

@login_required
def edit_user(request, pk=None):
    context = {}

    user = User.objects.get(pk=pk)

    if user.subscriber.phone_number:
        phone_number = '0' + user.subscriber.phone_number[4:]
    else:
        phone_number = ""

    dct = {
        'username': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': phone_number
        }

    if request.method == 'POST':
        form = EditUserForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(user)
            messages.success(request, 'User changed successfully.')
            return redirect('accounts:view_users')
    else:
        form = EditUserForm(user=request.user, initial=dct)

    context.update({'form': form})
    return render(request, 'accounts/edit_user.html', context)

@login_required
def upload_user_list(request):
    context = {}

    if request.method == 'POST':
      form = BulkUserUploadForm(request.POST, request.FILES, user=request.user)
      if form.is_valid():
          user_list = form.save()
          success = send_group_welcome_mail(user_list)
          messages.success(request, 'Users added successfully.')
          return redirect('accounts:upload_user_list')
    else:
        form = BulkUserUploadForm(user=request.user)

    context.update({
      'form': form, 
      'file_length': settings.MAX_FILE_LENGTH
    })
    return render(request, 'accounts/upload_user_list.html', context)

@login_required
def buy_package(request):
    context = {}
    packages = [(p.id, p) for p in Package.objects.all()]
    if request.method == "POST":
        form = PackageSubscriptionForm(request.POST, user=request.user, packages=packages)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package purchased successfully.')
            return redirect('accounts:buy_package')
    else:
        form = PackageSubscriptionForm(user=request.user, packages=packages)

    context.update({'form': form})
    return render(request, 'accounts/buy_package.html', context)

""" def view_users(request):
    context = {}
    group_name = request.user.subscriber.group.name
    users = [(u.id, u) for u in User.objects.filter(
      subscriber__group__name=group_name).exclude(pk=request.user.pk)]
    if request.method == "POST":
        form = UserListForm(request.POST, users=users)
        if form.is_valid():
            form.save()
            messages.success(request, 'Users deactivated successfully.')
            return redirect('accounts:view_users')
    else:
        form = UserListForm(users=users)

    context.update({'form': form})
    return render(request, 'accounts/user_list.html', context) """

class UserList(ListView):
    template_name = 'accounts/user_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserList, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(subscriber__group=request.user.subscriber.group).exclude(pk=request.user.pk)
        return render(request, self.template_name, {'users': users})

    # def get_queryset(self):
        # return User.objects.filter(subscriber__group=self.request.user.subscriber.group)

def toggle_active(request, pk=None):
    user = User.objects.get(pk=pk)

    if user.is_active: 
        user.is_active = False
    else:
        group_name, max_user_count = get_group_name_max_allowed_users(request.user.subscriber.group)
        if exceeds_max_user_count(request.user.pk, group_name, max_user_count):
            if not settings.EXCEED_MAX_USER_COUNT:
                messages.error(request,
                    "You are not allowed to create more users than your group threshold. Your group threshold is set to %s." % max_user_count)
                return redirect('accounts:view_users')

        user.is_active = True

    user.save()
    return redirect('accounts:view_users')
