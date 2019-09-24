# Generated by Django 2.0.13 on 2019-09-24 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190516_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategory',
            name='slug',
            field=models.SlugField(help_text='The name of this category in the URL.\n        Often just the same as the name in lowercase.', max_length=80, unique=True),
        ),
    ]