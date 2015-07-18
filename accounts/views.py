from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings

from .forms import CreateAccountForm, LoginForm

def index(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            # Create user in Django
            user = User.objects.create_user(
                form.cleaned_data['email'], form.cleaned_data['email'], form.cleaned_data['password']
            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            # user.phone_number = form.cleaned_data['phone_number']
            user.save()
            # Save username and password in RADIUS radcheck.
            form.save()

            # We need to call login here so that our dashboard can have user's details.
            auth = auth_and_login(request, user.username, form.cleaned_data['password'])
            if auth:
                return redirect('accounts:dashboard')
    else:
        form = CreateAccountForm()
  
    context = {'form': form}

    return render(request, 'accounts/index.html', context)

def auth_and_login(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return True
    else:
        return False

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            auth = auth_and_login(request, email, password)

            if auth:
                return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            context = {'form': form}
    else:
        if request.GET:
            print(request.GET)
            context = {
              'form': LoginForm(),
              'login_url': request.GET['login_url'],
              'continue_url': request.GET['continue_url']
            }

    return render(request, 'accounts/login.html', context)

    """if auth:
        # Now that we've logged in, we need to check whether user has valid service package
        # before attempting a Meraki authentication.
        # Here's a stub to check service package
        if settings.SERV_PKG:
            # User has service package, we can now auth at Meraki
            print("true")
        else:
            # User doesn't have a service package, he has to buy one
            pass
    else:
        # Display error on user form
        pass"""


def dashboard(request):
    # Let's remember to use User methods here and in the template, instead of attributes.
    """
    if new_user:
        welcome_msg = ""
        context = {'message': welcome_msg}
    else:
        context = {}"""

    context = {}
    return render(request, 'accounts/dashboard.html', context)
