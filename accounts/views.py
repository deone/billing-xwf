from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import CreateAccountForm

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
            new_user = True
            # return redirect('dashboard', new_user)
            return redirect('accounts:dashboard')
    else:
        form = CreateAccountForm()
  
    context = {'form': form}

    return render(request, 'accounts/index.html', context)

def login(request):
    if request.method == 'GET':
        if 'login_url' in request.GET:
            context = {
              'login_url': request.GET['login_url'],
              'continue_url': request.GET['continue_url']
            }
        else:
            context = {}

    return render(request, 'accounts/login.html', context)

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
