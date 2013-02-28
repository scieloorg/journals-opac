from django.conf import settings
from celery import task

from .sync import datacollector
from .sync import dataloader
from .sync import pipes
from . import functions
from catalog import models


@task(name='utils.tasks.build_catalog')
def build_catalog():
    """
    Builds the catalog based on the selected Collections and Journals.
    Important! All catalog public data are erased and reconstructed
    when you perform this operation.
    """
    ppl = pipes.Pipeline(pipes.PIssue,
                         pipes.PMission,
                         pipes.PSection,
                         pipes.PNormalizeJournalTitle,
                         pipes.PCleanup)

    data = functions._what_to_sync()
    transformed_data = ppl.run(data)

    marreta = dataloader.Marreta(settings=settings)
    marreta.rebuild_collection('journals', transformed_data)


def sync_collections_meta(managerapi_dep=datacollector.SciELOManagerAPI):
    """
    Fetches the metadata about available Collections in order for the
    user to configure the catalog instance.
    """
    scielo_api = managerapi_dep(settings=settings)
    data = scielo_api.get_all_collections()

    for col in data:
        models.CollectionMeta.objects.get_or_create(
            resource_uri=col.get('resource_uri', ''),
            name=col.get('name', ''),
            name_slug=col.get('name_slug', '')
        )


def sync_journals_meta(managerapi_dep=datacollector.SciELOManagerAPI):
    """
    Fetches the metadata about Journals bound to Collections marked as
    members in order for the user to configure the catalog instance.
    """
    scielo_api = managerapi_dep(settings=settings)

    collections = [c.name_slug for c in models.CollectionMeta.objects.members()]

    data = scielo_api.get_all_journals(*collections)

    cols_memo = {}
    for col in data:
        collection = col.get('collections')

        if collection not in cols_memo:
            cols_memo[collection] = (
                models.CollectionMeta.objects.get(
                    resource_uri=collection)
            )

        models.JournalMeta.objects.get_or_create(
            resource_uri=col.get('resource_uri', ''),
            name=col.get('title', ''),
            collection=cols_memo[collection],
        )
