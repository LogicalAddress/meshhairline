from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kxd=9&mpjnfw6+-s9bt618nxb%)33p#y5cmr@dw7*%yu5@%^-b'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INTERNAL_IPS = (
    '127.0.0.1',
)

try:
    from .local import *
except ImportError:
    pass