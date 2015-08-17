from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from django.http import Http404

from .forms import CreateAccountForm, LoginForm
from .models import Subscriber
from .helpers import auth_and_login, meraki_auth

def index(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            country = form.cleaned_data['country']
            country_code = Subscriber.COUNTRY_CODES_MAP[country]
            phone_number = country_code + str(form.cleaned_data['phone_number'])

            # Create user in Django
            user = User.objects.create_user(username, username, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Save phone_number in Subscriber.
            Subscriber.objects.create(user=user, country=country, phone_number=phone_number)

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

def captive(request):
    context = {'form': LoginForm()}
    if 'login_url' in request.GET:
        context.update({
          'login_url': request.GET['login_url'],
          'success_url': settings.SUCCESS_URL,
        })
    else:
        raise Http404("Login URL is incorrect. Please disconnect and reconnect to the WiFi network to get an accurate URL.")

    return render(request, 'accounts/login.html', context) 

def success(request):
    if logout_url in request.GET:
        context = {'logout_url': request.GET['logout_url']}

    return render(request, 'accounts/index.html', context)

def login(request):
    if request.method == 'POST':
        login_url = request.POST['login_url']
        success_url = request.POST['success_url']

        form = LoginForm(request.POST)

        if form.is_valid():
            email = request.POST['username']
            password = request.POST['password']

            auth = auth_and_login(request, email, password)

            if auth:
                if not settings.SERV_PKG:
                    # Go and buy service package at dashboard.
                    # return redirect(settings.LOGIN_REDIRECT_URL)
                    pass
                    # After buying package, do Meraki auth (automatically?? - can we have user who 
                    # just buys package without intentions of browsing?) 
                    # and redirect to dashboard displaying message in session.
                else:
                    # User has service package, let's attempt Meraki authentication
                    # After successful Meraki auth, user is redirected to dashboard with
                    # message that he is connected and can end his browsing session
                    # by clicking logout_url. logout_url is stored in Session and retrieved
                    # to construct logout link.
                    meraki_auth(request, email, password, success_url)
                
                return redirect(settings.LOGIN_REDIRECT_URL)

        context = {'form': form}
    else:
        context = {'form': LoginForm()}
        if 'login_url' in request.GET:
            context.update({
              'login_url': request.GET['login_url'],
              'success_url': settings.SUCCESS_URL,
            })
        else:
            raise Http404("Login URL is incorrect. Please disconnect and reconnect to the WiFi network to get an accurate URL.")

    return render(request, 'accounts/login.html', context)

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

    if 'auth_message' in request.session:
        context.update({'auth_message': request.session['auth_message']})

    return render(request, 'accounts/dashboard.html', context)
