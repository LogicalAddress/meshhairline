# Generated by Django 3.0.8 on 2020-08-10 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebsiteSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(blank=True, default='Meshhairline', help_text='Logo Link', max_length=255, null=True)),
                ('contact_email', models.CharField(blank=True, default='only1mesh@gmail.com', max_length=255, null=True)),
                ('logo_url', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter_link', models.CharField(blank=True, default='https://twitter.com/meshhairline', max_length=255, null=True)),
                ('facebook_link', models.CharField(blank=True, default='https://web.facebook.com/MeshHairline', max_length=255, null=True)),
                ('instagram_link', models.CharField(blank=True, default='https://www.instagram.com/meshhairline', max_length=255, null=True)),
                ('youtube_link', models.CharField(blank=True, default='https://www.youtube.com/channel/UCVdcKDTyzJBhld9MfrZ4_1w', max_length=255, null=True)),
                ('linkedin_link', models.CharField(blank=True, max_length=255, null=True)),
                ('ticktok_link', models.CharField(blank=True, max_length=255, null=True)),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]