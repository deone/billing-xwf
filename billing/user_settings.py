# Speed variants 
REGULAR = '0.512'
LITE = '1'
DELUX = '1.5'
PREMIERE = '2'
ULTRA = '3'
SUPREME = '4'

# Speed names
SPEED_NAME_MAP = {
    REGULAR: '512Kbps Regular',
    LITE: '1Mbps Lite',
    DELUX: '1.5Mbps Delux',
    PREMIERE: '2Mbps Premiere',
    ULTRA: '3Mbps Ultra',
    SUPREME: '4Mbps Supreme'
}

SPEED_CHOICES = (
    (REGULAR, SPEED_NAME_MAP[REGULAR]),
    (LITE, SPEED_NAME_MAP[LITE]),
    (DELUX, SPEED_NAME_MAP[DELUX]),
    (PREMIERE, SPEED_NAME_MAP[PREMIERE]),
    (ULTRA, SPEED_NAME_MAP[ULTRA]),
    (SUPREME, SPEED_NAME_MAP[SUPREME]),
)

# Volume variants
ONE = '1'
THREE = '3'
FIVE = '5'
EIGHT = '8'
TEN = '10'
TWELVE = '12'
FIFTEEN = '15'
TWENTY = '20'
TWENTY_FIVE = '25'
UNLTD = 'Unlimited'

# Volume names
VOLUME_NAME_MAP = {
    ONE: '1GB',
    THREE: '3GB',
    FIVE: '5GB',
    EIGHT: '8GB',
    TEN: '10GB',
    TWELVE: '12GB',
    FIFTEEN: '15GB',
    TWENTY: '20GB',
    TWENTY_FIVE: '25GB',
    UNLTD: 'Unlimited'
}

VOLUME_CHOICES = (
    (ONE, VOLUME_NAME_MAP[ONE]),
    (THREE, VOLUME_NAME_MAP[THREE]),
    (FIVE, VOLUME_NAME_MAP[FIVE]),
    (EIGHT, VOLUME_NAME_MAP[EIGHT]),
    (TEN, VOLUME_NAME_MAP[TEN]),
    (TWELVE, VOLUME_NAME_MAP[TWELVE]),
    (FIFTEEN, VOLUME_NAME_MAP[FIFTEEN]),
    (TWENTY, VOLUME_NAME_MAP[TWENTY]),
    (TWENTY_FIVE, VOLUME_NAME_MAP[TWENTY_FIVE]),
    (UNLTD, VOLUME_NAME_MAP[UNLTD]),
)

DAILY = 'Daily'
WEEKLY = 'Weekly'
MONTHLY = 'Monthly'

PACKAGE_TYPES = (
    (DAILY, 'Daily'),
    (WEEKLY, 'Weekly'),
    (MONTHLY, 'Monthly'),
)

PACKAGE_TYPES_HOURS_MAP = {
    DAILY: 1 * 24,
    WEEKLY: 7 * 24,
    MONTHLY: 30 * 24
}

MAX_FILE_LENGTH = 30

# Set this to False to test BulkUserUploadForm.clean()
# EXCEED_MAX_USER_COUNT = True
EXCEED_MAX_USER_COUNT = False
