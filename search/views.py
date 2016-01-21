from django.shortcuts import render
from django.contrib.auth.models import User

from . import get_query

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
