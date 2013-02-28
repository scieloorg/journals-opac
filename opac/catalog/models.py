from django.db import models


class CustomMetaManager(models.Manager):
    def members(self):
        qset = self.get_query_set().filter(is_member=True)

        return qset


class CollectionMeta(models.Model):
    """
    Represents Collection Metadata available to be part
    of the catalog.

    The entity selected as a member of the catalog must
    have the attribute ``is_member`` set to True.
    """
    objects = CustomMetaManager()

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
    objects = CustomMetaManager()

    is_member = models.BooleanField(default=False)
    resource_uri = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    collection = models.ForeignKey(CollectionMeta, related_name='journals')

    class Meta:
        verbose_name = u'Journal Meta'
        verbose_name_plural = u'Journals Meta'

    def __unicode__(self):
        return self.name

    @property
    def resource_id(self):
        cleaned = [seg for seg in self.resource_uri.split('/') if seg]
        return cleaned[-1]


class Sync(models.Model):
    """
    Represents an incremental sync event.
    """
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)
    last_seq = models.IntegerField(default=0)
