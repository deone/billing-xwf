from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import createAccountForm

def index(request):
    if request.method == 'POST':
        form = createAccountForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = createAccountForm()
  
    context = {'form': form}
    return render(request, 'accounts/index.html', context)
