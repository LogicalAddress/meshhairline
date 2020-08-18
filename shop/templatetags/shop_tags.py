from django import template

from shop.cart.cart import Cart
from shop.cart.settings import CART_TEMPLATE_TAG_NAME


register = template.Library()


@register.simple_tag(takes_context=True, name=CART_TEMPLATE_TAG_NAME)
def get_cart(context):
    request = context['request']
    context['cart'] = Cart(request.session)
    return ''
