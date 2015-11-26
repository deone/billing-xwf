from settings import *

DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['154.117.8.18']

STATIC_URL = "/static/"

SUCCESS_URL = "http://154.117.8.18:8080/success/"

DEFAULT_FROM_EMAIL = 'info@spectrawireless.com'

# VMS
VMS_URL = "http://154.117.8.18:8090/vouchers/"
VOUCHER_STUB_INSERT_URL = VMS_URL + "insert/"
VOUCHER_STUB_DELETE_URL = VMS_URL + "delete/"
VOUCHER_REDEEM_URL = VMS_URL + "redeem/"
VOUCHER_INVALIDATE_URL = VMS_URL + "invalidate/"
