import itertools

from django.conf import settings

from .sync import datacollector
from .sync import pipes
from catalog import models
from catalog import mongomodels


def make_journal_pipeline():
    """
    Returns a ``pipes.Pipeline`` instance wired with
    all the pipes needed to transform journals data.
    """
    ppl = pipes.Pipeline(pipes.PIssue,
                         pipes.PMission,
                         pipes.PSection,
                         pipes.PNormalizeJournalTitle,
                         pipes.PCleanup)
    return ppl


def get_user_catalog_definitions():
    """
    Analyses the choices the user made, and returns a list
    in the form:
    [[<collection>,], [<journal>,]]
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


def get_all_data_for_build(managerapi_dep=datacollector.SciELOManagerAPI):
    """
    Returns an iterator containing all journals that must be synced
    to build the catalog.

    If the collection is marked as member, and has some
    journals that are also marked as members, we assume
    only these journals must be synchronized. Else,
    sync all its journals.
    """
    scielo_api = managerapi_dep(settings=settings)
    full_collections, journals_a_la_carte = get_user_catalog_definitions()

    full_collections = (c.name_slug for c in full_collections)
    journals_a_la_carte = (j.resource_id for j in journals_a_la_carte)

    return itertools.chain(
        scielo_api.get_all_journals(*full_collections),
        scielo_api.get_journals(*journals_a_la_carte)
    )


def get_all_changes(since=0, managerapi_dep=datacollector.SciELOManagerAPI):
    """
    Returns a ``utils.datacollector.ChangesList`` instance
    containing all data that must be created or updated in
    order to keep the catalog updated.
    """
    scielo_api = managerapi_dep(settings=settings)
    full_collections, journals_a_la_carte = get_user_catalog_definitions()

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


def get_last_seq():
    """

    """
    last_sync = models.Sync.objects.all()[0]

    if last_sync:
        return last_sync.last_seq
    else:
        return 0


def get_remote_last_seq(managerapi_dep=datacollector.SciELOManagerAPI):
    """
    Gets the last seq shown at the SciELO Manager's Changes API.

    This function should not be used in a frequent basis, as its
    complexity grows linearly with the Changes entries.
    """
    scielo_api = managerapi_dep(settings=settings)

    data = scielo_api.get_changes()

    last_change = list(data)[-1]
    return last_change.get('seq', 0)
