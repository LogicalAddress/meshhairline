from django.dispatch import receiver
from shop.models import OrderItem
from django.db.models.signals import post_save
from django.core.signals import request_finished
from .models import EventPage, Ticket, EventTicket

@receiver(post_save, sender=OrderItem, dispatch_uid="meshhairline.event.signals.saveTickets")
def saveTickets(sender, instance, created, **kwargs):
    if created and instance.product.product_type == 'ticket':
        try:
            eventTicket = EventTicket.objects.get(ticket=instance.product)
            event = eventTicket.page
            ticket = Ticket(event=event, email=instance.email, 
                user_name=instance.username, quantity=instance.quantity, 
                amount=instance.total, payment_type=instance.payment_gateway,
                product=instance.product, product_title=instance.product.title,
                ticket_class=instance.product.ticket_class,
                event_title=event.title, seller=instance.product.seller)
            ticket.save()
        except Exception as e:
            print(str(e) + ' Warning: unable to associate the ticket to an event.')
            ticket = Ticket(email=instance.email, 
                user_name=instance.username, quantity=instance.quantity, 
                amount=instance.total, payment_type=instance.payment_gateway,
                product=instance.product, product_title=instance.product.title,
                ticket_class=instance.product.ticket_class,
                event_title='N/A', seller=instance.product.seller)
            ticket.save()