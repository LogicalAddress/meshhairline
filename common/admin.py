from django.contrib import admin

# Register your models here.
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from wagtail.admin import messages as wagtail_messages
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import (
    CreateView,
    DeleteView,
    EditView,
    InspectView,
)
from wagtail.core import hooks
from termsandconditions.models import TermsAndConditions

class InstanceSpecificViewHookMixin:
    """Mixin class responsible to apply wagtailstreamforms specific hooks."""

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class InspectFormView(InstanceSpecificViewHookMixin, InspectView):
    pass

class CreateTCView(CreateView):
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        wagtail_messages.success(
            self.request,
            self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance),
        )
        return redirect(self.get_success_url())

class EditTCView(InstanceSpecificViewHookMixin, EditView):
    pass

class DeleteTCView(InstanceSpecificViewHookMixin, DeleteView):
    pass

@modeladmin_register
class TCModelAdmin(ModelAdmin):
    model = TermsAndConditions
    list_display = ("name", "slug", )    
    list_filter = None
    menu_label = "T & C"
    menu_order = -600
    menu_icon = "icon icon-form"
    search_fields = None
    inspect_view_class = InspectFormView
    create_view_class = CreateTCView
    edit_view_class = EditTCView
    delete_view_class = DeleteTCView

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # for fn in artist_hook.get_hooks("construct_form_queryset"):
        #     qs = fn(qs, request)
        return qs

    def get_list_display(self, request):
        list_display = self.list_display
        # for fn in artist_hook.get_hooks("construct_form_list_display"):
        #     list_display = fn(list_display, request)
        return list_display

    def get_list_filter(self, request):
        list_filter = self.list_filter
        # for fn in artist_hook.get_hooks("construct_form_list_filter"):
        #     list_filter = fn(list_filter, request)
        return list_filter