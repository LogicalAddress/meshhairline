from .base import *

DEBUG = False
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
        'OPTIONS': {
            'ssl': {
                'ca': os.path.join(BASE_DIR, 'ca-certificate.crt'),
                'cert': None,
                'key': None,
            },
        }
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
DEFAULT_FROM_EMAIL= os.environ.get('DEFAULT_FROM_EMAIL', 'no-reply@pushdeploy.io'


import os
# Staging/Production AWS Everything
# https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_STATIC_LOCATION = 'static'
STATICFILES_STORAGE = 'common.storage_backends.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
DEFAULT_FILE_STORAGE = 'common.storage_backends.PublicMediaStorage'

AWS_PRIVATE_MEDIA_LOCATION = 'media/private'
PRIVATE_FILE_STORAGE = 'common.storage_backends.PrivateMediaStorage')