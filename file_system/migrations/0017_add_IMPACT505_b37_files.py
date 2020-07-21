# Generated by Django 2.2.11 on 2020-07-21 21:19

from django.db import migrations


def create_IMPACT505_b37_reference_files(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    File = apps.get_model('file_system', 'File')
    FileMetadata = apps.get_model('file_system', 'FileMetadata')
    FileGroup = apps.get_model('file_system', 'FileGroup')
    FileType = apps.get_model('file_system', 'FileType')
    file_group = FileGroup.objects.get(name='Reference Files')
    txt = FileType.objects.get(name='txt')
    ilist = FileType.objects.get(name='ilist')
    interval_list = FileType.objects.get(name='interval_list')
    try:

        file1 = File.objects.create(
            path='/juno/work/ci/resources/genomic_resources/targets/IMPACT505/b37/IMPACT505_FP_tiling_genotypes.txt',
            file_name='IMPACT505_FP_tiling_genotypes.txt',
            file_group=file_group,
            file_type=txt,
            size=0
        )
        file_metadata_1 = FileMetadata.objects.create(
            file=file1,
            version=0,
            metadata={
                "assay": "IMPACT505_b37",
                "data_type": "FP_genotypes"
            }
        )
        print("File created")
    except Exception as e:
        print("Fail to create file")
        print(str(e))
    try:
        file2 = File.objects.create(
            path='/juno/work/ci/resources/genomic_resources/targets/IMPACT505/b37/IMPACT505_b37_targets.ilist',
            file_name='IMPACT505_b37_targets.ilist',
            file_group=file_group,
            file_type=ilist,
            size=0
        )
        file_metadata_2 = FileMetadata.objects.create(
            file=file2,
            version=0,
            metadata={
                "assay": "IMPACT505_b37",
                "data_type": "targets_list"
            }
        )
        print("File created")
    except Exception as e:
        print("Fail to create file")
        print(str(e))
    try:
        file3 = File.objects.create(
            path='/juno/work/ci/resources/genomic_resources/targets/IMPACT505/b37/IMPACT505_b37_baits.ilist',
            file_name='IMPACT505_b37_baits.ilist',
            file_group=file_group,
            file_type=ilist,
            size=0
        )
        file_metadata_3 = FileMetadata.objects.create(
            file=file3,
            version=0,
            metadata={
                "assay": "IMPACT505_b37",
                "data_type": "baits_list"
            }
        )
        print("File created")
    except Exception as e:
        print("Fail to create file")
        print(str(e))
    try:
        file4 = File.objects.create(
            path='/juno/work/ci/resources/genomic_resources/targets/IMPACT505/b37/IMPACT505_FP_tiling_intervals.intervals',
            file_name='IMPACT505_FP_tiling_intervals.intervals',
            file_group=file_group,
            file_type=interval_list,
            size=0
        )
        file_metadata_4 = FileMetadata.objects.create(
            file=file4,
            version=0,
            metadata={
                "assay": "IMPACT505_b37",
                "data_type": "FP_intervals"
            }
        )
        print("File created")
    except Exception as e:
        print("Fail to create file")
        print(str(e))


def revert_migration(apps, schema_editor):
    File = apps.get_model('file_system', 'File')
    try:
        File.objects.get(path='/juno/work/ci/resources/genomic_resources/targets/IMPACT505/b37/IMPACT505_FP_tiling_genotypes.txt').delete()
    except Exception:
        pass
    try:
        File.objects.get(
            path='/juno/work/ci/resources/genomic_resources/targets/IMPACT505/b37/IMPACT505_b37_targets.ilist').delete()
    except Exception:
        pass
    try:
        File.objects.get(
            path='/juno/work/ci/resources/genomic_resources/targets/IMPACT505/b37/IMPACT505_b37_baits.ilist').delete()
    except Exception:
        pass
    try:
        File.objects.get(
            path='/juno/work/ci/resources/genomic_resources/targets/IMPACT505/b37/IMPACT505_FP_tiling_intervals.intervals').delete()
    except Exception:
        pass



class Migration(migrations.Migration):

    dependencies = [
        ('file_system', '0016_merge_20200612_2034'),
    ]

    operations = [
        migrations.RunPython(create_IMPACT505_b37_reference_files, reverse_code=revert_migration),
    ]
