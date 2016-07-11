from decimal import Decimal

from accounts.models import Radacct

def get_volume(package):
    if package.volume != 'Unlimited':
        volume = package.volume
    else:
        volume = 100000

    return volume

def get_subscriptions(user, flag):
    if flag == None:
        queryset = user.radcheck.packagesubscription_set.all
    else:
        queryset = user.subscriber.group.grouppackagesubscription_set.all

    return queryset()

def check_data_balance(subscription):
    """ data_usage = 0
    if subscription.package.volume != 'Unlimited':
        data_limit = Decimal(subscription.package.volume)
    else:
        # Set a data limit of 100000GB for Unlimited plans
        data_limit = 100000

    if 'group' in dir(subscription):
        group_users_usage = [s.user.radcheck.data_usage for s in subscription.group.subscriber_set.all()]
        for du in group_users_usage:
            data_usage += du
    else:
        data_usage = subscription.radcheck.data_usage

    return data_limit > data_usage """

    if 'group' in dir(subscription):
        data_balance = 1
        # data_balance = subscription.group.data_balance
    else:
        data_balance = subscription.radcheck.data_balance

    return data_balance > 0
