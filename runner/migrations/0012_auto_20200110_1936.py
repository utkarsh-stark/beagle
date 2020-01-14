# Generated by Django 2.2.8 on 2020-01-10 19:36

from django.db import migrations


def extract_request_id_from_filename(name):
    if name.startswith('ACCESS'):
        request = name.split(': ')[1]
        request = request.split(',')[0]
        return request
    elif name.startswith('FLATBUSH'):
        request = name.split(': ')[1]
        request = request.split(',')[0]
        return request
    elif name.startswith('ROSLIN'):
        request = name.split(' ')[1]
        request = request.split(',')[0]
        return request
    return None


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0011_run_tags'),
    ]

    def populate_request_ids_in_tags(apps, schema_editor):
        '''
        We can't import the Post model directly as it may be a newer
        version than this migration expects. We use the historical version.
        '''
        Run = apps.get_model('runner', 'Run')
        runs = Run.objects.all()
        for run in runs:
            try:
                request_id = extract_request_id_from_filename(run.name)
            except Exception:
                print("Failed to extract requestId for Run:%s" % run.name)
                continue
            if request_id and not run.tags.get('requestId'):
                run.tags = {'requestId': request_id}
                run.save()

    operations = [
        migrations.RunPython(populate_request_ids_in_tags),
    ]
