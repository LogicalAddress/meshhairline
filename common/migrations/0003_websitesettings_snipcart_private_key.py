# Generated by Django 3.0.8 on 2020-10-10 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20200811_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='websitesettings',
            name='snipcart_private_key',
            field=models.CharField(blank=True, help_text='Your Snipcart private API key', max_length=255, null=True),
        ),
    ]
