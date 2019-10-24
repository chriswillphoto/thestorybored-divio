from django.db import models
import django.forms

from rest_framework import serializers

from wagtail.images.models import Image
from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.models import register_snippet

from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField

from images.models import CustomImage
from home.models import CustomImageRenditionField

# from users import User

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        max_length=80,
        help_text='''The name of this category in the URL.
        Often just the same as the name in lowercase.'''
        )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class BlogIndex(Page):
    banner = models.ForeignKey(CustomImage, on_delete=models.SET_NULL, null=True)
    intro = models.TextField(blank=True)
    subheading = models.CharField(max_length=120, blank=True)

    categories = BlogCategory.objects.all()

    content_panels = Page.content_panels + [
        ImageChooserPanel('banner'),
        FieldPanel('subheading'),
        FieldPanel('intro', classname='full'),
    ]

    api_fields = [
        APIField('banner'),
        APIField('banner_resized', serializer=ImageRenditionField('width-1800|jpegquality-80', source='banner')),
        APIField('intro'),
        APIField('subheading'),
        APIField('categories', serializer=serializers.StringRelatedField(many=True))
    ]

    parent_page_types = ['home.HomePage']

    max_count = 1

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomImage
        fields = ['title', 'file', 'caption', 'alt_text', 'width', 'height', 'file_size', 'focal_point_x', 'focal_point_y', 'focal_point_width', 'focal_point_height']

class APIImageChooserBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        return ImageSerializer(context=context).to_representation(value)

class BlogPost(Page):
    # author = models.ForeignKey('users.User', related_name='blogposts', on_delete=models.SET_NULL, null=True, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    banner = models.ForeignKey(CustomImage, on_delete=models.SET_NULL, null=True)
    date = models.DateField("Post date")
    body = StreamField([
        # ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', APIImageChooserBlock()),
        ('key_quote', blocks.CharBlock(icon='openquote')),
    ])
    welcome_quote = RichTextField(blank=True, features=['bold', 'link'])
    welcome_quote_image = models.ForeignKey(CustomImage, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_welcome_quote_img')
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    # author_object = User.objects.get(id=author)
    # author_name = author_object.get_full_name()

    content_panels = Page.content_panels + [
        # FieldPanel('author'),
        FieldPanel('subtitle'),
        FieldPanel('date'),
        ImageChooserPanel('banner'),
        StreamFieldPanel('body', classname='collapsible'),
        FieldPanel('welcome_quote'),
        ImageChooserPanel('welcome_quote_image'),
        FieldPanel('categories', widget=django.forms.CheckboxSelectMultiple),
    ]

    api_fields = [
        APIField('banner'),
        APIField('banner_resized', serializer=ImageRenditionField('width-1800|jpegquality-80', source='banner')),
        APIField('thumbnail', serializer=ImageRenditionField('fill-160x160|jpegquality-80', source='banner')),
        APIField('owner.get_full_name', serializer=serializers.StringRelatedField()),
        APIField('owner.bio', serializer=serializers.StringRelatedField()),
        APIField('date'),
        APIField('subtitle'),
        APIField('body'),
        APIField('slug'),
        APIField('welcome_quote'),
        APIField('welcome_quote_image', serializer=CustomImageRenditionField('width-1200|jpegquality-80')),
        APIField('categories', serializer=serializers.StringRelatedField(many=True)),
    ]

    parent_page_types = ['BlogIndex']
