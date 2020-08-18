from django.db import models
from wagtail.core.models import Page, Orderable
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from common.blocks import Spotlight, TwoColGridImage, TwoColTextLeft, TwoColTextRight, IntroduceBlock
from blog.blocks import PromotedNewsList, PromotedSpotlightWithList
from shop.blocks import FeaturedProducts
from common.blocks import WebsiteHeader, WebsiteFooter, EmptyBlock, Carousel
from wagtailstreamforms.blocks import WagtailFormBlock
from wagtail.embeds.blocks import EmbedBlock
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.forms import WagtailAdminPageForm
# from django import forms
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import InlinePanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from .blocks import SpeakerBlock, EventSessionBlock
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalManyToManyField
from wagtailmodelchooser.blocks import ModelChooserBlock
from wagtail.admin.edit_handlers import PageChooserPanel
from django.conf import settings
from .blocks import TicketBlock
from users.models import User
from wagtailmetadata.models import MetadataPageMixin

class EventPageForm(WagtailAdminPageForm):
    # address = forms.CharField()
    def clean(self):
        cleaned_data = super(EventPageForm, self).clean()
        # Make sure that the event starts before it ends
        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']
        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', 'The end date must be after the start date')
        return cleaned_data
    def save(self, commit=True):
        page = super(EventPageForm, self).save(commit=False)
        page.duration = (page.end_date - page.start_date).days
        if commit:
            page.save()
        return page

@register_snippet
class Speaker(models.Model):
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    page = models.ForeignKey('wagtailcore.Page', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+')
    external_link = models.URLField(blank=True, null=True)
    photo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    twitter = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('job_title'),
        FieldPanel('description'),
        ImageChooserPanel('photo'),
        MultiFieldPanel([
            PageChooserPanel('page'),
            FieldPanel('external_link'),
        ], heading="Link"),
        MultiFieldPanel([
            FieldPanel('twitter'),
            FieldPanel('linkedin'),
            FieldPanel('facebook'),
            FieldPanel('instagram'),
        ], heading="Social"),
    ]

    @property
    def link(self):
        if self.page:
            return self.page.url
        elif self.external_link:
            return self.external_link
        else:
            return None

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Speakers'
        verbose_name = 'Speaker'

@register_snippet
class Sponsor(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    page = models.ForeignKey('wagtailcore.Page', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+')
    external_link = models.URLField(blank=True, null=True)
    photo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    twitter = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        ImageChooserPanel('photo'),
        MultiFieldPanel([
            PageChooserPanel('page'),
            FieldPanel('external_link'),
        ], heading="Link"),
        MultiFieldPanel([
            FieldPanel('twitter'),
            FieldPanel('linkedin'),
            FieldPanel('facebook'),
            FieldPanel('instagram'),
        ], heading="Social"),
    ]

    @property
    def link(self):
        if self.page:
            return self.page.url
        elif self.external_link:
            return self.external_link
        else:
            return null

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Sponsors'
        verbose_name = 'Sponsor'

class EventPage(MetadataPageMixin, Page):
    short_description = models.TextField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.IntegerField()
    location = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    event_type = models.CharField(max_length=50, 
        choices=settings.EVENT_TYPES, default="concert")
    cover_photo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    event_photo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    layout = models.CharField(max_length=20, default="default", choices=settings.EVENT_LAYOUTS)
    header = StreamField([
        ('header', WebsiteHeader()),
        ('empty', EmptyBlock()),
    ], blank=True, null=True)
    body = StreamField([
        ('spotlight', Spotlight()),
        ('featured_products', FeaturedProducts()),
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('form', WagtailFormBlock()),
        ('embed', EmbedBlock()),
        ('HTML', blocks.RawHTMLBlock()),
        ('Carousel', Carousel()),
        ('TwoColGridImage', TwoColGridImage()),
        ('TwoColTextLeft', TwoColTextLeft()),
        ('TwoColTextRight', TwoColTextRight()),
        ('Introduce', IntroduceBlock()),
        ('ticket', TicketBlock()),
    ],blank=True, null=True)
    footer = StreamField([
        ('footer', WebsiteFooter()),
        ('empty', EmptyBlock()),
    ], blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('start_date'),
            FieldPanel('end_date'),
            FieldPanel('location'),
            FieldPanel('address'),
            FieldPanel('short_description'),
            FieldPanel('description', classname="full"),
        ], heading="Event Meta"),
        MultiFieldPanel([
            InlinePanel('featured_guests', label="Featured Guest"),
            InlinePanel('event_agendas', label="Agenda"),
            InlinePanel('event_sponsors', label="Sponsor"),
            InlinePanel('event_tickets', label="Ticket"),
        ], heading="Event Design"),
        MultiFieldPanel([
            FieldPanel('cover_photo'),
            FieldPanel('event_photo'),
            FieldPanel('layout'),
            StreamFieldPanel('header'),
            StreamFieldPanel('body'),
            StreamFieldPanel('footer'),
        ], heading="Layout Design"),
    ]
    base_form_class = EventPageForm


@register_snippet
class Agenda(ClusterableModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    session_type = models.CharField(max_length=255) #e.g MAIN STAGE, BREAKOUT SESSION RM3
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('session_type'),
        MultiFieldPanel([
            FieldPanel('time_from'),
            FieldPanel('time_to'),
            FieldPanel('date'),
        ], heading="Time"),
        InlinePanel('agenda_speakers_relationship'),
    ]

    @property
    def speakers(self):
        speakers = [
            n.speaker for n in self.agenda_speakers_relationship.all()
        ]
        return speakers

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Agenda'
        verbose_name = 'Agenda'

class AgendaSpeakerRelationship(models.Model):
    agenda = ParentalKey('event.Agenda', on_delete=models.CASCADE, related_name='agenda_speakers_relationship')
    speaker = models.ForeignKey(
        'event.Speaker', on_delete=models.CASCADE, related_name='+'
    )
    panels = [
        SnippetChooserPanel('speaker'),
    ]
    class Meta:
        unique_together = ('agenda', 'speaker')


class FeaturedGuest(Orderable):
    page = ParentalKey('event.EventPage', related_name="featured_guests")
    speaker = models.ForeignKey('event.Speaker', on_delete=models.CASCADE, related_name="+")
    panels = [
        SnippetChooserPanel('speaker')
    ]
    class Meta:
        unique_together = ('page', 'speaker')

class EventAgenda(Orderable):
    page = ParentalKey('event.EventPage', related_name="event_agendas")
    agenda = models.ForeignKey('event.Agenda', on_delete=models.CASCADE, related_name="+")
    panels = [
        SnippetChooserPanel('agenda')
    ]
    class Meta:
        unique_together = ('page', 'agenda')


class EventSponsor(Orderable):
    page = ParentalKey('event.EventPage', related_name="event_sponsors")
    sponsor = models.ForeignKey('event.Sponsor', on_delete=models.CASCADE, related_name="+")
    panels = [
        SnippetChooserPanel('sponsor')
    ]
    class Meta:
        unique_together = ('page', 'sponsor')


class EventTicket(Orderable):
    page = ParentalKey('event.EventPage', related_name="event_tickets")
    ticket = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name="+")
    panels = [
        PageChooserPanel('ticket')
    ]
    class Meta:
        unique_together = ('page', 'ticket')

class Ticket(models.Model):
    event = models.ForeignKey('event.EventPage', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+')
    product = models.ForeignKey('shop.Product', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+')
    product_title = models.CharField(max_length=255, blank=True, null=True)
    event_title = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    ticket_class = models.CharField(max_length=50, blank=True, null=True)
    payment_type = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    amount = models.FloatField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product_title

    class Meta:
        verbose_name_plural = 'Tickets'
        verbose_name = 'Ticket'