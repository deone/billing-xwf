def get_subscriptions(user, flag):
    subscriptions = None

    if flag == None:
        queryset = user.radcheck.packagesubscription_set.all
    else:
        queryset = user.subscriber.group.grouppackagesubscription_set.all

    try:
        subscriptions = queryset()
    except IndexError:
        pass

    return subscriptions
