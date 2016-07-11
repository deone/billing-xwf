from django.utils import timezone
from django.forms import ValidationError
from django.conf import settings

from accounts.models import RechargeAndUsage
from packages.models import PackageSubscription
from payments.models import IndividualPayment

from decimal import Decimal
from datetime import timedelta

def get_volume(package):
    if package.volume != 'Unlimited':
        volume = package.volume
    else:
        volume = 100000

    return volume

def increment_data_balance(radcheck, package):
    volume = get_volume(package)
    radcheck.data_balance += Decimal(volume)
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

    increment_data_balance(radcheck, package)
    subscription = PackageSubscription.objects.create(radcheck=radcheck, package=package, start=start)

    if token is not None:
        IndividualPayment.objects.create(subscription=subscription, token=token)

    subscription.stop = compute_stop_time(start, package.package_type)
    subscription.save()

    return subscription
