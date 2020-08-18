from wagtail.core.blocks import StructBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks
from event.blocks import PromotedEventBlock
from common.blocks import QuickLinkValue
from blog import get_model

class FeaturedContents(StructBlock):
   spotlight = blocks.StructBlock([
        ('picture', ImageChooserBlock( required=False) ),
        ('video', blocks.URLBlock(required=False, label="Stream URL", help_text="RSTP Video Feed")),
        ('video_min_height', blocks.CharBlock(required=False, default="300px")),
        ('embed', EmbedBlock(required=False)),
        ('title', blocks.CharBlock(required=True, label="Title")),
        ('external_link',blocks.URLBlock(required=False, label="external_link")),
        ('page', blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")),
        ('creators', blocks.ListBlock(blocks.StructBlock([
            ('name', blocks.CharBlock()),
            ('external_link',blocks.URLBlock(required=False, label="external_link")),
            ('page', blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")),
        ], value_class = QuickLinkValue))),
       ('date', blocks.DateBlock(required=False)),
   ], value_class = QuickLinkValue)

   promotedList = blocks.ListBlock(blocks.StructBlock([
       ('title', blocks.CharBlock(required=True, label="Title")),
       ('external_link', blocks.URLBlock(required=False, label="external_link")),
       ('page', blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")),
       ('author', blocks.StructBlock([
            ('name', blocks.CharBlock()),
            ('external_link',blocks.URLBlock(required=False, label="external_link")),
            ('page', blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")),
        ], value_class = QuickLinkValue)),
       ('date', blocks.DateBlock(required=False)),
       ('picture', ImageChooserBlock( required=False) ),
   ], value_class = QuickLinkValue))

   section_text = blocks.RawHTMLBlock(required=False, label="Section text")
   padding_type = blocks.ChoiceBlock(choices=[
         ('uk-padding-large', 'Large'),
         ('uk-padding-small', 'Small'),
      ], icon = 'media', default="uk-padding-small")
   promoted_events = blocks.ListBlock(blocks.StructBlock([
       ('event', PromotedEventBlock(required=False)),
    ]))
   def get_context(self, value, parent_context=None):
       context = super().get_context(value, parent_context=parent_context)
       blogpages = get_model('blog.BlogPage').objects.filter(is_featured=True).order_by('-first_published_at')
       context['blogpages'] = blogpages
       return context
   class Meta:
       icon = 'media'
       label = "Featured Contents"
       template = "blog/blocks/FeaturedContents.html"


class PromotedNewsList(StructBlock):
    promotedList = blocks.ListBlock(blocks.StructBlock([
       ('title', blocks.CharBlock(required=True, label="Title")),
       ('external_link',blocks.URLBlock(required=False, label="external_link")),
       ('description',blocks.CharBlock(required=True, label="Description")),
       ('page', blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")),
       ('author', blocks.StructBlock([
            ('name', blocks.CharBlock()),
            ('external_link',blocks.URLBlock(required=False, label="external_link")),
            ('page', blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")),
        ], value_class=QuickLinkValue)),
       ('date', blocks.DateBlock(required=False)),
       ('picture', ImageChooserBlock( required=False) ),
    ], value_class = QuickLinkValue))
    section_text = blocks.RawHTMLBlock(required=False, label="Section text")
    layout = blocks.ChoiceBlock(choices=[
            ('uk-width-2-3@m', '80% Width in Container'),
            ('nop', 'Fullwidth'), #dummy class
      ], icon = 'media', default="uk-width-2-3@m")
    align = blocks.ChoiceBlock(choices=[
            ('uk-align-center', 'Middle'),
            ('uk-align-left', 'Left'), #dummy class
      ], icon = 'media', default="uk-align-left")
    class Meta:
       icon = 'media'
       label = "Promoted News List"
       template = "blog/blocks/PromotedNewsList.html"

class PromotedSpotlightWithList(StructBlock):
   spotlight = blocks.StructBlock([
        ('picture', ImageChooserBlock( required=False) ),
        ('video', blocks.URLBlock(required=False, label="Stream URL", help_text="RSTP Video Feed")),
        ('video_min_height', blocks.CharBlock(required=False, default="300px")),
        ('embed', EmbedBlock(required=False)),
        ('title', blocks.CharBlock(required=True, label="Title")),
        ('external_link',blocks.URLBlock(required=False, label="external_link")),
        ('page', blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")),
        ('creators', blocks.ListBlock(blocks.StructBlock([
            ('name', blocks.CharBlock()),
            ('external_link',blocks.URLBlock(required=False, label="external_link")),
            ('page', blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")),
        ], value_class = QuickLinkValue))),
       ('date', blocks.DateBlock(required=False)),
      ], value_class = QuickLinkValue)

   promotedList = blocks.ListBlock(blocks.StructBlock([
       ('title', blocks.CharBlock(required=True, label="Title")),
       ('external_link', blocks.URLBlock(required=False, label="external_link")),
       ('page', blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")),
       ('author', blocks.StructBlock([
            ('name', blocks.CharBlock()),
            ('external_link',blocks.URLBlock(required=False, label="external_link")),
            ('page', blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")),
        ], value_class = QuickLinkValue)),
       ('date', blocks.DateBlock(required=False)),
       ('picture', ImageChooserBlock( required=False) ),
   ], value_class = QuickLinkValue))
   padding_type = blocks.ChoiceBlock(choices=[
         ('uk-padding-large', 'Large'),
         ('uk-padding-small', 'Small'),
      ], icon = 'media', default="uk-padding-small")
   class Meta:
      icon = 'media'
      label = "Promoted Spotlight with List"
      template = "blog/blocks/PromotedSpotlightWithList.html"