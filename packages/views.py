from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from billing.decorators import must_be_individual_user
from accounts.models import Radcheck
from accounts.helpers import md5_password
from .models import Package, InstantVoucher

@ensure_csrf_cookie
def insert_stub(request):
    """ This view is strictly for testing. """
    response = {}
    if request.method == 'POST':
        package = Package.objects.create(package_type=request.POST['package_type'],
            speed=request.POST['speed'], volume=request.POST['volume'], price=request.POST['price'])
        package.__dict__.pop("_state")
        response.update({'code': 200, 'result': package.__dict__})
    else:
        response.update({'status': 'ok'})

    return JsonResponse(response)

@ensure_csrf_cookie
def delete_stub(request):
    """ This view is strictly for testing. """
    response = {}
    if request.method == 'POST':
        package = Package.objects.get(pk=request.POST['package_id'])
        package.delete()
        response.update({'code': 200})
    else:
        response.update({'status': 'ok'})

    return JsonResponse(response)

@ensure_csrf_cookie
def packages(request):
    response = {}
    packages = []
    for p in Package.objects.all():
        string = p.package_type + ' ' + p.speed + ' Mbps ' + str(p.price) + ' GHS'
        tup = (p.pk, string)
        packages.append(tup)
    response.update({'code': 200, 'results': list(packages)})
    return JsonResponse(response)

@ensure_csrf_cookie
def insert_vouchers(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        package_id = request.POST['package_id']

        radcheck = Radcheck.objects.create(username=username,
                                    attribute='MD5-Password',
                                    op=':=',
                                    value=md5_password(password))
        package = Package.objects.get(pk=package_id)

        InstantVoucher.objects.create(radcheck=radcheck, package=package)

    return JsonResponse({'status': 'ok'})

@must_be_individual_user
@login_required
def create_package(request, pk):
    # create package and redirect to /accounts/buy_package/
    print pk
    messages.success(request, 'Package purchased successfully.')
    return redirect('accounts:buy_package')
