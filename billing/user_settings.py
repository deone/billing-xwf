SPEED_CHOICES = (
    ('1', '1Mbps'),
    ('1.5', '1.5Mbps'),
    ('2', '2Mbps'),
)

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
