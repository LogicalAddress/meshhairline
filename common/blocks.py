from wagtail.core.blocks import StructBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtailstreamforms.blocks import WagtailFormBlock
from wagtail.core.models import Page
# from blog.models import BlogPage
from event.blocks import PromotedEventBlock

class QuickLinkValue(blocks.StructValue):
    @property
    def url(self):
        if self.get('external_link'):
            return self['external_link']
        elif self.get('page') and self['page']:
            return self['page'].url
        else:
            return None

class WebsiteHeader(blocks.StructBlock):
    button_text = blocks.CharBlock(required=False, label="Button Text")
    page = blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")
    external_link = blocks.URLBlock(required=False, label="URL", help_text="External Link")
    show_main_menu = blocks.BooleanBlock(default=True, required=False)
    class Meta:
       icon = 'media'
       label = "Customizable Header"
       template = "common/blocks/Header.html"
       value_class = QuickLinkValue

class WebsiteFooter(blocks.StructBlock):
    body = blocks.StreamBlock([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('form', WagtailFormBlock()),
        ('embed', EmbedBlock(required=False)),
        ('HTML', blocks.RawHTMLBlock())
    ], blank=True, null=True)
    class Meta:
       icon = 'media'
       label = "Customizable Footer"
       template = "common/blocks/Footer.html"

class EmptyBlock(blocks.StaticBlock):
   class Meta:
       icon = 'media'
       label = "Empty Block"
       template = "common/blocks/Empty.html"

class HRBlock(blocks.StaticBlock):
   class Meta:
       icon = 'media'
       label = "Horizontal Line"
       template = "common/blocks/HR.html"

class Carousel(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label="Title")
    items = blocks.ListBlock(blocks.StructBlock([
        ('image', ImageChooserBlock( required=False)),
        ('overlay_text', blocks.CharBlock(required=True, label="Overlay Text")),
        ('description', blocks.CharBlock(required=False)),
        ('page', blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")),
        ('external_link', blocks.URLBlock(required=False, label="URL", help_text="External Link")),
        ('is_active', blocks.BooleanBlock(required=False, default=False)),
        ('display_type', blocks.ChoiceBlock(choices=[
            ('text', 'Text'),
            ('image', 'Image'),
            ('video', 'Video'),
            ('event', 'Event'),
            ('product', 'Product'),
        ], icon = 'cup', default="image")),
        ('embed', EmbedBlock(required=False)),
    ], value_class = QuickLinkValue))
    section_text = blocks.RawHTMLBlock(required=False, label="Section text")
    video_min_height = blocks.CharBlock(required=False, default="300px")
    class Meta:
       icon = 'media'
       label = "Carousel"
       template = "common/blocks/Carousel.html"

class Spotlight(StructBlock):
    photo = ImageChooserBlock(required=False)
    embed = EmbedBlock(required=False)
    video = blocks.URLBlock(required=False, label="video stream", help_text="RTSP Endpoint")
    video_min_height = blocks.CharBlock(required=False, default="300px")
    biography = blocks.RichTextBlock(required=True)
    heading = blocks.CharBlock(required=False, label="Heading")
    title = blocks.CharBlock(required=True, label="Title")
    external_link = blocks.URLBlock(required=False, label="External Link", help_text="URL to external page")
    page = blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")
    class Meta:
       icon = 'media'
       label = "Spotlight"
       template = "common/blocks/Spotlight.html"
       value_class = QuickLinkValue


class TwoColGridImage(StructBlock):
    title = blocks.CharBlock(required=False, label="Title")
    video_min_height = blocks.CharBlock(required=False, default="300px")
    items = blocks.ListBlock(blocks.StructBlock([
       ('picture', ImageChooserBlock( required=False) ),
       ('embed', EmbedBlock(required=False)),
       ('title', blocks.CharBlock(required=False, label="Title")),
       ('vertical_text', blocks.RawHTMLBlock(required=False, label="vertical_text") ),
       ('external_link', blocks.URLBlock(required=False, label="External Link", help_text="URL to external page")),
       ('page', blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")),
    ], value_class = QuickLinkValue))
    section_text = blocks.RawHTMLBlock(required=False, label="Section text")
    class Meta:
       icon = 'media'
       label = "TwoColGridImage"
       template = "common/blocks/TwoColGridImage.html"


class TwoColTextLeft(StructBlock):
    photo = ImageChooserBlock(required=False)
    embed = EmbedBlock(required=False)
    video_min_height = blocks.CharBlock(required=False, default="300px")
    text = blocks.RichTextBlock(required=True)
    heading = blocks.CharBlock(required=False, label="Heading")
    external_link = blocks.URLBlock(required=False, label="External Link", help_text="URL to external page")
    page = blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")
    class Meta:
       icon = 'media'
       label = "Two Cols Text Left"
       template = "common/blocks/TwoColTextLeft.html"
       value_class = QuickLinkValue

class TwoColTextRight(StructBlock):
    photo = ImageChooserBlock(required=False)
    embed = EmbedBlock(required=False)
    video_min_height = blocks.CharBlock(required=False, default="300px")
    text = blocks.RichTextBlock(required=True)
    heading = blocks.CharBlock(required=False, label="Heading")
    external_link = blocks.URLBlock(required=False, label="External Link", help_text="URL to external page")
    page = blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")
    vimeo = blocks.URLBlock(required=False, label="Vimeo URL", help_text="Vimeo")
    class Meta:
       icon = 'media'
       label = "Two Cols Text Right"
       template = "common/blocks/TwoColTextRight.html"
       value_class = QuickLinkValue

class IntroduceBlock(StructBlock):
    title = blocks.CharBlock(required=False, label="Title")
    align_title = blocks.ChoiceBlock(choices=[
            ('left', 'Left'),
            ('right', 'Right'),
            ('center', 'Center'),
        ], icon = 'media', default="left")
    intro = blocks.RawHTMLBlock(required=False, label="Intro text")
    align_intro = blocks.ChoiceBlock(choices=[
            ('left', 'Left'),
            ('right', 'Right'),
            ('center', 'Center'),
            ('justify', 'Justfy'),
        ], icon = 'media', default="left")
    class Meta:
       icon = 'media'
       label = "Intro Block"
       template = "common/blocks/IntroBlock.html"