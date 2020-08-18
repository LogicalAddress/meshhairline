from wagtail.core.blocks import StructBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks
from common.blocks import QuickLinkValue


class ProductBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock(
       required=True,
       target_model='shop.Product'
    )
    display_type = blocks.ChoiceBlock(choices=[
        ('lean', 'Lean'),
        ('details', 'Details') 
    ], default='lean')
    action_text = blocks.CharBlock(default="Buy")
    class Meta:
       icon = 'media'
       label = "Product basic details & cart"
       template = "shop/blocks/Product.html"

class FeaturedProducts(StructBlock):
    products = blocks.ListBlock(blocks.StructBlock([
       ('picture', ImageChooserBlock( required=True) ),
       ('title', blocks.CharBlock(required=True, label="Title")),
       ('discount', blocks.RawHTMLBlock(required=False, label="Discount text") ),
       ('external_link', blocks.URLBlock(required=False, label="External Link", help_text="URL to external page")),
       ('page', blocks.PageChooserBlock(label="page", required=False, help_text="Link a Page")),
       ('amount', blocks.RawHTMLBlock( required=True) ),
    ], value_class = QuickLinkValue))
    section_text = blocks.RawHTMLBlock(required=False, label="Section text")
    class Meta:
       icon = 'media'
       label = "Featured Product"
       template = "shop/blocks/FeaturedProducts.html"