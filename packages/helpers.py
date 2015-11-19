from django.forms import ValidationError
from django.utils import timezone

from accounts.helpers import get_balance
from accounts.models import RechargeAndUsage

def check_balance_and_subscription(subscriber, package):
    amount = -package.price
    balance = get_balance(subscriber)
    if (balance - package.price) >= 0:
        balance = balance - package.price
    else:
        raise ValidationError('Package price is more than balance.', code='insufficient-funds')

    now = timezone.now()

    try:
        existing_subscription = subscriber.packagesubscription_set.all()[0]
    except IndexError:
        start = now
    else:
        if existing_subscription.is_valid():
            start = existing_subscription.stop
        else:
            start = now

    return {
        'subscriber': subscriber,
        'start': start,
        'stop': None,
        'package': package,
        'amount': amount,
        'balance': balance
    }

def charge_subscriber(subscriber, amount, balance, package):
    RechargeAndUsage.objects.create(
        subscriber=subscriber,
        amount=amount,
        balance=balance,
        action='USG',
        activity_id=package.pk
    )

    return True
