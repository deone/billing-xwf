from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings

from billing.decorators import must_be_individual_user
from packages.models import Package

import json
import requests

@login_required
@must_be_individual_user
def index(request, package_pk):
    current_site = Site.objects.get_current()
    package = Package.objects.get(pk=package_pk)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic cnNrd3R3dWw6ZmVsd3NrZHU=',
    }

    return_url = 'http://%s%s' % (current_site.domain, reverse('packages:create_subscription', kwargs={'package_pk': package_pk}))
    data = '{"invoice": {"items": {"item_0": {"name": "Spectra Internet Package - ' + str(package) + '", "quantity": 1, "unit_price": "' + str(package.price) + '", "total_price": "' + str(package.price) + '"}}, "total_amount":' + str(package.price) + ', "description": "Internet Service"}, "store": {"name": "' + settings.STORE_NAME + '"}, "actions": {"return_url": "' + return_url + '"}}'

    response = requests.post(settings.CHECKOUT_URL, headers=headers, data=data)
    return redirect(response.json()['response_text'])