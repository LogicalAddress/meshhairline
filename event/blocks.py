from wagtail.core.blocks import StructBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks
import datetime
from wagtailmodelchooser.blocks import ModelChooserBlock
from django.utils.translation import ugettext_lazy as _

class QuickLinkValue(blocks.StructValue):
   @property
   def url(self):
         if self.get('external_link'):
            return self['external_link']
         elif self['page']:
            return self['page'].url
         else:
            return None

class PromotedEventBlock(StructBlock):
   title = blocks.CharBlock(required=True, label="Title")
   description = blocks.CharBlock(required=True, label="Description")
   date = blocks.DateBlock()
   time = blocks.TimeBlock(required=True)
   display_type = blocks.ChoiceBlock(choices=[
      ('text', 'Text'),
      ('image', 'Image'),
      ('video', 'video'),
   ], icon = 'cup', default="text")
   picture = ImageChooserBlock( required=False)
   embed = EmbedBlock(required=False)
   video_min_height = blocks.CharBlock(required=False, default="300px")
   external_link = blocks.URLBlock(required=False, label="external_link")
   page = blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")
   link_text = blocks.CharBlock(required=True, label="Button Text", help_text="e.g Register Now")
   def get_context(self, value, parent_context=None):
      context = super().get_context(value, parent_context=parent_context)
      context['is_happening_today'] = (value['date'] == datetime.date.today())
      return context
   class Meta:
      icon = 'media'
      label = "Promoted Event"
      template = "event/blocks/PromotedEvent.html"
      value_class = QuickLinkValue


class SpeakerBlock(blocks.StructBlock):
   speaker = ModelChooserBlock('event.Speaker')
   is_featured_guest = blocks.BooleanBlock(default=False, required=False)
   class Meta:
      icon = 'media'
      label = "Speaker"
      template = "event/blocks/speaker.html"

class EventSessionBlock(blocks.StructBlock):
   title = blocks.CharBlock(required=True, label=_("Date label"))
   agenda =  blocks.ListBlock(blocks.StructBlock([
       ('agenda', ModelChooserBlock('event.Agenda'))
   ]))
   class Meta:
      icon = 'media'
      label = "Event Session"
      template = "event/blocks/session.html"


class TicketBlock(blocks.StructBlock):
   button_text = blocks.CharBlock(default="Buy Ticket")
   tickets =  blocks.ListBlock(blocks.StructBlock([
       ('page', blocks.PageChooserBlock(required=True, target_model='shop.Product'))
   ])) 
   class Meta:
      icon = 'media'
      label = "Ticket Block"
      template = "event/blocks/TicketBlock.html"