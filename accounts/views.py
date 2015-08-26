from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from django.http import Http404
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .forms import CreateAccountForm, LoginForm
from .models import Subscriber
from .helpers import auth_and_login, send_verification_mail

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
    if 'logout_url' in request.GET:
        context = {'logout_url': request.GET['logout_url']}
    else:
        context = {}

    return render(request, 'accounts/success.html', context)

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
            phone_number = country_code + form.cleaned_data['phone_number'][1:]

            # Create user in Django
            user = User.objects.create_user(username, username, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Save phone_number in Subscriber.
            Subscriber.objects.create(user=user, country=country, phone_number=phone_number)

            # Save username and password in RADIUS radcheck.
            form.save()

            # Send verification mail here
            subject_template = 'accounts/verification_subject.txt'
            email_template = 'accounts/verification_email.html'

            send_verification_mail(request, user, subject_template, email_template)

            # We need to call login here so that our dashboard can have user's details.
            auth = auth_and_login(request, user.username, form.cleaned_data['password'])
            if auth:
                return redirect('accounts:dashboard')
    else:
        form = CreateAccountForm()
  
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
    if not request.user.subscriber.email_verified:
        context = {'verified': False}

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
