from django.db import models


class CollectionMeta(models.Model):
    """
    Represents Collection Metadata available to be part
    of the catalog.

    The entity selected as a member of the catalog must
    have the attribute ``is_member`` set to True.
    """
    is_member = models.BooleanField(default=False)
    resource_uri = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    name_slug = models.CharField(max_length=128)

    class Meta:
        verbose_name = u'Collection Meta'
        verbose_name_plural = u'Collections Meta'

    def __unicode__(self):
        return self.name


class JournalMeta(models.Model):
    """
    Represents Journal Metadata available to be part
    of the catalog.

    The entity selected as a member of the catalog must
    have the attribute ``is_member`` set to True.
    """
    is_member = models.BooleanField(default=False)
    resource_uri = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    collection = models.ForeignKey(CollectionMeta, related_name='journals')

    class Meta:
        verbose_name = u'Journal Meta'
        verbose_name_plural = u'Journals Meta'
