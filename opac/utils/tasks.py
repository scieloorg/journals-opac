import itertools

from django.conf import settings
from celery import task

from .sync import datacollector
from .sync import dataloader
from .sync import pipes
from catalog import models
from catalog import mongomodels


def _get_user_catalog_definitions():
    """
    It analyses the choices the user made, and returns a list
    in the form:
    [[<collection_name_slug>,], [<journal>,]]
    """
    collections = models.CollectionMeta.objects.members()

    full_collections = []
    journals_a_la_carte = []

    for collection in collections:
        # decide if the entire collection must be synced or only some
        # journals.
        if collection.journals.members().exists():
            journals_a_la_carte = collection.journals.members()
        else:
            full_collections.append(collection)

    return [full_collections, journals_a_la_carte]


def _what_to_sync(managerapi_dep=datacollector.SciELOManagerAPI):
    """
    Returns an iterator containing all journals that must be synced
    to build the catalog.

    If the collection is marked as member, and has some
    journals that are also marked as members, we assume
    only these journals must be synchronized. Else,
    sync all its journals.
    """
    scielo_api = managerapi_dep(settings=settings)
    full_collections, journals_a_la_carte = _get_user_catalog_definitions()

    full_collections = (c.name_slug for c in full_collections)
    journals_a_la_carte = (j.resource_id for j in journals_a_la_carte)

    return itertools.chain(
        scielo_api.get_all_journals(*full_collections),
        scielo_api.get_journals(*journals_a_la_carte)
    )


def _what_have_changed(managerapi_dep=datacollector.SciELOManagerAPI):
    """
    Returns an iterator containing all journals that must be created
    or updated in order to keep the catalog updated.
    """
    scielo_api = managerapi_dep(settings=settings)
    full_collections, journals_a_la_carte = _get_user_catalog_definitions()

    data = scielo_api.get_changes()

    return identify_changes(data, full_collections, journals_a_la_carte)


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

    data = _what_to_sync()
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


def _list_issues_uri(journal_meta, journal_dep=mongomodels.Journal):
        # TODO: This instantiation logic must be at Journal.get_journal
        journal_data = journal_dep.objects.find_one({'id': journal_meta.resource_id})
        journal_doc = journal_dep(**journal_data)
        return (issue.resource_uri for issue in journal_doc.list_issues())


def identify_changes(changes,
                     collections,
                     journals,
                     list_issues_uri_dep=_list_issues_uri):
    """
    Returns a list of ``object_uri`` that must be
    synced.

    ``changes`` is an iterable where each element is an
    entry in changes API.

    ``collections`` is an iterable of collections
    that must have all its journals synced.

    ``journals`` is an iterable of journals that must
    be synced.
    """
    journals_list = []
    issues_list = []

    # list uris from all journals and its issues
    for j in journals:
        journals_list.append(j.resource_uri)
        issues_list.append(list_issues_uri_dep(j))

    collections_uris = (c.resource_uri for c in collections)
    journals_uris = journals_list
    issues_uris = itertools.chain(*issues_list)
    super_set = set().union(collections_uris, journals_uris, issues_uris)

    changed = set()
    for change_rec in changes:
        if change_rec.get('collection_uri') in super_set or (
            change_rec.get('object_uri') in super_set):

            changed.add(change_rec.get('object_uri'))

    return list(changed)
