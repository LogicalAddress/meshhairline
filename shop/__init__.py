from django.core.exceptions import ImproperlyConfigured

def get_model(model_string):
    from django.apps import apps
    try:
        return apps.get_model(model_string)
    except ValueError:
        raise ImproperlyConfigured("model_string must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "Model refers to model '%s' that has not been installed" % model_string
        )