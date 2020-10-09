from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.admin.edit_handlers import StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField
from common.blocks import WebsiteHeader, WebsiteFooter, EmptyBlock, Spotlight
from common.blocks import TwoColGridImage, TwoColTextLeft, TwoColTextRight
from common.blocks import IntroduceBlock, Carousel, HRBlock
from shop.blocks import FeaturedProducts
from blog.blocks import FeaturedContents, PromotedSpotlightWithList, PromotedNewsList
from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from django.template.response import TemplateResponse
from .cart.cart import Cart
from django.http import HttpResponseRedirect
from django import forms
import decimal
from wagtail.core.models import Site
from django.utils.translation import ugettext_lazy as _
from wagtail.search import index
from wagtailstreamforms.blocks import WagtailFormBlock
from django.conf import settings
from .blocks import ProductBlock
from users.models import User
from wagtailmetadata.models import MetadataPageMixin
from wagtail.admin.edit_handlers import PageChooserPanel
from common.socialmeta import CollectionMixin
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from shop.cart.cart import Cart


@receiver(user_logged_in)
def set_default_currency(request, user, **kwargs):
    if hasattr(request.session,'currency') and request.session['currency'] != user.default_currency:
        cart = Cart(request.session)
        cart.clear()
    if user.default_currency:
        request.session['currency'] = user.default_currency
    else:
        request.session['currency'] = 'NGN'

class JSONResponse(HttpResponse):
	"""An HttpResponse that renders its content into JSON."""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)


class ProductTag(TaggedItemBase):
    content_object = ParentalKey(
        'Product',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

@register_setting
class ShopSettings(BaseSetting):
    default_currency_symbol = models.CharField(default="N", max_length=3, help_text="Default should be naira symbol")
    exchange_rate = models.IntegerField(default=380, help_text="1USD in NGN")



class ShopIndexPage(MetadataPageMixin, Page):
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
    def get_context(self, request):
        context = super().get_context(request)
        context['products'] = Product.objects.live()
        return context
    class Meta:
        verbose_name_plural = 'Shop Home'
        verbose_name = 'Shop Home'


class Product(MetadataPageMixin, RoutablePageMixin, Page):
    date = models.DateField("Post date")
    sku = models.CharField(max_length=255)
    short_description = models.TextField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    old_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    is_featured = models.BooleanField(default=False, blank=True, null=True)
    is_unlisted = models.BooleanField(default=False, blank=True, null=True)
    is_downloadable = models.BooleanField(default=False, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    star_ticket = models.BooleanField(default=False, blank=True, null=True)
    product_type = models.CharField(max_length=20, default="default", choices=settings.PRODUCT_TYPE)
    seat = models.IntegerField(blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_in_stock = models.BooleanField(default=True)
    ticket_class = models.CharField(max_length=50, blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tags = ClusterTaggableManager(through=ProductTag, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('product_type'),
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('is_featured'),
            FieldPanel('is_unlisted'),
            InlinePanel('product_categories', label='category'),
            FieldPanel('seller')
        ], heading="Product information"),
        FieldPanel('sku'),
        FieldPanel('price'),
        FieldPanel('old_price'),
        ImageChooserPanel('image'),
        FieldPanel('short_description'),
        FieldPanel('description', classname="full"),
        MultiFieldPanel([
            FieldPanel('is_downloadable'),
            DocumentChooserPanel('document'),
        ], heading="Virtual Products"),
        MultiFieldPanel([
            FieldPanel('ticket_class'),
            FieldPanel('star_ticket'),
            FieldPanel('seat', help_text="Applicable if product type is ticket"),
        ], heading="Ticketing"),
        InlinePanel('custom_fields', label='Custom fields'),
        InlinePanel('specifications', label='Technical Specification'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]
    def get_context(self, request):
        context = super().get_context(request)
        fields = []
        for f in self.custom_fields.get_object_list():
            if f.options:
                f.options_array = f.options.split('|')
                fields.append(f)
            else:
                fields.append(f)
        context['custom_fields'] = fields
        fields = []
        for f in self.specifications.get_object_list():
            fields.append(f)
        context['specifications'] = fields
        return context

    @route(r'^item/(?P<pk>[-\w]+)/$')
    def item(self, request, pk):
        item = Product.objects.get(pk=pk)
        data = {
            "id": item.pk,
            "price": self.get_currency_price(item.price, 'USD'),
            # "url": self.reverse_subpage('item', args=(pk, )),
            "image": item.get_site().root_url + item.image.get_rendition('fill-50x50').url,
            "url": item.get_url() + self.reverse_subpage('item', args=(pk, )),
        }
        print(data)   
        return JSONResponse(data, status=200)

    def get_currency_price(self, price, currency): 
        if currency and currency == "USD":
            rate = 360
            price = float(price) / rate
            return "%.2f" % round(price, 2)
        else:
            return float(price)

    def current_price(self, currency, rate):
        if currency == "NGN":
            return self.price
        else:
            return self.price / rate
        


class Collection(CollectionMixin, Page):
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    content_panels = Page.content_panels + [
        ImageChooserPanel('icon'),
        InlinePanel('category_collections', label="Featured Categories"),
        InlinePanel('featured_products_collection', label="Featured Products"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['products'] = Product.objects.child_of(self).live()
        return context

    class Meta:
        verbose_name_plural = 'collections'
        verbose_name = 'collection'

class ProductCategory(Page):
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('icon'),
        InlinePanel('featured_products', label="Featured Products"),
    ]

    class Meta:
        verbose_name_plural = 'product categories'
        verbose_name = 'product category'

class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'shop.Product',
        related_name='+',
        on_delete=models.CASCADE
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
    ]

    class Meta:
        abstract = True

class FeaturedProduct(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True

class ProductFeaturedProduct(Orderable, FeaturedProduct):
    page = ParentalKey('ProductCategory', related_name='featured_products')

class CollectionFeaturedProduct(Orderable, FeaturedProduct):
    page = ParentalKey('shop.Collection', related_name='featured_products_collection')

class CategoryCollectionMap(models.Model):
    page = ParentalKey('shop.Collection', on_delete=models.CASCADE, related_name='category_collections')
    product_category = models.ForeignKey(
        'shop.ProductCategory', on_delete=models.CASCADE, related_name='categories_pages'
    )
    panels = [
        PageChooserPanel('product_category'),
    ]
    class Meta:
        unique_together = ('page', 'product_category')
        
class ProductPageProductCategory(models.Model):
    page = ParentalKey('shop.Product', on_delete=models.CASCADE, related_name='product_categories')
    product_category = models.ForeignKey(
        'shop.ProductCategory', on_delete=models.CASCADE, related_name='product_pages'
    )
    panels = [
        PageChooserPanel('product_category'),
    ]
    class Meta:
        unique_together = ('page', 'product_category')
        
class ProductGalleryImage(Orderable):
    page = ParentalKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

class ProductCustomField(Orderable):
    product = ParentalKey(Product, on_delete=models.CASCADE, related_name='custom_fields')
    name = models.CharField(max_length=255)
    options = models.CharField(max_length=500, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('options')
    ]

class ProductSpecificationField(Orderable):
    product = ParentalKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=255)
    option = models.CharField(max_length=500, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('option')
    ]

class OrderQuerySet(models.QuerySet):
    def for_site(self, site):
        """Return all orders for a specific site."""
        return self.filter(site=site)

class AbstractOrder(models.Model):
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(_("Title"), max_length=255) #order reference
    author = models.ForeignKey(User, related_name='author', on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(_("Email"))
    username = models.CharField(_("Username"), max_length=255, blank=True, null=True)
    unique_items = models.IntegerField(_("Unique Items"), blank=True, null=True)
    quantity = models.IntegerField(_("Quantity"), default=1)
    total = models.DecimalField(decimal_places=2, max_digits=10)
    payment_gateway = models.CharField(_("Payment Gateway"), max_length=255, blank=True, null=True)
    ref = models.CharField(_("Payment Reference"), max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=10, default="NGN", choices=settings.CURRENCY)
    is_delivered = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrderQuerySet.as_manager()

    settings_panels = [
        MultiFieldPanel([
            FieldPanel("email"),
        ], _("Contact")),
        MultiFieldPanel([
            FieldPanel("is_delivered"),
            FieldPanel("is_shipped"),
            FieldPanel("is_received"),
        ], _("Flags")),
        FieldPanel("title", classname="full"),
        FieldPanel("username"),
        FieldPanel("unique_items"),
        FieldPanel("quantity"),
        FieldPanel("total"),
        FieldPanel("ref"),
        FieldPanel("payment_gateway"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(settings_panels, heading=_("Order")),
        ]
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ["title"]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

class Order(index.Indexed, AbstractOrder):
    search_fields = [
        index.SearchField('title', partial_match=True),
        index.SearchField('email', partial_match=True),
    ]

class OrderItemQuerySet(models.QuerySet):
    def for_site(self, site):
        """Return all order items for a specific site."""
        return self.filter(site=site)

class OrderItem(index.Indexed, models.Model):
    order = models.ForeignKey(
        'shop.Order',
        on_delete=models.CASCADE,
        related_name='+'
    )
    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    buyer = models.ForeignKey(User, related_name='buyer', on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(User, related_name='seller', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(_("Title"), max_length=255) #product name
    email = models.EmailField(_("Email"))
    username = models.CharField(_("Username"), max_length=255, blank=True, null=True)
    quantity = models.IntegerField(_("Quantity"), default=1)
    total = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    payment_gateway = models.CharField(_("Payment Gateway"), max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=10, default="NGN", choices=settings.CURRENCY)
    ref = models.CharField(_("Payment Reference"), max_length=255, blank=True, null=True)
    is_delivered = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrderItemQuerySet.as_manager()

    settings_panels = [
        MultiFieldPanel([
            FieldPanel("email"),
        ], _("Contact")),
        MultiFieldPanel([
            FieldPanel("order"),
            FieldPanel("product"),
        ], _("Association")),
        MultiFieldPanel([
            FieldPanel("is_delivered"),
            FieldPanel("is_shipped"),
            FieldPanel("is_received"),
        ], _("Flags")),
        FieldPanel("title", classname="full"),
        FieldPanel("email"),
        FieldPanel("username"),
        FieldPanel("quantity"),
        FieldPanel("price"),
        FieldPanel("total"),
        FieldPanel("ref"),
        FieldPanel("payment_gateway"),
    ]

    search_fields = [
        index.SearchField('title', partial_match=True),
        index.SearchField('email', partial_match=True),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(settings_panels, heading=_("Order Items")),
        ]
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Order Items'
        verbose_name = 'Order Item'

class CartPage(RoutablePageMixin, MetadataPageMixin, Page): 
    header = StreamField([
        ('header', WebsiteHeader()),
        ('empty', EmptyBlock()),
    ], blank=True, null=True)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),
        ('HTML', blocks.RawHTMLBlock()),
        ('product', ProductBlock()),
        ('line', HRBlock()),
    ],blank=True, null=True)
    description = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),
        ('HTML', blocks.RawHTMLBlock())
    ],blank=True, null=True)
    thankyou_body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('embed', EmbedBlock()),
        ('HTML', blocks.RawHTMLBlock()),
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
        StreamFieldPanel('description'),
        StreamFieldPanel('thankyou_body', help_text="Create the 'Thank you' page"),
        StreamFieldPanel('footer'),
    ]
    @route(r'^$')
    def base(self, request):
        return TemplateResponse(
          request,
          self.get_template(request),
          self.get_context(request)
        )

    @route(r'^add/$')
    def add(self, request):
        if request.POST:
            cart = Cart(request.session)
            product = Product.objects.get(pk=request.POST.get('product_id'))
            quantity = request.POST.get('quantity', request.POST.get('quantity'))
            discount = request.POST.get('discount', 0)
            price = product.price - decimal.Decimal(discount)
            cart.add(product, price, quantity)
        return HttpResponseRedirect(self.url)

    @route(r'^set-quantity/$')
    def set_quantity(self, request):
        if request.POST:
            cart = Cart(request.session)
            product = Product.objects.get(pk=request.POST.get('product_id'))
            quantity = request.POST.get('quantity')
            cart.set_quantity(product, quantity)
        return HttpResponseRedirect(self.url)
        
    @route(r'^remove/$')
    def remove(self, request):
        if request.POST:
            cart = Cart(request.session)
            product = Product.objects.get(pk=request.POST.get('product_id'))
            cart.remove(product)
        return HttpResponseRedirect(self.url)
    
    @route(r'^remove-single/$')
    def remove_single(self, request):
        if request.POST:
            cart = Cart(request.session)
            product = Product.objects.get(pk=request.POST.get('product_id'))
            cart.remove_single(product)
        return HttpResponseRedirect(self.url)
    
    @route(r'^clear/$')
    def clear(self, request):
        cart = Cart(request.session)
        cart.clear()
        return HttpResponseRedirect(self.url)
    
    @route(r'^checkout/$')
    def checkout(self, request):
        if request.POST and request.POST['trxref']:
            # TODO: Validate Paystack
            if hasattr(request.session, 'currency') and request.session.currency == 'USD':
                currency = request.session.currency
                payment_gateway="snipcart"
            elif hasattr(request.session, 'currency') and request.session.currency == 'NGN':
                currency = request.session.currency
                payment_gateway="paystack"
            else:
                currency = 'NGN'
                payment_gateway="paystack"
            cart = Cart(request.session)
            order = Order(title=request.POST['trxref'], email=request.user.email, 
                username=request.user.username, unique_items=cart.unique_count,
                author=request.user,
                quantity=cart.count, total=cart.total, payment_gateway=payment_gateway,
                ref=request.POST['trxref'],
                currency=currency)
            order.save()
            for item in cart.items:
                oi = OrderItem(order=order, product=item.product, seller=item.product.seller,
                title=item.product.title, email=request.user.email, username=request.user.username,
                quantity=item.quantity, total=item.quantity*item.price, buyer=request.user,
                currency=currency,
                price=item.price, payment_gateway=payment_gateway,ref=request.POST['trxref'])
                oi.save()
            user = User.objects.get(pk=request.user.pk)
            user.default_currency = currency
            user.save()
            cart.clear()
            return HttpResponseRedirect(self.url + self.reverse_subpage('thanks'))
        return HttpResponseRedirect(self.url + self.reverse_subpage('create'))

    @route(r'^submit-thank-you/$')
    def thanks(self, request):
        return TemplateResponse(
          request,
           'shop/checkout_thank_you.html',
           { "page" : self, "self": self }
        )