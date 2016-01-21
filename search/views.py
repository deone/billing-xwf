from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from billing.decorators import must_be_group_admin
from . import get_query

@must_be_group_admin
@login_required
def index(request):
    context = {}
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['username', 'first_name', 'last_name',])
        found_entries = User.objects.filter(entry_query)

    context.update({'users': found_entries})

    return render(request, 'search/results.html', context)
