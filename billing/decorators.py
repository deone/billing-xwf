from django.http import Http404

def must_be_group_admin(func):
    def func_wrapper(*args, **kwargs):
        request = args[0]
        if request.user.subscriber.is_group_admin and request.user.subscriber.group is not None:
            return func(*args, **kwargs)
        else:
            raise Http404
    return func_wrapper

def must_be_individual_user(func):
    pass
