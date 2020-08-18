import random
import string
from django.utils.text import slugify

def unique_slug_generator(instance, new_slug=None, increment = 1):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = slugify(new_slug)
    else:
        slug = slugify(instance.title)
    Klass = instance
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=increment
                )
        return unique_slug_generator(instance, new_slug=new_slug, increment = increment + 1)
    return slug