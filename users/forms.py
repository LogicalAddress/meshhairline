from django import forms
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from wagtail.users.forms import UserEditForm, UserCreationForm
from allauth.account.forms import SignupForm
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.forms import ModelForm
from .models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms_foundation.layout import Layout, Fieldset, SplitDateTimeField, Row, Column, ButtonHolder, Submit, Div

# class CustomUserEditForm(UserEditForm):
#     country = CountryField(blank=True).formfield()

class CustomUserCreationForm(SignupForm):
    city = forms.CharField(label=_("City"), max_length=255, required=True)
    country = CountryField(blank=False).formfield()
    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomUserCreationForm, self).save(request)
        user.country = request.POST.get('country')
        user.city = request.POST.get('city')
        user.save()
        # Add your own processing here.
        # You must return the original result.
        return user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-register'
        self.helper.form_class = 'register-form'
        self.helper.form_method = 'POST'
        self.helper.form_action = '/account/signup/'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['country'].initial = "NG"

        self.helper.layout = Layout(
            Div(
                Row(
                    Column('email', css_class='large-4'),
                ),
                Row(
                    Column('username', css_class='small-2 large-4'),
                ),
                Row(
                    Column('password1', css_class='small-2 large-4'),                
                ),
            ),
            Fieldset(
                'Location',
                Row(
                    Column('city', css_class='large-3'),
                    Column('country', css_class='large-3'),
                ),
            ),
        )


class CustomUserProfileForm(UserEditForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['username'].widget.attrs['readonly'] = True
            del self.fields['is_superuser']
            for fieldname in ['username']:
                self.fields[fieldname].help_text = None
    def clean_email(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.email
        else:
            return self.cleaned_data['email']
    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.username
        else:
            return self.cleaned_data['username']
    def clean_is_superuser(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.is_superuser
        else:
            return self.cleaned_data['is_superuser']
    @property
    def password_enabled(self):
        return False
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone', 'city', 'country', 'shipping_address', )
        exclude =('password1', 'password2')