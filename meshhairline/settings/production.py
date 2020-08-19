from .base import *

DEBUG = True
SECRET_KEY = 'kxd=9&mpjnfw6+-s9bt618nxb%)33p#y4cmr@dw7*%yu5@%^-b'

ALLOWED_HOSTS = ['*'] 

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_BACKEND', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DATABASE_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('DATABASE_USER', 'root'),
        'PASSWORD': os.environ.get('DATABASE_PASS', 'yahweh'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '3306'),
        # 'OPTIONS': {
        #     'ssl': {
        #         'ca': os.path.join(BASE_DIR, 'ca-certificate.crt'),
        #         'cert': None,
        #         'key': None,
        #     },
        # }
    }
}

try:
    from .local import *
except ImportError:
    pass

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.sendgrid.net')
EMAIL_USE_TLS = False
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'apikey')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL= os.environ.get('DEFAULT_FROM_EMAIL', 'no-reply@pushdeploy.io')