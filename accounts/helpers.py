from django.contrib.auth import authenticate, login as auth_login

import hashlib
import requests

def auth_and_login(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return True
    else:
        return False

def meraki_auth(request, email, password, success_url):
    """ Attempt authenticating with Meraki. Set message in Session. """
    payload = {'username': email, 'password': password, 'success_url': success_url}
    try:
        r = requests.post(request.POST['login_url'], data=payload)
    except Exception as e:
        key, value = e.args
        request.session['auth_message'] = value
    else:
        request.session['auth_message'] = "You are successfully logged in."

    return

def md5_password(password):
    m = hashlib.md5()
    m.update(password)

    return m.hexdigest()
