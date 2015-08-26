from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings

import hashlib

def auth_and_login(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return True
    else:
        return False

def md5_password(password):
    m = hashlib.md5()
    m.update(password)

    return m.hexdigest()

def send_verification_mail(request, user):
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verification_link = "http://%s%s" % (domain,
        reverse('accounts:verify_email', kwargs={'uidb64': uid, 'token': token}))
    send_mail('Verify Email', verification_link,
        settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
