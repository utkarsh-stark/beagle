# Generated by Django 2.2.8 on 2020-01-17 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_system', '0012_migrate_bad_filenames'),
        ('runner', '0013_merge_20200117_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='port',
            name='files',
            field=models.ManyToManyField(to='file_system.File'),
        ),
    ]
