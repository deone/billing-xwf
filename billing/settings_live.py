from settings import *

DEBUG = TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['154.117.0.11']

STATIC_ROOT = os.path.join(BASE_DIR, "static_live")

STATIC_URL = "/static/"
