def get_subscriptions(user, flag):
    if flag == None:
        queryset = user.radcheck.packagesubscription_set.all
    else:
        queryset = user.subscriber.group.grouppackagesubscription_set.all

    return queryset()
