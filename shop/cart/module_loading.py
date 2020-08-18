from django.conf import settings

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module


def get_product_model():
    """
    Returns the product model that is used by this cart.
    """
    package, module = 'shop.models.Product'.rsplit('.', 1)
    return getattr(import_module(package), module)