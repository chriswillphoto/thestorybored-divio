from django.db import models

from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel

from django.core.exceptions import ValidationError

from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField

from images.models import CustomImage

from rest_framework import serializers

from wagtail.images.models import SourceImageIOError
from collections import OrderedDict
# Create your models here.

class CustomImageRenditionField(ImageRenditionField):
    def to_representation(self, image):
        try:
            thumbnail = image.get_rendition(self.filter_spec)

            if thumbnail.image.focal_point_x is not None and thumbnail.image.focal_point_y is not None:

                focal_point_x = thumbnail.image.get_focal_point().x / thumbnail.image.width
                focal_point_y = thumbnail.image.get_focal_point().y / thumbnail.image.height
            else:
                focal_point_x = None
                focal_point_y = None

            return OrderedDict([
                ('url', thumbnail.url),
                ('width', thumbnail.width),
                ('height', thumbnail.height),
                ('caption', thumbnail.image.caption),
                ('focal_points', [focal_point_x, focal_point_y]),
            ])
        except SourceImageIOError:
            return OrderedDict([
                ('error', 'SourceImageIOError'),
            ])

class HomePage(Page):

    def save(self, *args, **kwargs):
        if HomePage.objects.exists() and not self.pk:
            raise ValidationError('There can only be one HomePage')
        return super(HomePage, self).save(*args, **kwargs)

    hero_banner = models.ForeignKey(CustomImage, on_delete=models.SET_NULL, null=True)
    welcome_quote = RichTextField(blank=True, features=['bold', 'link'])
    subheading = models.CharField(max_length=250, blank=True)
    intro_about = RichTextField(blank=True)
    intro_about_image = models.ImageField(upload_to="homepage", blank=True)
    # social_banner = models.ImageField(upload_to="homepage", blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_banner'),
        FieldPanel('welcome_quote'),
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
        FieldPanel('intro_about', classname="full"),
        FieldPanel('intro_about_image'),
    ]


    api_fields = [
        APIField('hero_banner'),
        APIField('hero_banner_resized', serializer=CustomImageRenditionField('width-1800|jpegquality-80', source='hero_banner')),
        APIField('welcome_quote'),
        APIField('subheading'),
        APIField('intro_about'),
        APIField('intro_about_image'),
    ]

    max_count = 1
