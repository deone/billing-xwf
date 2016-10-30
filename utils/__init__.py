from django.utils import timezone
from django.forms import ValidationError
from django.conf import settings
from django.core.urlresolvers import reverse

from accounts.models import RechargeAndUsage
from packages.models import PackageSubscription
from payments.models import IndividualPayment

from decimal import Decimal
from datetime import timedelta

def get_captive_url_message(request):
    captive_url = '%s?login_url=%s&continue_url=%s&ap_mac=%s&ap_name=%s&ap_tags=%s&client_mac=%s&client_ip=%s' % (
        reverse('captive'), 
        request.session['login_url'], 
        request.session['continue_url'],
        request.session['ap_mac'],
        request.session['ap_name'],
        request.session['ap_tags'],
        request.session['client_mac'],
        request.session['client_ip']
        )
        
    return "%s%s" % ('Package purchased successfully. You may ', "<a href=" + captive_url + ">log in</a> to browse.")

def increment_data_balance(radcheck, package):
    radcheck.data_balance += Decimal(package.volume)
    radcheck.save()

def get_subscriptions(user, flag):
    if flag == None:
        queryset = user.radcheck.packagesubscription_set.all
    else:
        queryset = user.subscriber.group.grouppackagesubscription_set.all

    return queryset()

def get_balance(radcheck):
    try:
        last_activity = RechargeAndUsage.objects.filter(radcheck=radcheck)[0]
    except IndexError, RechargeAndUsage.DoesNotExist:
        last_activity = None

    if last_activity is not None:
        balance = last_activity.balance
    else:
        balance = 0

    return balance

def charge_subscriber(radcheck, amount, balance, package):
    RechargeAndUsage.objects.create(
        radcheck=radcheck,
        amount=amount,
        balance=balance,
        action='USG',
        activity_id=package.pk
    )

    return True

def check_subscription(radcheck=None, group=None):
    now = timezone.now()

    try:
        if radcheck is not None:
            existing_subscription = radcheck.packagesubscription_set.all()[0]
        if group is not None:
            existing_subscription = group.grouppackagesubscription_set.all()[0]
    except IndexError:
        start = now
    else:
        if existing_subscription.is_valid():
            start = existing_subscription.stop
        else:
            start = now

    return start

def compute_stop_time(start, package_type):
    return start + timedelta(hours=settings.PACKAGE_TYPES_HOURS_MAP[package_type])

def check_balance_and_subscription(radcheck, package):
    amount = -package.price
    balance = get_balance(radcheck)
    if (balance - package.price) >= 0:
        balance = balance - package.price
    else:
        raise ValidationError('Package price is more than balance.', code='insufficient-funds')

    return (check_subscription(radcheck=radcheck), amount, balance)

def save_subscription(radcheck, package, start, amount=None, balance=None, token=None):
    if token is None:
        charge_subscriber(radcheck, amount, balance, package)

    if package.volume != 'Unlimited':
        increment_data_balance(radcheck, package)
    subscription = PackageSubscription.objects.create(radcheck=radcheck, package=package, start=start)

    if token is not None:
        IndividualPayment.objects.create(subscription=subscription, token=token)

    subscription.stop = compute_stop_time(start, package.package_type)
    subscription.save()

    return subscription
