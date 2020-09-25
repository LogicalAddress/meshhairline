from django import template

from shop.cart.cart import Cart
from shop.cart.settings import CART_TEMPLATE_TAG_NAME


register = template.Library()


@register.simple_tag(takes_context=True, name=CART_TEMPLATE_TAG_NAME)
def get_cart(context):
    request = context['request']
    context['cart'] = Cart(request.session)
    return ''

@register.simple_tag(takes_context=True, name='currency_price')
def get_currency_price(context, price, currency):
    if currency and currency == "USD":
        rate = 360
        price = float(price) / rate
        return "%.2f" % round(price, 2)
    else:
        return float(price)

@register.simple_tag(takes_context=True, name='currency_symbol')
def get_currency_symbol(context, currency):
    if currency and currency == 'USD':
        return '$'
    else:
        return 'N'