# Generated by Django 2.0.13 on 2019-10-23 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customimage',
            name='alt_text',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
