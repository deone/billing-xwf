from settings import *

DEBUG = False

IP = '154.117.8.21'

ALLOWED_HOSTS = [IP]
SUCCESS_URL = "http://" + IP + "/success/"
DEFAULT_FROM_EMAIL = 'info@spectrawireless.com'

# VMS
# VMS_URL = "http://" + IP + ":8090/vouchers/"
# VOUCHER_STUB_INSERT_URL = VMS_URL + "insert/"
# VOUCHER_STUB_DELETE_URL = VMS_URL + "delete/"
# VOUCHER_REDEEM_URL = VMS_URL + "redeem/"
# VOUCHER_INVALIDATE_URL = VMS_URL + "invalidate/"
# VOUCHER_SELL_URL = VMS_URL + "sell/"