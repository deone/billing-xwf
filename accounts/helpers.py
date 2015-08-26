from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import loader

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

def make_context(request, user):
    current_site = get_current_site(request)

    return {
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'site_name': current_site.name,
        'protocol': 'http',
    }

def send_verification_mail(request, user, subject_template_name, email_template_name):
    context = make_context(request, user)
    subject = loader.render_to_string(subject_template_name, context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])

    email_message.send()
