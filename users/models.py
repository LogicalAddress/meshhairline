from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django_countries.fields import CountryField
from wagtail.snippets.models import register_snippet

class User(AbstractUser):
    country = CountryField(blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    default_currency = models.CharField(max_length=10, choices=settings.CURRENCY, blank=True, null=True)