from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django_countries.fields import CountryField
from wagtail.snippets.models import register_snippet
from wagtail.core.models import Page
from common.blocks import WebsiteHeader, WebsiteFooter, EmptyBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailstreamforms.blocks import WagtailFormBlock
from common.blocks import Spotlight, TwoColGridImage
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core import blocks
from blog.blocks import FeaturedContents
from shop.blocks import FeaturedProducts
from common.blocks import Carousel, TwoColTextLeft, TwoColTextRight, IntroduceBlock
from django.core.exceptions import PermissionDenied
from blog.blocks import PromotedNewsList, PromotedSpotlightWithList
from shop.blocks import ProductBlock
from common.blocks import HRBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from shop import get_model as get_shop_model
from django.http import Http404
from wagtailmetadata.models import MetadataPageMixin


class Dashboard(RoutablePageMixin, MetadataPageMixin, Page):
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

    @route(r'^$')
    def base(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account_login'))
        orders = get_shop_model('shop.Order').objects.filter(author=request.user).order_by('-id')[:10]
        context = self.get_context(request)
        context['orders'] = orders
        return TemplateResponse(request, self.get_template(request), context)

    @route(r'^orders/$')
    def orders(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account_login'))
        orders = get_shop_model('shop.Order').objects.filter(author=request.user).order_by('-id')[:10]
        context = self.get_context(request)
        context['orders'] = orders
        return render(request, "dashboard/orders.html", context)
    
    @route(r'^orders/(?P<pk>[-\w]+)/$')
    def order(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account_login'))
        items = get_shop_model('shop.OrderItem').objects.filter(order=pk, buyer=request.user).order_by('-id')
        order = get_shop_model('shop.Order').objects.get(pk=pk)
        if not items:
            raise Http404
        context = self.get_context(request)
        context['items'] = items
        context['order'] = order
        return render(request, "dashboard/order_items.html", context)

