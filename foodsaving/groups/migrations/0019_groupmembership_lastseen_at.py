# Generated by Django 2.0.2 on 2018-02-28 16:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0018_group_sent_summary_up_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmembership',
            name='lastseen_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
