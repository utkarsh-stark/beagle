from django.contrib import admin
from import_export.admin import ExportActionMixin
from .models import Storage, File, FileType, FileMetadata, FileGroup, FileGroupMetadata, FileRunMap, ImportMetadata, Sample

# Register your models here.


class FileAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'file_name', 'file_group', 'size', 'created_date')
    search_fields = ['file_name']


class SampleAdmin(admin.ModelAdmin):
    list_display = ('id', 'sample_id', 'redact')
    search_fields = ['sample_id']


class FileRunMapAdmin(admin.ModelAdmin):
    list_display = ('file', 'run')


class FileMetadataAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('file', 'version', 'metadata','created_date')
    autocomplete_fields = ['file']
    search_fields = ('id', 'file__id', 'metadata__requestId', 'metadata__sampleName')


class ImportMetadataAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('file',)
    search_fields = ('file__id',)


admin.site.register(File, FileAdmin)
admin.site.register(Storage)
admin.site.register(Sample, SampleAdmin)
admin.site.register(FileGroup)
admin.site.register(FileType)
admin.site.register(FileMetadata, FileMetadataAdmin)
admin.site.register(ImportMetadata, ImportMetadataAdmin)
admin.site.register(FileGroupMetadata)
admin.site.register(FileRunMap, FileRunMapAdmin)
