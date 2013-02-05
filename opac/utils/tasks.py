from django.conf import settings

from .sync import datacollector
from .sync import dataloader
from .sync import pipes


def full_sync():
    scielo_api = datacollector.SciELOManagerAPI(settings=settings)
    ppl = pipes.Pipeline(pipes.PIssue,
                         pipes.PMission,
                         pipes.PSection,
                         pipes.PNormalizeJournalTitle,
                         pipes.PCleanup)

    data = scielo_api.get_all_journals('saude-publica')
    transformed_data = ppl.run(data)

    marreta = dataloader.Marreta(settings=settings)
    marreta.rebuild_collection('journals', transformed_data)
