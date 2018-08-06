
from django.db import models


class CmsPage(models.Model):
    page_id = models.SmallIntegerField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    root_template = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    identifier = models.CharField(max_length=100, blank=True, null=True)
    content_heading = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    creation_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    is_active = models.SmallIntegerField()
    sort_order = models.SmallIntegerField()
    layout_update_xml = models.TextField(blank=True, null=True)
    custom_theme = models.CharField(max_length=100, blank=True, null=True)
    custom_root_template = models.CharField(
        max_length=255, blank=True, null=True)
    custom_layout_update_xml = models.TextField(blank=True, null=True)
    custom_theme_from = models.DateField(blank=True, null=True)
    custom_theme_to = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cms_page'
        app_label = "magento"
