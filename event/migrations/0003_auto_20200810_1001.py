# Generated by Django 3.0.8 on 2020-08-10 10:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
        ('wagtailimages', '0022_uploadedimage'),
        ('event', '0002_ticket_product'),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AddField(
            model_name='speaker',
            name='photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='featuredguest',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured_guests', to='event.EventPage'),
        ),
        migrations.AddField(
            model_name='featuredguest',
            name='speaker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='event.Speaker'),
        ),
        migrations.AddField(
            model_name='eventticket',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_tickets', to='event.EventPage'),
        ),
        migrations.AddField(
            model_name='eventticket',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='shop.Product'),
        ),
        migrations.AddField(
            model_name='eventsponsor',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_sponsors', to='event.EventPage'),
        ),
        migrations.AddField(
            model_name='eventsponsor',
            name='sponsor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='event.Sponsor'),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='cover_photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='event_photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='search_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Search image'),
        ),
        migrations.AddField(
            model_name='eventagenda',
            name='agenda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='event.Agenda'),
        ),
        migrations.AddField(
            model_name='eventagenda',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_agendas', to='event.EventPage'),
        ),
        migrations.AddField(
            model_name='agendaspeakerrelationship',
            name='agenda',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='agenda_speakers_relationship', to='event.Agenda'),
        ),
        migrations.AddField(
            model_name='agendaspeakerrelationship',
            name='speaker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='event.Speaker'),
        ),
        migrations.AlterUniqueTogether(
            name='featuredguest',
            unique_together={('page', 'speaker')},
        ),
        migrations.AlterUniqueTogether(
            name='eventticket',
            unique_together={('page', 'ticket')},
        ),
        migrations.AlterUniqueTogether(
            name='eventsponsor',
            unique_together={('page', 'sponsor')},
        ),
        migrations.AlterUniqueTogether(
            name='eventagenda',
            unique_together={('page', 'agenda')},
        ),
        migrations.AlterUniqueTogether(
            name='agendaspeakerrelationship',
            unique_together={('agenda', 'speaker')},
        ),
    ]