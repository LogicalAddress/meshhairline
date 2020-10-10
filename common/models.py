from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.conf import settings

@register_setting
class WebsiteSettings(BaseSetting):

    site_name = models.CharField(
        max_length=255,
        help_text='Logo Link',
        blank=True,
        null=True,
        default="Meshhairline"
    ) 

    contact_email = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default='only1meshhairline@gmail.com'
    )

    snipcart_api_key = models.CharField(
        max_length=255,
        help_text='Your Snipcart public API key'
    )

    snipcart_private_key = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Your Snipcart private API key'
    )

    logo_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    twitter_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="https://twitter.com/meshhairline"
    )

    facebook_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="https://web.facebook.com/MeshHairline"
    )

    instagram_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="https://www.instagram.com/meshhairline"
    )

    youtube_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="https://www.youtube.com/channel/UCVdcKDTyzJBhld9MfrZ4_1w"
    )

    linkedin_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    ticktok_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )