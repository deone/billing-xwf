from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import CreateAccountForm

def index(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CreateAccountForm()
  
    context = {'form': form}
    return render(request, 'accounts/index.html', context)

def login(request):
    return render(request, 'accounts/login.html')
