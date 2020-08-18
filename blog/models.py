from django.db import models
from django import forms
from modelcluster.fields import ParentalKey, ParentalManyToManyField

# Create your models here.
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.search import index
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.snippets.models import register_snippet
from wagtail.images.blocks import ImageChooserBlock
from common.blocks import WebsiteHeader, WebsiteFooter, EmptyBlock, Carousel, TwoColGridImage
from wagtailstreamforms.blocks import WagtailFormBlock
from wagtail.embeds.blocks import EmbedBlock
from common.blocks import IntroduceBlock, TwoColTextRight, TwoColTextLeft, HRBlock
from common.blocks import Spotlight
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import PageChooserPanel
from shop.blocks import ProductBlock, FeaturedProducts
from blog.blocks import PromotedNewsList, PromotedSpotlightWithList, FeaturedContents
from wagtailmetadata.models import MetadataPageMixin

class BlogPage(MetadataPageMixin, Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('form', WagtailFormBlock()),
        ('embed', EmbedBlock()),
        ('HTML', blocks.RawHTMLBlock()),
        ('Carousel', Carousel()),
        ('TwoColGridImage', TwoColGridImage()),
        ('spotlight', Spotlight()),
        ('TwoColTextLeft', TwoColTextLeft()),
        ('TwoColTextRight', TwoColTextRight()),
        ('Introduce', IntroduceBlock()),
        ('product', ProductBlock()),
        ('line', HRBlock()),
    ],blank=True, null=True)

    tags = ClusterTaggableManager(through='blog.BlogPageTag', blank=True)
    is_featured = models.BooleanField(default=False)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('is_featured'),
            InlinePanel('categories', label='category'),
        ], heading="Blog information"),
        MultiFieldPanel([
            FieldPanel('intro'),
            ImageChooserPanel('featured_image'),
            StreamFieldPanel('body'),
        ]),
        MultiFieldPanel([
                InlinePanel('authors', label='Author', min_num=1),
            ],
            heading="Author(s)"
        ),
        InlinePanel('related_links', label="Related links"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_siblings().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        fields = []
        for f in self.authors.get_object_list():
            fields.append(f)
        context['authors'] = fields
        return context
    class Meta:
        verbose_name_plural = 'blog page'
        verbose_name = 'blog page'


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'
        verbose_name = 'blog category'

class BlogPageBlogCategory(ClusterableModel):
    page = ParentalKey('blog.BlogPage', on_delete=models.CASCADE, related_name='categories')
    blog_category = models.ForeignKey(
        'blog.BlogCategory', on_delete=models.CASCADE, related_name='blog_pages'
    )
    panels = [
        SnippetChooserPanel('blog_category'),
    ]
    class Meta:
        unique_together = ('page', 'blog_category')

class BlogTagsIndexPage(MetadataPageMixin, Page):
    max_count = 1
    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)
        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context

    class Meta:
        verbose_name_plural = 'Blog Tags'
        verbose_name = 'Blog Tag'
        # app_label = 'blogtag_index_page'

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogIndexPage(MetadataPageMixin, Page):
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
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [ 
        FieldPanel('intro', classname="full"),
        MultiFieldPanel([
            StreamFieldPanel('header'),
            StreamFieldPanel('body'),
            StreamFieldPanel('footer'),
        ], heading='layout')
    ]

    def get_context(self, request):
        # only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    class Meta:
        verbose_name_plural = 'Blog Index'
        verbose_name = 'Blog Index'
        # app_label = 'blog_index_page'


class AuthorsOrderable(Orderable):
    blog = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='authors')
    author = models.ForeignKey(
        "blog.Authors",
        on_delete=models.CASCADE,
    )
    panels = [
        PageChooserPanel("author"),
    ]

class Authors(MetadataPageMixin, Page):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )
    twitter = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel('description'),
                ImageChooserPanel("image"),
            ],
            heading="Bio",
        ),
        MultiFieldPanel([
            FieldPanel('twitter'),
            FieldPanel('linkedin'),
            FieldPanel('facebook'),
            FieldPanel('instagram'),
        ], heading="Social"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        # null=True,
        # blank=True,
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

class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True

class BlogPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('BlogPage', related_name='related_links')

class AuthorIndexPage(MetadataPageMixin, Page):
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
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        MultiFieldPanel([
            StreamFieldPanel('header'),
            StreamFieldPanel('body'),
            StreamFieldPanel('footer'),
        ], heading='layout')
    ]
    class Meta:
        verbose_name = "Authors Index"
        verbose_name_plural = "Authors Index"