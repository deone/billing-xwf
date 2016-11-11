from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
from django.utils.deprecation import RemovedInDjango20Warning

from twilio.rest import TwilioRestClient

from billing.decorators import *

from utils import get_subscriptions, get_captive_url

from .forms import CreateUserForm, LoginForm, BulkUserUploadForm, EditUserForm, RechargeAccountForm
from .models import Subscriber, NetworkParameter
from .helpers import *

""" <QueryDict: {
u'client_ip': [u'10.8.0.78'], 
u'login_url': [u'https://n110.network-auth.com/splash/login?mauth=MMNsInqn8ksWBR7PgbfBkWG8PawzJm1wi4PE9pDEUdU1qFuHtYczZmRJFJ3dD7AJvl9DRppZnJAZOTA7L3KbzaX4WgwU74t5ibpIJBwHJ-eg5RnL4Hct5hs7i1UIRBH6kbeL9X4hlcFLZKvkaV2mpeP_hX9hxs5jGl_C0N6oWtoQtUjskrMcnBaA&continue_url=http%3A%2F%2Fgoogle.com%2F'], 
u'continue_url': [u'http://google.com/'], 
u'ap_tags': [u'office-accra recently-added'], 
u'ap_mac': [u'00:18:0a:f2:de:20'], 
u'ap_name': [u'Spectra-HQ-NOC'], 
u'client_mac': [u'4c:eb:42:ce:6c:3d']}> """

def captive(request):
    """
    We need users to _always_ be able to launch the captive portal from the dashboard
    if they are not logged in to browse and end their browsing session if they are logged in to browse.
    The only requirement is that the captive portal loads.

    - Attempt fetching network parameter from DB with `client_mac`.
    - If this fails, save GET params in session and set logout_key to None.
    - Else, update DB entry with GET params
    """
    # Always save client_mac in session so that success() can use it to update NetworkParameter
    if 'client_mac' not in request.session:
    	request.session['client_mac'] = request.GET['client_mac']

    try:
        np = NetworkParameter.objects.get(client_mac=request.GET['client_mac'])
    except NetworkParameter.DoesNotExist:
        # Store request.GET parameters in session
        if not 'login_url' in request.session:
            request.session['login_url'] = request.GET['login_url']
            request.session['continue_url'] = request.GET['continue_url']
            request.session['ap_mac'] = request.GET['ap_mac']
            request.session['ap_name'] = request.GET['ap_name']
            request.session['ap_tags'] = request.GET['ap_tags']
            request.session['client_ip'] = request.GET['client_ip']
            request.session['logout_url'] = None
    else:
        np.login_url = request.GET['login_url']
        np.continue_url = request.GET['continue_url']
        np.ap_mac = request.GET['ap_mac']
        np.ap_name = request.GET['ap_name']
        np.client_mac = request.GET['client_mac']
        np.client_ip = request.GET['client_ip']
	np.logout_url = None
        np.save()

    context = {'form': LoginForm()}
    
    if 'error_message' in request.GET:
        context.update({
            'error_message': request.GET['error_message']
        })

    if 'login_url' in request.GET:
        context.update({
          'login_url': request.GET['login_url'],
          'success_url': settings.SUCCESS_URL,
        })
    else:
        raise Http404("Login URL is incorrect. Please disconnect and reconnect to the WiFi network to get an accurate URL.")

    return render(request, 'captive.html', context)

def success(request):
    np = NetworkParameter.objects.get(client_mac=request.session['client_mac'])
    np.logout_url = request.GET['logout_url']
    np.save()

    context = {'logout_url': request.GET.get('logout_url', None)}

    return render(request, 'accounts/success.html', context)

def create(request):
    # print request.COOKIES
    # We need to implement a logout page here. Users should be able to come here
    # and get a logout link to terminate their browsing session. It would be really
    # helpful if we set 'logout_url' as a cookie after user is authenticated in captive()
    # and delete this cookie when the user clicks the link to log out.
    if request.method == 'POST':
        form = CreateUserForm(request.POST, user=AnonymousUser())
        if form.is_valid():
            user = form.save()
            
            # Send verification sms
            # phone_number = user.subscriber.phone_number
            # client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            # client.messages.create(to=phone_number, from_=settings.TWILIO_NUMBER, body=settings.WELCOME_SMS)

            # Let's save network parameters here
            login_url = request.session.get('login_url', None)
            if login_url:
                NetworkParameter.objects.create(
                    subscriber=user.subscriber,
                    login_url=request.session['login_url'],
                    continue_url=request.session['continue_url'],
                    ap_mac=request.session['ap_mac'],
                    ap_name=request.session['ap_name'],
                    ap_tags=request.session['ap_tags'],
                    client_mac=request.session['client_mac'],
                    client_ip=request.session['client_ip'],
                    )

            # We need to call login here so that our
            # dashboard can have user's details.
            auth = auth_and_login(request, user.username,
                form.cleaned_data['password'])
            if auth:
                return redirect('index')
    else:
    	form = CreateUserForm(user=request.user)
  
    context = {'form': form}

    return render(request, 'accounts/create.html', context)

@login_required
def index(request):
    # Let's remember to use User methods here and in the template, instead of attributes.
    """
    if new_user:
        welcome_msg = ""
        context = {'message': welcome_msg}
    else:
        context = {}"""

    context = {}

    # Get subscriptions.
    subscriptions = list(get_subscriptions(request.user, request.user.subscriber.group))

    # Get subscriptions with stop time < now.
    expired_subscriptions = [s for s in subscriptions if s.stop < timezone.now()]

    # Remove expired subscriptions from subscriptions list so we have active and unused subscriptions
    for es in expired_subscriptions:
        subscriptions.remove(es)

    # Get active subscription
    active_subscription = subscription_is_unlimited = None
    if subscriptions:
        active_subscription = subscriptions.pop()
        if active_subscription.package.volume == 'Unlimited':
            subscription_is_unlimited = True

    context.update({'active_subscription': active_subscription})

    # Group member don't see subscription history
    if request.user.subscriber.group == None or request.user.subscriber.is_group_admin:
        context.update({
          'expired_subscriptions': expired_subscriptions,
          'unused_subscriptions': subscriptions,
          'subscription_is_unlimited': subscription_is_unlimited
          })

    if request.user.subscriber.email_verified:
        context.update({'verified': True})

    # Open captive portal from dashboard.
    # This should only happen if user isn't already logged in.
    np = NetworkParameter.objects.get(subscriber=request.user.subscriber)
    if np.logout_url is None:
        context.update({'captive_url': get_captive_url(request.user.subscriber)})

    # End browsing session from dashboard.
    np = NetworkParameter.objects.get(subscriber=request.user.subscriber)
    context.update({'logout_url': np.logout_url})

    return render(request, 'accounts/index.html', context)

def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            current_app=None, extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': 'Password reset complete',
    }

    captive_url = get_captive_url(request.session)
    context.update({'captive_url': captive_url})

    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)

@csrf_protect
def password_reset(request, is_admin_site=False, extra_context=None, current_app=None, 
                        template_name=None, password_reset_form=None, post_reset_redirect=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'request': request,
            }
            if is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 2.0.",
                    RemovedInDjango20Warning, 3
                )
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': 'Password reset',
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)

def verify_email(request, uidb64=None, token=None):
    assert uidb64 is not None and token is not None
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    a, b = token.split('-')

    if user is not None and len(b) == 20:
        subscriber = user.subscriber
        subscriber.email_verified = True
        subscriber.date_verified = timezone.now()
        subscriber.save()

        return redirect('index')
    else:
        raise Http404("Verification link incorrect.")

@login_required
def resend_mail(request):
    send_verification_mail(request.user)
    return redirect('index')

@login_required
@must_be_group_admin
def add_user(request):
    context = {}

    if request.method == 'POST':
        form = CreateUserForm(request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            success = send_group_welcome_mail([user])
            messages.success(request, 'User added successfully.')
            return redirect('accounts:add_user')
    else:
        form = CreateUserForm(user=request.user)

    context.update({'form': form})
    return render(request, 'accounts/add_user.html', context)

@login_required
def edit_user(request, pk=None):
    context = {}

    user = User.objects.get(pk=pk)

    if user.subscriber.phone_number:
        phone_number = '0' + user.subscriber.phone_number[4:]
    else:
        phone_number = ""

    dct = {
        'username': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': phone_number
        }

    request.session.set_test_cookie()

    if request.method == 'POST':
        form = EditUserForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(user)
            messages.success(request, 'User changed successfully.')
            referrer = request.session.get('referrer')
            del request.session['referrer']

            return redirect(referrer)
    else:
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            if not request.session.get('referrer'):
                request.session['referrer'] = request.META.get('HTTP_REFERER')

        form = EditUserForm(user=request.user, initial=dct)

    context.update({'form': form})
    return render(request, 'accounts/edit_user.html', context)

@login_required
@must_be_group_admin
def upload_user_list(request):
    context = {}

    if request.method == 'POST':
      form = BulkUserUploadForm(request.POST, request.FILES, user=request.user)
      if form.is_valid():
          user_list = form.save()
          success = send_group_welcome_mail(user_list)
          messages.success(request, 'Users added successfully.')
          return redirect('accounts:upload_user_list')
    else:
        form = BulkUserUploadForm(user=request.user)

    context.update({
      'form': form, 
      'file_length': settings.MAX_FILE_LENGTH
    })
    return render(request, 'accounts/upload_user_list.html', context)

@login_required
@must_be_individual_user
def recharge_account(request):
    context = {}

    if request.method == 'POST':
        form = RechargeAccountForm(request.POST, user=request.user)
        if form.is_valid():
            voucher = form.save()
            url = settings.VOUCHER_INVALIDATE_URL
            response = send_api_request(url, {'id': voucher['serial_number']})

            if response['code'] == 200:
                messages.success(request, 
                    "%s%s" % ('Account recharged successfully. ', "<a class='btn btn-primary' href=" + reverse('packages:buy') + ">Purchase a package</a>"))
                return redirect('accounts:recharge_account')
    else:
        form = RechargeAccountForm(user=request.user)

    context.update({'form': form})
    return render(request, 'accounts/recharge_account.html', context)

@login_required
@must_be_group_admin
def view_users(request, page=None):
    context = {}
    user_list = User.objects.filter(subscriber__group=request.user.subscriber.group).exclude(pk=request.user.pk)

    paginate_by = request.GET.get('paginate_by', None)

    if paginate_by is None:
        paginate_by = 10

    paginator = Paginator(user_list, int(paginate_by))

    if page is None:
        page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context.update({'users': users})

    if paginate_by is not None:
        context.update({'paginate_by': paginate_by})

    return render(request, 'accounts/user_list.html', context)

@login_required
@must_be_group_admin
def toggle_status(request, pk):
    user = User.objects.get(pk=pk)
    
    if not request.session.get('referrer'):
        request.session['referrer'] = request.META.get('HTTP_REFERER')

    referrer = request.session.get('referrer')
    del request.session['referrer']

    if user.is_active:
        user.is_active = False
    else:
        group = request.user.subscriber.group
        if group.max_user_count_reached() or group.available_user_slots_count() is None:
            if not settings.EXCEED_MAX_USER_COUNT:
                messages.error(request,
                    "You are not allowed to create more users than your group threshold. Your group threshold is set to %s." % group.max_no_of_users)
                return redirect(referrer)
        else:
            user.is_active = True

    user.save()

    return redirect(referrer)
