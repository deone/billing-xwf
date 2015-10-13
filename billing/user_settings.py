FIRST = '1'
SECOND = '1.5'
THIRD = '2'

SPEED_CHOICES = (
    (FIRST, '1Mbps Lite'),
    (SECOND, '1.5Mbps Delux'),
    (THIRD, '2Mbps Supreme'),
)

SPEED_NAME_MAP = {
    FIRST: 'Lite',
    SECOND: 'Delux',
    THIRD: 'Supreme'
}

VOLUME_CHOICES = (
    ('1', '1GB'),
    ('3', '3GB'),
    ('5', '5GB'),
    ('8', '8GB'),
    ('10', '10GB'),
    ('12', '12GB'),
    ('15', '15GB'),
    ('20', '20GB'),
    ('25', '25GB'),
    ('Unlimited', 'Unlimited'),
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
