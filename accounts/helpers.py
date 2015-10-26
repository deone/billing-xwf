from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives, send_mass_mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import loader

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

def md5_password(password):
    m = hashlib.md5()
    m.update(password)

    return m.hexdigest()

def make_context(user):
    current_site = Site.objects.get_current()

    return {
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'site_name': current_site.name,
        'protocol': 'http',
    }

def send_verification_mail(user):
    context = make_context(user)
    subject_template = 'accounts/verification_subject.txt'
    email_template = 'accounts/verification_email.html'
    subject = loader.render_to_string(subject_template, context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template, context)

    email_message = EmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])

    email_message.send()

def send_group_welcome_mail(lst):
    messages = build_message_list(lst)
    success = send_mass_mail(messages)

    return success

def build_message_list(lst):
    message_list = []

    subject_template = 'accounts/group_member_welcome_subject.txt'
    email_template = 'accounts/group_member_welcome_email.html'
    for user in lst:
        context = make_context(user)
        subject = loader.render_to_string(subject_template, context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template, context)
        message = (subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
        message_list.append(message)

    return tuple(message_list)

def send_vms_request(url, payload):
    get_response = requests.get(url)
    post_response = requests.post(
          url,
          data={'payload': payload},
          headers={"X-CSRFToken": get_response.cookies['csrftoken']},
          cookies=get_response.cookies
        )

    return post_response.json()
