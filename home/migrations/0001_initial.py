# Generated by Django 2.0.13 on 2019-05-16 00:01

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('welcome_quote', wagtail.core.fields.RichTextField(blank=True)),
                ('subheading', models.CharField(blank=True, max_length=250)),
                ('intro_about', wagtail.core.fields.RichTextField(blank=True)),
                ('intro_about_image', models.ImageField(blank=True, upload_to='homepage')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]