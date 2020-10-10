from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.urls import path, include
from rest_framework import routers
from search import views as search_views
from .api import api_router
from common.views import switch_currency
from .app import PaymentMethods, SnipcartHook
from shop.views import twoCheckoutCo, customPaymentSession, customConfirmPayment, customConfirmPayment

urlpatterns = [
    url(r'^account/', include('allauth.urls')), # Creates urls like yourwebsite.com/login/
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),
    # path('api/', include(router.urls))
    path("paystack", include(('paystack.urls','paystack'),namespace='paystack')),
    url(r'^user/', include('users.urls')),
    # Terms and Conditions
    url(r'^terms/', include('termsandconditions.urls')),
    url(r'^switch_currency/$', switch_currency, name='switch_currency'),
    url(r'^payment-methods/$', PaymentMethods.as_view()),
    url(r'^snipcart_hook/$', SnipcartHook.as_view()),
    url(r'^2checkout/$', twoCheckoutCo),
    url(r'^custom-payment-session/$', customPaymentSession),
    url(r'^custom-confirm-payment/$', customConfirmPayment),
    url(r'^custom-refund/$', customRefundPayment),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    url(r'^api/v2/', api_router.urls),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r"", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r"^pages/", include(wagtail_urls)),
]
