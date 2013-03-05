import itertools

from django.conf import settings

from .sync import datacollector
from .sync import pipes
from catalog import models
from catalog import mongomodels


def make_journal_pipeline():
    ppl = pipes.Pipeline(pipes.PIssue,
                         pipes.PMission,
                         pipes.PSection,
                         pipes.PNormalizeJournalTitle,
                         pipes.PCleanup)
    return ppl


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


def _what_have_changed(since=0, managerapi_dep=datacollector.SciELOManagerAPI):
    """
    Returns a dict with the keys ``issues`` and ``journals``, where
    each one is an iterator containing all data that must be created
    or updated in order to keep the catalog updated.
    """
    scielo_api = managerapi_dep(settings=settings)
    full_collections, journals_a_la_carte = _get_user_catalog_definitions()

    data = scielo_api.get_changes(since=since)

    changes_list = datacollector.ChangesList(data)
    changes = changes_list.filter(collections=full_collections,
        journals=journals_a_la_carte)

    return changes


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
    Returns a dict where the keys are ``journals`` and ``issues``
    both containing a list of ``object_uri`` that must be
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

    collections_uris = set(c.resource_uri for c in collections)
    journals_uris = set(journals_list)
    issues_uris = set(itertools.chain(*issues_list))

    changed_journals = set()
    changed_issues = set()

    for change_rec in changes:
        _collection_uri = change_rec.get('collection_uri')
        _object_uri = change_rec.get('object_uri')

        if _collection_uri in collections_uris:
            # identify the endpoint to know how to classify the uri
            endpoint = [seg for seg in _object_uri.split('/') if seg][-2]
            if endpoint == 'journals':
                changed_journals.add(_object_uri)
            elif endpoint == 'issues':
                changed_issues.add(_object_uri)
            else:
                continue
        elif _object_uri in journals_uris:
            changed_journals.add(_object_uri)
        elif _object_uri in issues_uris:
            changed_issues.add(_object_uri)
        else:
            continue

    return {'journals': list(changed_journals), 'issues': list(changed_issues)}


def get_last_seq():
    last_sync = models.Sync.objects.all()[0]

    if last_sync:
        return last_sync.last_seq
    else:
        return 0
