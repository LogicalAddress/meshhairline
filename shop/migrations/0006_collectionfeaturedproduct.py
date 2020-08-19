# Generated by Django 3.0.8 on 2020-08-10 10:53

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_delete_categorycollection'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionFeaturedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='shop.Product')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured_products_collection', to='shop.Collection')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
