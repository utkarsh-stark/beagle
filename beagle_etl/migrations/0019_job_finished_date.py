# Generated by Django 2.2.10 on 2020-06-08 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beagle_etl', '0018_assay_hold'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='finished_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
