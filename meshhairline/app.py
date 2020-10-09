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
from users.models import User
from shop.models import Order, OrderItem, Product

class SnipcartHook(APIView):
    """
    * Requires token authentication.
    """
    # authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]

    def get(self, request, format=None):
        """
        Docs
        """
        print("SnipcartHook:GET: Incoming get")
        print(request.data)
        data = {
            "body": "ok"
        }
        return Response(data)
    def post(self, request, format=None):
        """
        Docs
        """
        print("SnipcartHook:POST: Incoming post")
        print(request.data['eventName'])
        try:
            if request.data['eventName'] == "order.completed":
                payment_gateway="snipcart"
                user = User.objects.get(email=request.data['content']['user']['email'])
                unique_items = len(request.data['content']['items'])
                # quantity = [sum(x.quantity) for x in request.data['content']['items']]
                print("user object")
                print(request.data['content']['user'])
                print(request.data['content']['user']['itemsCount'])
                quantity = request.data['content']['user']['itemsCount']
                total = request.data['content']['user']['itemsTotal']
                currency = request.data['content']['user']['currency']
                order = Order(title=request.data['content']['user']['paymentTransactionId'], 
                    email=user.email, 
                    username=user.username, unique_items=unique_items,
                    author=request.user,
                    quantity=quantity, total=total, payment_gateway=payment_gateway,
                    ref=request.data['content']['user']['paymentTransactionId'],
                    currency=currency)
                order.save()
                for item in request.data['content']['items']:
                    product = Product.objects.get(pk=item['id'])
                    oi = OrderItem(order=order, product=product, seller=product.seller,
                    title=product.title, email=user.email, username=user.username,
                    quantity=item['quantity'], total=item['totalPrice'], buyer=user,
                    currency=currency,
                    price=item['unitPrice'], payment_gateway=payment_gateway,ref=item['uniqueId'])
                    oi.save()
            data = {
                "body": "ok"
            } 
            return Response(data)
        except Exception as e:
                print(str(e) + ' Warning: snipcart webhook.')
                return Response({'status': str(e)})

class PaymentMethods(APIView):
    """
    * Requires token authentication.
    """
    # authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]

    def get(self, request, format=None):
        """
        Docs
        """
        print("Incoming get")
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
    def post(self, request, format=None):
        """
        Docs
        """
        print("Incoming post")
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