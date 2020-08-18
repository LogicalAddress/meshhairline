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
from .models import Ticket
# from import_export import resources


class InstanceSpecificViewHookMixin:
    """Mixin class responsible to apply wagtailstreamforms specific hooks."""

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class InspectFormView(InstanceSpecificViewHookMixin, InspectView):
    pass

class CreateTicketView(CreateView):
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        wagtail_messages.success(
            self.request,
            self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance),
        )
        return redirect(self.get_success_url())

class EditTicketView(InstanceSpecificViewHookMixin, EditView):
    pass

class DeleteTicketView(InstanceSpecificViewHookMixin, DeleteView):
    pass

@modeladmin_register
class TicketModelAdmin(ModelAdmin):
    model = Ticket
    list_display = ("event_title", "product_title", "user_name", "ticket_class", "email", "quantity", "amount", "payment_type", "created_at")    
    list_filter = None
    menu_label = "Tickets"
    menu_order = -600
    menu_icon = "icon icon-form"
    search_fields = ("event_title", "product_title", "user_name", "email", "ticket_class", "payment_type" )
    inspect_view_class = InspectFormView
    create_view_class = CreateTicketView
    edit_view_class = EditTicketView
    delete_view_class = DeleteTicketView

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