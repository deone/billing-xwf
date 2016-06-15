from django.forms import ValidationError
from django.utils import timezone

from accounts.helpers import get_balance
from accounts.models import RechargeAndUsage

from .models import PackageSubscription, compute_stop

def create_package(radcheck, package, start):
    subscription = PackageSubscription.objects.create(radcheck=radcheck, package=package, start=start)
    subscription.stop = compute_stop(subscription.start, package.package_type)
    subscription.save()
    
    return subscription

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

def check_balance_and_subscription(radcheck, package):
    amount = -package.price
    balance = get_balance(radcheck)
    if (balance - package.price) >= 0:
        balance = balance - package.price
    else:
        raise ValidationError('Package price is more than balance.', code='insufficient-funds')

    return (check_subscription(radcheck=radcheck), amount, balance)

def charge_subscriber(radcheck, amount, balance, package):
    RechargeAndUsage.objects.create(
        radcheck=radcheck,
        amount=amount,
        balance=balance,
        action='USG',
        activity_id=package.pk
    )

    return True

def update_cleaned_data(data, dct):
    return data.update(dct)
