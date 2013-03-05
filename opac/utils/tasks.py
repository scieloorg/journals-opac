from datetime import datetime

from django.conf import settings
from django.db import transaction
from celery import task

from .sync import datacollector
from .sync import dataloader
from . import functions
from catalog import models


@task(name='utils.tasks.build_catalog')
def build_catalog():
    """
    Builds the catalog based on the selected Collections and Journals.
    Important! All catalog public data are erased and reconstructed
    when you perform this operation.
    """
    ppl = functions.make_journal_pipeline()

    data = functions._what_to_sync()
    transformed_data = ppl.run(data)

    marreta = dataloader.Marreta(settings=settings)
    marreta.rebuild_collection('journals', transformed_data)

    models.Sync.objects.create(ended_at=datetime.now(),
        last_seq=60, status='finished')


def update_catalog(managerapi_dep=datacollector.SciELOManagerAPI):
    scielo_api = managerapi_dep(settings=settings)
    journal_ppl = functions.make_journal_pipeline()

    with transaction.commit_on_success():
        sync = models.Sync.objects.create()

        changes = functions._what_have_changed(since=functions.get_last_seq())
        changed_journals = changes.show('journals', unique=True)
        # changed_issues = changes.show('issues', unique=True)

        changed_journals_ids = [ch.resource_id for ch in changed_journals]
        # changed_issues_ids = [ch.resource_id for ch in changed_issues]

        journals_data = scielo_api.get_journals(*changed_journals_ids)
        # issues_data = scielo_api.get_issues(*changed_issues_ids)

        transformed_journals_data = journal_ppl.run(journals_data)

        marreta = dataloader.Marreta(settings=settings)
        marreta.update_collection('journals', transformed_journals_data)

        sync.last_seq = changes.last_seq
        sync.status = 'finished'
        sync.ended_at = datetime.now()
        sync.save()


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
