from django.conf import settings
from accounts.forms import LoginForm

class AuthRedirectMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path == '/accounts/login/':
            if request.method == 'GET':
                response = view_func(request, *view_args, **view_kwargs)
                return response
            else:
                print(request.session)
