from django.db import models

from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from common.blocks import Spotlight, TwoColGridImage
from blog.blocks import FeaturedContents, PromotedNewsList, PromotedSpotlightWithList
from shop.blocks import FeaturedProducts, ProductBlock
from common.blocks import WebsiteHeader, WebsiteFooter, EmptyBlock, Carousel
from wagtailstreamforms.blocks import WagtailFormBlock
from wagtail.embeds.blocks import EmbedBlock
from common.blocks import TwoColTextLeft, TwoColTextRight, IntroduceBlock, HRBlock
from wagtailmetadata.models import MetadataPageMixin

class Homepage(MetadataPageMixin, Page):
    max_count = 1
    header = StreamField([
        ('header', WebsiteHeader()),
        ('empty', EmptyBlock()),
    ], blank=True, null=True)
    body = StreamField([
        ('spotlight', Spotlight()),
        ('featured_products', FeaturedProducts()),
        ('featured_contents', FeaturedContents()),
        ('promoted_news_list', PromotedNewsList()),
        ('promoted_spotlight_with_list', PromotedSpotlightWithList()),
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
        ('product', ProductBlock()),
        ('line', HRBlock()),
    ],blank=True, null=True)
    footer = StreamField([
        ('footer', WebsiteFooter()),
        ('empty', EmptyBlock()),
    ], blank=True, null=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('body'),
        StreamFieldPanel('footer'),
    ]