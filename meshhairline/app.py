from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import serializers
from rest_framework.fields import Field 
from rest_framework.renderers import JSONRenderer
from django.contrib.contenttypes.models import ContentType
from wagtail.api import APIField
from django.db.models import Q
from django.conf import settings
from django.http import Http404
from rest_framework import status
from datetime import datetime


class PaymentMethods(APIView):
    """
    * Requires token authentication.
    """
    # authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]

    def get(self, request, format=None):
        """
        Return currently logged in user's favourites.
        """
        return Response([])    
    def post(self, request, format=None):
        """
        Docs
        """
        print(request.data)
        data = {
            "headers": {
                "content-type": "application/json"
            },
            "body": [
                {
                    "id": "2checkoutcom",
                    "name": "2Checkout.com",
                    "checkoutUrl": "https://meshhairline.com/2checkout",
                },
                # {
                #     "id": "snipcart_custom_gatway_2",
                #     "name": "Custom gateway 2",
                #     "checkoutUrl": "https://snipcart.com/checkout_gateway_2",
                #     "iconUrl": "https://snipcart.com/checkout_gateway_2/icon.png"
                # }
            ]
        }
        return Response(data)