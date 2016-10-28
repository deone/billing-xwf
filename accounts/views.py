from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from billing.decorators import *

from utils import get_subscriptions

from .forms import CreateUserForm, LoginForm, BulkUserUploadForm, EditUserForm, RechargeAccountForm
from .models import Subscriber
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
    context = {'form': LoginForm()}
    request.session['logout_url'] = None
    
    # Store request.GET parameters in session
    if not 'login_url' in request.session:
        request.session['login_url'] = request.GET['login_url']
        request.session['continue_url'] = request.GET['continue_url']
        request.session['ap_mac'] = request.GET['ap_mac']
        request.session['ap_name'] = request.GET['ap_name']
        request.session['ap_tags'] = request.GET['ap_tags']
        request.session['client_mac'] = request.GET['client_mac']
        request.session['client_ip'] = request.GET['client_ip']

    if 'error_message' in request.GET:
        context.update({
            'error_message': request.GET['error_message']
        })

    if 'login_url' in request.GET:
        context.update({
          'login_url': request.GET['login_url'],
          'logout_url': request.session['logout_url'],
          'success_url': settings.SUCCESS_URL,
        })
    else:
        raise Http404("Login URL is incorrect. Please disconnect and reconnect to the WiFi network to get an accurate URL.")

    return render(request, 'captive.html', context)

def success(request):
    if 'logout_url' in request.GET:
        request.session['logout_url'] = request.GET['logout_url']
        context = {'logout_url': request.session.get('logout_url', None)}
    else:
        context = {}

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

    logout_url = request.session.get('logout_url', None)
    context.update({'logout_url': logout_url})

    return render(request, 'accounts/index.html', context)

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
                messages.success(request, "Account recharged successfully.")
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
