from django.db import models

from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField

from django.core.exceptions import ValidationError

from images.models import CustomImage

from rest_framework import serializers


from home.models import CustomImageRenditionField

# Create your models here.

class AboutPage(Page):
    hero_banner = models.ForeignKey(CustomImage, on_delete=models.SET_NULL, null=True)
    subheading = models.CharField(max_length=250, blank=True)
    welcome_quote = RichTextField(blank=True, features=['bold', 'link'])
    welcome_quote_image = models.ForeignKey(CustomImage, on_delete=models.SET_NULL, null=True, blank=True, related_name='about_welcome_quote_img')
    about_text = RichTextField(blank=True)
    about_image = models.ImageField(upload_to="homepage", blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_banner'),
        FieldPanel('welcome_quote'),
        ImageChooserPanel('welcome_quote_image'),
        FieldPanel('subheading'),
        # MultiFieldPanel(
        #     [
        #         FieldPanel('info_heading_1'),
        #         FieldPanel('info_box_1', classname="full"),
        #         FieldPanel('info_heading_2'),
        #         FieldPanel('info_box_2', classname="full"),
        #         FieldPanel('info_heading_3'),
        #         FieldPanel('info_box_3', classname="full"),
        #         FieldPanel('info_heading_4'),
        #         FieldPanel('info_box_4', classname="full")
        #     ],
        #     heading='Info boxes',
        #     classname='collapsible'
        # ),
        FieldPanel('about_text', classname="full"),
        FieldPanel('about_image'),
    ]


    api_fields = [
        APIField('hero_banner'),
        APIField('hero_banner_resized', serializer=CustomImageRenditionField('width-1800|jpegquality-80', source='hero_banner')),
        APIField('welcome_quote'),
        APIField('welcome_quote_image', serializer=CustomImageRenditionField('width-1200|jpegquality-80')),
        APIField('subheading'),
        APIField('about_text'),
        APIField('about_image'),
    ]

    max_count = 1
    parent_page_types = ['home.HomePage']
