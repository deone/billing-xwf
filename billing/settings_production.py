from settings import *

DEBUG = False

URL = 'xwf.spectrawireless.com'
ALLOWED_HOSTS = [URL]
SUCCESS_URL = "http://" + URL + "/success/"

DEFAULT_FROM_EMAIL = 'info@spectrawireless.com'

# VMS
IP = '154.117.8.18'
VMS_URL = "http://" + IP + ":8090/vouchers/"
VOUCHER_STUB_INSERT_URL = VMS_URL + "insert/"
VOUCHER_STUB_DELETE_URL = VMS_URL + "delete/"
VOUCHER_REDEEM_URL = VMS_URL + "redeem/"
VOUCHER_INVALIDATE_URL = VMS_URL + "invalidate/"
VOUCHER_SELL_URL = VMS_URL + "sell/"

# Speed variants 
SUPREME = '4'

# Speed names
SPEED_NAME_MAP = {
    SUPREME: '4Mbps Supreme'
}

SPEED_CHOICES = (
    (SUPREME, SPEED_NAME_MAP[SUPREME]),
)

# Volume variants
HUNDRED_MB = '0.1'
THREE_HUNDRED_MB = '0.3'
ONE = '1'
TWO = '2'
TWO_POINT_FIVE = '2.5'
SIX = '6'

# Volume names
VOLUME_NAME_MAP = {
    HUNDRED_MB: '0.1GB',
    THREE_HUNDRED_MB: '0.3GB',
    ONE: '1GB',
    TWO: '2GB',
    TWO_POINT_FIVE: '2.5GB',
    SIX: '6GB'
}

VOLUME_CHOICES = (
    (HUNDRED_MB, VOLUME_NAME_MAP[HUNDRED_MB]),
    (THREE_HUNDRED_MB, VOLUME_NAME_MAP[THREE_HUNDRED_MB]),
    (ONE, VOLUME_NAME_MAP[ONE]),
    (TWO, VOLUME_NAME_MAP[TWO]),
    (TWO_POINT_FIVE, VOLUME_NAME_MAP[TWO_POINT_FIVE]),
    (SIX, VOLUME_NAME_MAP[SIX]),
)