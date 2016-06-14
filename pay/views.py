from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings

from billing.decorators import must_be_individual_user
from packages.models import Package

import json
import requests

@must_be_individual_user
@login_required
def index(request, pk):
    current_site = Site.objects.get_current()
    package = Package.objects.get(pk=pk)

    headers = {
        'Content-Type': 'application/json',
        'MP-Master-Key': settings.PAYMENT_MASTER_KEY,
        'MP-Private-Key': settings.PAYMENT_TEST_PRIVATE_KEY,
        'MP-Token': '84ca940ca8ad14a592d4',
    }

    return_url = 'http://%s/accounts/buy_package/' % current_site.domain

    data = '{"invoice": {"total_amount": "' + str(package.price) + '", "description": "' + settings.PAYMENT_DESCRIPTION + '"}, "store": {"name": "' + settings.STORE_NAME + '"}, "actions": {"return_url": "' + return_url + '"}}'

    response = requests.post(settings.PAYMENT_TEST_URL, headers=headers, data=data)
    obj = json.loads(response.content)
    return redirect(obj['response_text'])
